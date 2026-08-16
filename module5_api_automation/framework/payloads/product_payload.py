from datetime import datetime


# =====================================================
# Product payload builder. Converts test data into
# an API request payload.
# =====================================================
def build_product_payload(
    title,
    price,
    description,
    category,
    image
):
    return {
        "title": title,
        "price": price,
        "description": description,
        "category": category,
        "image": image
    }


# =====================================================
# Payload data type validation
# =====================================================
def build_dynamic_product_title(prefix="QA Product"):
    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    return f"{prefix} {timestamp}"