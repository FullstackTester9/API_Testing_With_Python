import pytest

from framework.payloads import (
    build_product_request,
    override_product_request,
    build_nested_product_request
)


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

# =====================================================
# Tests for "Product" level overrides.
# =====================================================
@pytest.mark.data_management
def test_product_request_supports_field_override(
    valid_product_data
):

    payload = build_product_request(
        valid_product_data
    )

    updated_payload = override_product_request(
        payload,
        price=999.99
    )

    assert updated_payload["title"] == (
        valid_product_data["title"]
    )

    assert updated_payload["price"] == 999.99

    assert updated_payload["category"] == (
        valid_product_data["category"]
    )

# =====================================================
# Overriding data multiple times.
# =====================================================
@pytest.mark.data_management
@pytest.mark.parametrize(
    "override_data",
    [
        pytest.param(
            {"price": 10.00},
            id="OVERRIDE-001"
        ),
        pytest.param(
            {"price": 100.00},
            id="OVERRIDE-002"
        ),
        pytest.param(
            {
                "price": 999.99,
                "category": "electronics"
            },
            id="OVERRIDE-003"
        )
    ]
)

# =====================================================
# This test handles multiple override combination.
# =====================================================
def test_product_request_with_dynamic_overrides(
    valid_product_data,
    override_data
):

    payload = build_product_request(
        valid_product_data
    )

    updated_payload = override_product_request(
        payload,
        **override_data
    )

    for key, value in override_data.items():
        assert updated_payload[key] == value


# =====================================================
# Tests for nested product request.
# =====================================================
@pytest.mark.data_management
def test_build_nested_product_request():

    data = {
        "title": "Nested QA Product",
        "price": 49.99,
        "description": "Nested payload test",
        "category": "electronics",
        "image": "https://i.pravatar.cc",
        "brand": "QA Brand",
        "manufacturer_name": "QA Corporation",
        "manufacturer_country": "India"
    }

    payload = build_nested_product_request(data)

    assert payload["title"] == data["title"]

    assert (
        payload["metadata"]["brand"]
        == data["brand"]
    )

    assert (
        payload["metadata"]["manufacturer"]["name"]
        == data["manufacturer_name"]
    )

    assert (
        payload["metadata"]["manufacturer"]["country"]
        == data["manufacturer_country"]
    )
