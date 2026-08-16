# =====================================================
# This file is used for creating templates for
# different payloads. The values inside "{}" brackets
# are placeholders and will be replaces with actual
# test data.
# =====================================================

# =====================================================
# Payload template for "Product".
# =====================================================
PRODUCT_PAYLOAD_TEMPLATE = {
    "title": "{title}",
    "price": "{price}",
    "description": "{description}",
    "category": "{category}",
    "image": "{image}"
}

# =====================================================
# Building the payload for "PRODUCT" using optional
# fields template.
# =====================================================
PRODUCT_OPTIONAL_PAYLOAD_TEMPLATE = {
    "title": "{title}",
    "price": "{price}",
    "description": "{description}",
    "category": "{category}",
    "image": "{image}",
    "brand": "{brand}"
}