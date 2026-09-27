"""Spark Pandas UDF wrapper for PCN masking.

Shared by the masking pipeline (pcn_detection_masking.ipynb) and the method
comparison benchmark so both run the same UDF around the same pcn_utils logic.
"""

import sys

import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

import pcn_utils
from pcn_utils import PCN_PATTERN

# Pickle pcn_utils and this module by value into UDF closures, so executors
# don't need to import them from the workspace.
try:
    from pyspark import cloudpickle

    cloudpickle.register_pickle_by_value(pcn_utils)
    cloudpickle.register_pickle_by_value(sys.modules[__name__])
except Exception as exc:
    print(f"Note: PCN modules not registered for by-value pickling ({exc}); "
          "relying on workspace files being on the executor path.")


def make_mask_udf(mask_fn):
    """Wrap a per-string masking function in a vectorised Pandas UDF.

    Pandas UDFs are called once per Arrow batch (default 10k rows) instead of
    once per row, avoiding per-row JVM↔Python serialisation.

    Inside each batch:
      1. series.str.contains() runs the regex across the whole batch to find
         rows with any PCN candidate; typically most rows have none and are
         skipped entirely.
      2. mask_fn runs only on candidate rows. Luhn and character-level
         masking are per-match operations, so they can't be vectorised.
    """
    @F.pandas_udf(StringType())
    def mask_udf(series: pd.Series) -> pd.Series:
        has_candidate = series.str.contains(PCN_PATTERN, na=False)
        if not has_candidate.any():
            return series
        # Copy so the Arrow-backed input buffer is never mutated
        result = series.copy()
        result[has_candidate] = series[has_candidate].apply(mask_fn)
        return result

    return mask_udf
