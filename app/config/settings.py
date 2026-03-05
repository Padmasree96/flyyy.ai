# Industry-specific configurations
from typing import Dict, List

# No more hardcoding - all strings are centralized here
INDUSTRY_CONFIGS: Dict[str, Dict] = {
    "construction": {
        "table_detection_keywords": ["description", "item", "equipment", "sl no", "particulars"],
        "field_mapping": {
            "product": ["description", "item name", "equipment", "particulars"],
            "brand": ["brand", "make", "manufacturer"],
            "quantity": ["qty", "quantity", "nos"],
            "category": ["category", "group", "system"]
        },
        "thresholds": {
            "fuzzy_match": 85
        }
    },
    "retail": {
        "table_detection_keywords": ["sku", "product", "stock", "upc", "barcode"],
        "field_mapping": {
            "product": ["product name", "item description", "sku name"],
            "brand": ["brand", "manufacturer", "label"],
            "quantity": ["stock level", "count", "remaining", "inventory"],
            "category": ["department", "aisle", "section"]
        },
        "thresholds": {
            "fuzzy_match": 80
        }
    },
    "default": {
        "table_detection_keywords": ["item", "qty", "description"],
        "field_mapping": {
            "product": ["item", "description"],
            "brand": ["brand", "make"],
            "quantity": ["qty", "quantity"],
            "category": ["category"]
        },
        "thresholds": {
            "fuzzy_match": 80
        }
    }
}

DEFAULT_INDUSTRY = "construction"

INVALID_ROW_KEYWORDS = ["total", "subtotal", "grand total", "note", "continued", "carried forward"]

def get_config(industry: str = DEFAULT_INDUSTRY) -> Dict:
    return INDUSTRY_CONFIGS.get(industry, INDUSTRY_CONFIGS["default"])
