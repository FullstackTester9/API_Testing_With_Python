from datetime import datetime
from framework.payloads.request_builder import RequestBuilder
from framework.payloads.templates import PRODUCT_PAYLOAD_TEMPLATE


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

# =====================================================
# Building the payload for "PRODUCT" using template.
# =====================================================
def build_product_request(data):
    builder = RequestBuilder(PRODUCT_PAYLOAD_TEMPLATE)

    return builder.build(
        title=data["title"],
        price=data["price"],
        description=data["description"],
        category=data["category"],
        image=data["image"]
    )

# =====================================================
# This provide product specific interface.
# =====================================================
def override_product_request(payload, **overrides):
    builder = RequestBuilder(PRODUCT_PAYLOAD_TEMPLATE)

    return builder.override(
        payload,
        **overrides
    )