# Category Classifier
def classify_category(product):

    p = product.lower()

    if "breaker" in p:
        return "Switchgear"

    if "rmu" in p:
        return "Switchgear"

    if "transformer" in p:
        return "Power Equipment"

    return "Electrical Equipment"