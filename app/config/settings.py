# ─── Centralized Configuration ───
from typing import Dict, List

# ─── Header Detection ───
HEADER_SCAN_LIMIT = 20

HEADER_KEYWORDS = [
    "description",
    "item",
    "material",
    "equipment",
    "qty",
    "quantity",
    "unit",
    "rate",
    "amount"
]

# ─── Row Filtering ───
SECTION_KEYWORDS = [
    "building",
    "hall",
    "laboratory",
    "room",
    "area"
]

INVALID_ROW_KEYWORDS = [
    "total",
    "subtotal",
    "grand total",
    "note",
    "remarks"
]

# ─── Extraction Limits ───
MAX_PRODUCT_LENGTH = 200  # Raised slightly to allow merged descriptions
MAX_REASONABLE_QUANTITY = 1000

# ─── Engineering Attribute Ignore Words ───
# NOTE: 'total'/'subtotal' are NOT here — they're in INVALID_ROW_KEYWORDS
IGNORE_WORDS = [
    "floor", "depth", "nominal", "dia",
    "from", "upto", "schedule",
    "as per", "refer", "drawing"
]

# ─── Regex Patterns for Attribute Lines ───
DIMENSION_PATTERN = r"^\s*\d+\s*(mm|cm|m|sq\.?mm)"
DEPTH_PATTERN = r"\d+(\.\d+)?\s*m\s*depth"

# ─── EPC Material Classification Keywords ───
EPC_CATEGORY_RULES = {
    "Electrical": [
        "switch", "socket", "mcb", "isolator",
        "earthing", "charger", "junction",
        "transformer", "dg set", "substation",
        "switchgear", "breaker", "ups"
    ],
    "Plumbing": [
        "pipe", "valve", "tap", "cock",
        "pump", "chilled water", "drain", "water supply"
    ],
    "Lighting": [
        "light", "lamp", "led", "downlight",
        "tube", "flood", "bulkhead", "lighting"
    ],
    "Cable & Wiring": [
        "cable", "wire", "conduit",
        "tray", "xlpe", "armoured", "wiring"
    ],
    "Panels": [
        "panel", "distribution board",
        "rmu", "ht panel", "lt panel", "control panel"
    ],
    "Civil materials": [
        "cement", "sand", "brick",
        "aggregate", "concrete",
        "bitumen", "steel", "reinforcement"
    ],
    "Fixtures": [
        "lift", "elevator", "fan",
        "mirror", "dryer", "holder",
        "sensor", "fixture"
    ]
}

# ─── Material Keyword Validation ───
# Only keep rows that contain at least one of these real-material words
MATERIAL_KEYWORDS = [
    "pipe", "cable", "lift", "light", "panel",
    "cement", "brick", "fan", "tray", "wire",
    "valve", "pump", "switch", "socket", "conduit",
    "transformer", "breaker", "lamp", "led", "xlpe",
    "armoured", "concrete", "sand", "steel", "elevator",
    "sensor", "fixture", "mcb", "isolator", "earthing",
    "bitumen", "aggregate", "holder", "dryer", "mirror",
    "ups", "dg set", "substation", "switchgear",
    "distribution board", "rmu", "tap", "cock",
    "chilled water", "drain", "water supply",
    "reinforcement", "bulkhead", "flood", "downlight",
    "junction", "charger", "tube"
]

# ─── Industry Configs ───
INDUSTRY_CONFIGS: Dict[str, Dict] = {
    "construction": {
        "table_detection_keywords": ["description", "item", "equipment", "sl no", "particulars"],
        "field_mapping": {
            "product": ["description", "item name", "equipment", "particulars", "item"],
            "brand": ["brand", "make", "manufacturer"],
            "quantity": ["qty", "quantity", "nos"],
            "category": ["category", "group", "system"]
        },
        "thresholds": {
            "fuzzy_match": 70
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
            "fuzzy_match": 70
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
            "fuzzy_match": 70
        }
    }
}

DEFAULT_INDUSTRY = "construction"


def get_config(industry: str = DEFAULT_INDUSTRY) -> Dict:
    return INDUSTRY_CONFIGS.get(industry, INDUSTRY_CONFIGS["default"])
