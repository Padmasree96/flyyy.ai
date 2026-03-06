# ─── EPC Category Classification ───
from ..config.settings import EPC_CATEGORY_RULES


def classify_category(product: str) -> str:
    """Classify BOQ item into EPC category."""
    if not product:
        return "misc"

    text = product.lower()

    for category, keywords in EPC_CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "misc"