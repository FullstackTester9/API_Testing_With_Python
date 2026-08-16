import pytest

from framework.payloads import build_product_request


# =====================================================
# Requesting valid product data and converting it to
# the payload.
# =====================================================
@pytest.mark.data_management
def test_build_product_request(valid_product_data):

    payload = build_product_request(
        valid_product_data
    )

    assert payload["title"] == (
        valid_product_data["title"]
    )

    assert payload["price"] == (
        valid_product_data["price"]
    )

    assert payload["description"] == (
        valid_product_data["description"]
    )

    assert payload["category"] == (
        valid_product_data["category"]
    )

    assert payload["image"] == (
        valid_product_data["image"]
    )


# =====================================================
# It defines how the test should be executed with
# multiple dataset.
# =====================================================
@pytest.mark.data_management
@pytest.mark.parametrize(
    "product_data",
    [
        pytest.param(
            {
                "title": "Template Product A",
                "price": 10.99,
                "description": "Template test A",
                "category": "electronics",
                "image": "https://i.pravatar.cc"
            },
            id="TPL-001"
        ),
        pytest.param(
            {
                "title": "Template Product B",
                "price": 25.50,
                "description": "Template test B",
                "category": "jewelery",
                "image": "https://i.pravatar.cc"
            },
            id="TPL-002"
        )
    ]
)

# =====================================================
# Creating payloads form multiple datasets.
# =====================================================
def test_product_request_builder_with_multiple_datasets(
    product_data
):

    payload = build_product_request(product_data)

    assert payload == product_data