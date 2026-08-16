import pytest

from framework.payloads import build_product_payload
from framework.payloads import build_dynamic_product_title


# =====================================================
# Test payload builder. Verifies that the payload builder
# correctly converts test data into the API payload.
# =====================================================
@pytest.mark.data_management
def test_build_product_payload(valid_product_data):

    payload = build_product_payload(
        title=valid_product_data["title"],
        price=valid_product_data["price"],
        description=valid_product_data["description"],
        category=valid_product_data["category"],
        image=valid_product_data["image"]
    )

    assert payload["title"] == valid_product_data["title"]
    assert payload["price"] == valid_product_data["price"]
    assert payload["description"] == valid_product_data["description"]
    assert payload["category"] == valid_product_data["category"]
    assert payload["image"] == valid_product_data["image"]


# =====================================================
# Payload structure validation. This method makes sure
# that the payload does not accidentally contain
# unexpected fields.
# =====================================================
@pytest.mark.data_management
def test_product_payload_contains_expected_fields(
    valid_product_data
):

    payload = build_product_payload(
        title=valid_product_data["title"],
        price=valid_product_data["price"],
        description=valid_product_data["description"],
        category=valid_product_data["category"],
        image=valid_product_data["image"]
    )

    expected_fields = {
        "title",
        "price",
        "description",
        "category",
        "image"
    }

    assert set(payload.keys()) == expected_fields


# =====================================================
# Payload data type validation. Tests the request side
# before the request reaches the API.
# =====================================================
@pytest.mark.data_management
def test_product_payload_data_types(
    valid_product_data
):

    payload = build_product_payload(
        title=valid_product_data["title"],
        price=valid_product_data["price"],
        description=valid_product_data["description"],
        category=valid_product_data["category"],
        image=valid_product_data["image"]
    )

    assert isinstance(payload["title"], str)
    assert isinstance(payload["price"], (int, float))
    assert isinstance(payload["description"], str)
    assert isinstance(payload["category"], str)
    assert isinstance(payload["image"], str)


# =====================================================
# Dynamic data generation. Verifies dynamic test data
# is generated.
# =====================================================
@pytest.mark.data_management
def test_dynamic_product_title():

    title = build_dynamic_product_title()

    assert title.startswith("QA Product")
    assert len(title) > len("QA Product")


@pytest.mark.data_management
def test_valid_product_payload_fixture(
    valid_product_payload
):

    assert valid_product_payload["title"] == (
        "QA Test Product"
    )

    assert valid_product_payload["price"] == 99.99