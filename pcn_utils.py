"""Shared PCN detection, validation, and masking utilities.

Single source of truth for the regex + Luhn logic used by the masking
pipeline (pcn_detection_masking.ipynb), the evaluation harness, and the
method comparison benchmark.
"""

import re
import random
import pandas as pd

# ---------------------------------------------------------------------------
# Regex & constants
# ---------------------------------------------------------------------------
# Compiled once at import; the compiled pattern is shipped to workers with
# the UDF closure rather than recompiled on every batch.
#
#   (?<!\d)              - not preceded by a digit (no suffix of a longer number)
#   (?:\d[\s-]*?){12,18} - 12 to 18 digits, each optionally followed by spaces or
#                          hyphens (non-greedy), covering 4111111111111111,
#                          4111-1111-1111-1111 and 4111 1111 1111 1111
#   \d                   - the final (13th–19th) digit, no trailing separator
#   (?!\d)               - not followed by a digit (no prefix of a longer number)
#
# The lookarounds enforce digit boundaries without \b, which doesn't work
# reliably next to hyphens and spaces.
PCN_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[\s-]*?){12,18}"
    r"\d"
    r"(?!\d)"
)

# Strips separators from a match to get the pure digit string for Luhn.
SEPARATOR_RE = re.compile(r"[\s-]")

CARD_TYPES = {
    "Maestro": {
        "prefix": ["5018", "5020", "5038", "5893", "6304", "6759", "6761", "6762", "6763"],
        "length": 16, "pattern": [4, 4, 4, 4],
    },
    "Mastercard": {
        "prefix": ["51", "52", "53", "54", "55"],
        "length": 16, "pattern": [4, 4, 4, 4],
    },
    "Visa": {
        "prefix": ["4"],
        "length": 16, "pattern": [4, 4, 4, 4],
    },
    "Amex": {
        "prefix": ["34", "37"],
        "length": 15, "pattern": [4, 6, 5],
    },
    "Discover": {
        "prefix": ["6011", "622", "64", "65"],
        "length": 16, "pattern": [4, 4, 4, 4],
    },
    "Diners": {
        "prefix": ["300", "301", "302", "303", "304", "305", "36", "38"],
        "length": 14, "pattern": [4, 6, 4],
    },
    "JCB": {
        "prefix": ["35"],
        "length": 16, "pattern": [4, 4, 4, 4],
    },
}

SEPARATORS = {"hyphen": "-", "space": " ", "none": ""}


# ---------------------------------------------------------------------------
# Luhn helpers
# ---------------------------------------------------------------------------

def passes_luhn(digits: str) -> bool:
    """Standard Luhn mod-10 validation on a pure-digit string.

    Walk the digits right to left, double every second digit (subtracting 9
    when the result exceeds 9), and check the total is divisible by 10.
    This is the gate that separates real PCNs (ISO/IEC 7812-1) from phone,
    account and serial numbers that happen to be 13–19 digits long.
    """
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def compute_luhn_check_digit(partial: str) -> str:
    """Compute the check digit that makes partial + digit Luhn-valid."""
    digits = [int(d) for d in partial]
    odd = digits[-1::-2]
    even = digits[-2::-2]
    total = sum(even)
    for d in odd:
        doubled = d * 2
        total += doubled - 9 if doubled > 9 else doubled
    return str((10 - (total % 10)) % 10)


# ---------------------------------------------------------------------------
# Masking
# ---------------------------------------------------------------------------

def mask_pcns_in_string(text: str, use_luhn: bool = True) -> str:
    """Regex-match PCN candidates, Luhn-validate, mask confirmed ones with X.

    With use_luhn=False every regex candidate is masked (regex-only baseline).

    Matches are replaced right to left so earlier offsets stay valid. Every
    character in a match (digits and separators) becomes 'X', so the output
    keeps the input's length and '||' column delimiters outside the match
    are never disturbed.
    """
    if not text:
        return text
    matches = list(PCN_PATTERN.finditer(text))
    if not matches:
        return text
    chars = list(text)
    for m in reversed(matches):
        raw = m.group()
        digits_only = SEPARATOR_RE.sub("", raw)
        if len(digits_only) < 13 or len(digits_only) > 19:
            continue
        if use_luhn and not passes_luhn(digits_only):
            continue
        for i in range(m.start(), m.end()):
            chars[i] = "X"
    return "".join(chars)


def mask_pcns_regex_only(text: str) -> str:
    """Baseline: mask every regex candidate without Luhn validation."""
    return mask_pcns_in_string(text, use_luhn=False)


# ---------------------------------------------------------------------------
# Card generation (for evaluation corpus)
# ---------------------------------------------------------------------------

def generate_card_number(card_type=None, separator_name="none"):
    """Generate a Luhn-valid card number.

    Returns (formatted_str, raw_digits, card_type).
    """
    if card_type is None:
        card_type = random.choice(list(CARD_TYPES.keys()))
    info = CARD_TYPES[card_type]
    prefix = random.choice(info["prefix"])
    number = prefix
    while len(number) < info["length"] - 1:
        number += str(random.randint(0, 9))
    number += compute_luhn_check_digit(number)

    sep = SEPARATORS.get(separator_name, "")
    if sep == "":
        return number, number, card_type

    parts, pos = [], 0
    for seg_len in info["pattern"]:
        parts.append(number[pos : pos + seg_len])
        pos += seg_len
    return sep.join(parts), number, card_type


def generate_luhn_failing_number(length):
    """Generate a random digit string of given length that fails Luhn."""
    while True:
        digits = "".join(str(random.randint(0, 9)) for _ in range(length))
        if not passes_luhn(digits):
            return digits


def generate_luhn_valid_number(length):
    """Generate a random Luhn-valid digit string of given length."""
    partial = "".join(str(random.randint(0, 9)) for _ in range(length - 1))
    return partial + compute_luhn_check_digit(partial)
