# Text Cleaning Utilities
from typing import Any
import re
import pandas as pd

def clean_text(text: Any) -> str:
    """Standardized text cleaning for consistency."""
    if text is None:
        return ""
    
    # Convert to string and strip whitespace
    text_str = str(text).strip()
    
    # Remove multiple spaces/newlines
    text_str = re.sub(r'\s+', ' ', text_str)
    
    return text_str

def normalize_header(text: Any) -> str:
    """Normalize headers for better matching."""
    cleaned = clean_text(text).lower()
    # Remove special characters
    cleaned = re.sub(r'[^a-z0-9]', '', cleaned)
    return cleaned

def clean_quantity(value: Any) -> float:
    """Extract numerical value from strings like '10 Nos' or '5.5 Units'."""
    if value is None or pd.isna(value):
        return 0.0
    
    # Search for first number (integer or decimal)
    match = re.search(r"(\d+(\.\d+)?)", str(value))
    if match:
        try:
            return float(match.group(1))
        except (ValueError, TypeError):
            pass
    return 0.0

def is_valid_row(product_text: str, invalid_keywords: list) -> bool:
    """Check if a row is valid (not a total/subtotal row)."""
    if not product_text:
        return False
    
    text = str(product_text).lower()
    return not any(k.lower() in text for k in invalid_keywords)
