# ─── Text Cleaning, Attribute Detection & Validation ───
import re
from typing import Any, List

from ..config.settings import (
    INVALID_ROW_KEYWORDS,
    SECTION_KEYWORDS,
    MAX_PRODUCT_LENGTH,
    IGNORE_WORDS,
    DIMENSION_PATTERN,
    DEPTH_PATTERN,
    MATERIAL_KEYWORDS,
)


def clean_text(text: Any) -> str:
    """Standardized text cleaning for consistency."""
    if text is None:
        return ""

    text_str = str(text).strip()
    text_str = re.sub(r"\s+", " ", text_str)
    return text_str


def clean_quantity(value: Any) -> float:
    """Extract the first numeric value from strings like '10 Nos' or '5.5 Units'."""
    if value is None:
        return 0.0

    match = re.search(r"\d+(\.\d+)?", str(value))
    if match:
        return float(match.group())

    return 0.0


def is_attribute_line(text: str) -> bool:
    """
    Check if a line is an engineering attribute / dimension / specification
    rather than a real material description.
    Examples: '250 mm nominal dia', 'From 3.0 to 4.5m depth'
    """
    if not text:
        return False

    text_lower = text.strip().lower()

    # Dimension pattern: starts with number + unit (e.g. "250 mm", "100 sq.mm")
    if re.match(DIMENSION_PATTERN, text_lower):
        return True

    # Depth pattern: "3.0m depth"
    if re.search(DEPTH_PATTERN, text_lower):
        return True

    # Starts with ignore words
    for w in IGNORE_WORDS:
        if text_lower.startswith(w):
            return True

    return False


def contains_material_keyword(text: str) -> bool:
    """Check if the text contains at least one known material keyword."""
    if not text:
        return False

    text_lower = text.lower()
    return any(kw in text_lower for kw in MATERIAL_KEYWORDS)


def is_valid_product(product: Any) -> bool:
    """Combined validation: length, numeric, totals, sections."""
    if product is None:
        return False

    text = str(product).strip()

    # Too short
    if len(text) < 3:
        return False

    # Pure number (row index)
    if text.replace(".", "").isnumeric():
        return False

    # Paragraph description
    if len(text) > MAX_PRODUCT_LENGTH:
        return False

    text_lower = text.lower()

    # Total / subtotal rows
    if any(k in text_lower for k in INVALID_ROW_KEYWORDS):
        return False

    # Section headings — BUT only if the text does NOT contain a material keyword
    # e.g. "13 Passenger Lift with motor room" has "room" but also "lift"
    has_material = any(kw in text_lower for kw in MATERIAL_KEYWORDS)
    if not has_material and any(k in text_lower for k in SECTION_KEYWORDS):
        return False

    return True
