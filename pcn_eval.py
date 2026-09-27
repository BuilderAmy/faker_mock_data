"""Shared span-level and field-level scoring for the PCN evaluation corpus."""

import json
import pandas as pd

TEXT_COLUMNS = ["text_field", "card_number_field", "other_number_field", "metadata_field"]


def positions_to_ranges(positions):
    """Convert a set of positions into contiguous (start, end) ranges."""
    sorted_pos = sorted(positions)
    ranges = []
    start = sorted_pos[0]
    prev = start
    for p in sorted_pos[1:]:
        if p == prev + 1:
            prev = p
        else:
            ranges.append((start, prev + 1))
            start = p
            prev = p
    ranges.append((start, prev + 1))
    return ranges


def compute_prf(tp, fp, fn):
    """Compute precision, recall, F1 from counts."""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def evaluate_row(row, text_columns=TEXT_COLUMNS, masked_suffix="_masked"):
    """Evaluate a single row. Returns span results, field results, and FP details.

    Expects each column in `text_columns` to have a masked counterpart named
    f"{col}{masked_suffix}".
    """
    annotations = json.loads(row["annotations"])
    span_results = []
    field_results = []
    fp_details = []

    for col in text_columns:
        original = row[col]
        masked = row[f"{col}{masked_suffix}"]

        if pd.isna(original):
            continue

        col_annotations = [a for a in annotations if a["field"] == col]
        has_annotations = len(col_annotations) > 0

        # Check which characters were masked
        masked_positions = set()
        for i in range(len(original)):
            if i < len(masked) and original[i] != masked[i]:
                masked_positions.add(i)
        was_masked = len(masked_positions) > 0

        # --- Span-level evaluation ---
        annotated_positions = set()
        for a in col_annotations:
            span_positions = set(range(a["start"], a["end"]))
            annotated_positions.update(span_positions)

            span_masked = span_positions.issubset(masked_positions)
            partially_masked = len(span_positions & masked_positions) > 0 and not span_masked

            if span_masked:
                verdict = "TP"
            elif partially_masked:
                verdict = "PARTIAL_FN"
            else:
                verdict = "FN"

            span_results.append({
                "test_id": row["test_id"],
                "test_category": row["test_category"],
                "test_label": row["test_label"],
                "field": col,
                "card_type": a.get("card_type", ""),
                "separator": a.get("separator", ""),
                "digits": a["digits"],
                "verdict": verdict,
            })

        # --- False positive detection ---
        fp_positions = masked_positions - annotated_positions
        if fp_positions:
            for start, end in positions_to_ranges(fp_positions):
                span_results.append({
                    "test_id": row["test_id"],
                    "test_category": row["test_category"],
                    "test_label": row["test_label"],
                    "field": col,
                    "card_type": "",
                    "separator": "",
                    "digits": original[start:end],
                    "verdict": "FP",
                })
                fp_details.append({
                    "test_id": row["test_id"],
                    "field": col,
                    "start": start,
                    "end": end,
                    "original_text": original[max(0, start - 10):end + 10],
                })

        # --- Field-level evaluation ---
        if has_annotations and was_masked:
            field_verdict = "TP"
        elif not has_annotations and was_masked:
            field_verdict = "FP"
        elif has_annotations and not was_masked:
            field_verdict = "FN"
        else:
            field_verdict = "TN"

        field_results.append({
            "test_id": row["test_id"],
            "test_category": row["test_category"],
            "test_label": row["test_label"],
            "field": col,
            "verdict": field_verdict,
        })

    return span_results, field_results, fp_details


def evaluate_corpus(corpus_df, text_columns=TEXT_COLUMNS, masked_suffix="_masked"):
    """Evaluate every row. Returns (span_df, field_df, fp_df)."""
    all_span, all_field, all_fp = [], [], []
    for _, row in corpus_df.iterrows():
        sr, fr, fp = evaluate_row(row, text_columns, masked_suffix)
        all_span.extend(sr)
        all_field.extend(fr)
        all_fp.extend(fp)
    return pd.DataFrame(all_span), pd.DataFrame(all_field), pd.DataFrame(all_fp)


def summarise_metrics(span_df, field_df):
    """Aggregate span- and field-level counts into accuracy / P / R / F1.

    Accuracy is reported at field level only: span-level scoring has no
    true negatives (an unannotated, unmasked span is not an event).
    """
    span_counts = span_df["verdict"].value_counts() if len(span_df) else pd.Series(dtype=int)
    span_tp = int(span_counts.get("TP", 0))
    span_fp = int(span_counts.get("FP", 0))
    span_fn = int(span_counts.get("FN", 0) + span_counts.get("PARTIAL_FN", 0))
    span_p, span_r, span_f1 = compute_prf(span_tp, span_fp, span_fn)

    field_counts = field_df["verdict"].value_counts() if len(field_df) else pd.Series(dtype=int)
    field_tp = int(field_counts.get("TP", 0))
    field_fp = int(field_counts.get("FP", 0))
    field_fn = int(field_counts.get("FN", 0))
    field_tn = int(field_counts.get("TN", 0))
    field_total = field_tp + field_fp + field_fn + field_tn
    field_p, field_r, field_f1 = compute_prf(field_tp, field_fp, field_fn)
    field_acc = (field_tp + field_tn) / field_total if field_total else 0.0

    return {
        "span_tp": span_tp, "span_fp": span_fp, "span_fn": span_fn,
        "span_precision": span_p, "span_recall": span_r, "span_f1": span_f1,
        "field_tp": field_tp, "field_fp": field_fp,
        "field_fn": field_fn, "field_tn": field_tn,
        "field_accuracy": field_acc,
        "field_precision": field_p, "field_recall": field_r, "field_f1": field_f1,
    }
