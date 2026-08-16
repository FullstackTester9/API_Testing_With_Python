import pytest

from framework.payloads import RequestBuilder


# =====================================================
# Actual values are inserted into the placeholders
# of template.
# =====================================================
@pytest.mark.data_management
def test_request_builder_replaces_template_values():

    template = {
        "title": "{title}",
        "price": "{price}"
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        price=99.99
    )

    assert payload["title"] == "QA Product"
    assert payload["price"] == 99.99


# =====================================================
# Verifies that the  original template remains
# unchanged.
# =====================================================
@pytest.mark.data_management
def test_request_builder_does_not_modify_template():

    template = {
        "title": "{title}",
        "price": "{price}"
    }

    builder = RequestBuilder(template)

    builder.build(
        title="Modified Product",
        price=100
    )

    assert template["title"] == "{title}"
    assert template["price"] == "{price}"


# =====================================================
# This test prevents accidental payload fields from
# silently entering the request.
# =====================================================
@pytest.mark.data_management
def test_request_builder_rejects_unknown_field():

    template = {
        "title": "{title}",
        "price": "{price}"
    }

    builder = RequestBuilder(template)

    with pytest.raises(KeyError):
        builder.build(
            title="QA Product",
            unknown_field="Invalid"
        )


# =====================================================
# Verifies that only "price" changes.
# =====================================================
@pytest.mark.data_management
def test_request_builder_overrides_existing_field():

    template = {
        "title": "{title}",
        "price": "{price}",
        "category": "{category}"
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        price=25.50,
        category="electronics"
    )

    updated_payload = builder.override(
        payload,
        price=99.99
    )

    assert updated_payload["title"] == "QA Product"
    assert updated_payload["price"] == 99.99
    assert updated_payload["category"] == "electronics"


# =====================================================
# Testing for multiple override.
# =====================================================
@pytest.mark.data_management
def test_request_builder_supports_multiple_overrides():

    template = {
        "title": "{title}",
        "price": "{price}",
        "category": "{category}"
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        price=25.50,
        category="electronics"
    )

    updated_payload = builder.override(
        payload,
        price=199.99,
        category="jewelery"
    )

    assert updated_payload["title"] == "QA Product"
    assert updated_payload["price"] == 199.99
    assert updated_payload["category"] == "jewelery"


# =====================================================
# Test for original payload isolation.
# =====================================================
@pytest.mark.data_management
def test_request_builder_override_does_not_modify_original():

    template = {
        "title": "{title}",
        "price": "{price}"
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        price=25.50
    )

    updated_payload = builder.override(
        payload,
        price=999.99
    )

    assert payload["price"] == 25.50
    assert updated_payload["price"] == 999.99


# =====================================================
# Test for invalid override. This prevents accidental
# field from being added to the API.
# =====================================================
@pytest.mark.data_management
def test_request_builder_rejects_unknown_override_field():

    template = {
        "title": "{title}",
        "price": "{price}"
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        price=25.50
    )

    with pytest.raises(KeyError):
        builder.override(
            payload,
            unknown_field="Invalid"
        )


# =====================================================
# Tests for nested field override.
# =====================================================
@pytest.mark.data_management
def test_request_builder_sets_nested_field():

    template = {
        "title": "{title}",
        "metadata": {
            "brand": "{brand}",
            "country": "{country}"
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        metadata={
            "brand": "Original Brand",
            "country": "India"
        }
    )

    updated_payload = builder.set_nested(
        payload,
        "metadata.brand",
        "Updated Brand"
    )

    assert updated_payload["metadata"]["brand"] == (
        "Updated Brand"
    )

    assert updated_payload["metadata"]["country"] == (
        "India"
    )


# =====================================================
# Verifies multiple nesting levels.
# =====================================================
@pytest.mark.data_management
def test_request_builder_sets_deep_nested_field():

    template = {
        "metadata": {
            "manufacturer": {
                "name": "{name}",
                "country": "{country}"
            }
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        metadata={
            "manufacturer": {
                "name": "Original Manufacturer",
                "country": "India"
            }
        }
    )

    updated_payload = builder.set_nested(
        payload,
        "metadata.manufacturer.name",
        "Updated Manufacturer"
    )

    assert (
        updated_payload["metadata"]
        ["manufacturer"]
        ["name"]
        == "Updated Manufacturer"
    )

    assert (
        updated_payload["metadata"]
        ["manufacturer"]
        ["country"]
        == "India"
    )


# =====================================================
# Verifies invalid nested path.
# =====================================================
@pytest.mark.data_management
def test_request_builder_rejects_unknown_nested_field():

    template = {
        "metadata": {
            "brand": "{brand}"
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        metadata={
            "brand": "QA Brand"
        }
    )

    with pytest.raises(KeyError):

        builder.set_nested(
            payload,
            "metadata.unknown",
            "Invalid"
        )


# =====================================================
# Tests for optional field addition.
# =====================================================
@pytest.mark.data_management
def test_request_builder_adds_optional_field():

    template = {
        "title": "{title}",
        "metadata": {}
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        metadata={}
    )

    updated_payload = builder.add_optional(
        payload,
        "metadata.brand",
        "QA Brand"
    )

    assert (
        updated_payload["metadata"]["brand"]
        == "QA Brand"
    )


# =====================================================
# Tests for deep optional field addition.
# =====================================================
@pytest.mark.data_management
def test_request_builder_adds_deep_optional_field():

    template = {
        "title": "{title}",
        "metadata": {}
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        metadata={}
    )

    updated_payload = builder.add_optional(
        payload,
        "metadata.manufacturer.country",
        "India"
    )

    assert (
        updated_payload["metadata"]
        ["manufacturer"]
        ["country"]
        == "India"
    )


# =====================================================
# Tests for optional field removal.
# =====================================================
@pytest.mark.data_management
def test_request_builder_removes_optional_field():

    template = {
        "title": "{title}",
        "metadata": {
            "brand": "{brand}"
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        title="QA Product",
        metadata={
            "brand": "QA Brand"
        }
    )

    updated_payload = builder.remove_optional(
        payload,
        "metadata.brand"
    )

    assert "brand" not in (
        updated_payload["metadata"]
    )


# =====================================================
# Tests for deep optional field removal
# =====================================================
@pytest.mark.data_management
def test_request_builder_removes_deep_optional_field():

    template = {
        "metadata": {
            "manufacturer": {
                "name": "{name}",
                "country": "{country}"
            }
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        metadata={
            "manufacturer": {
                "name": "QA Corp",
                "country": "India"
            }
        }
    )

    updated_payload = builder.remove_optional(
        payload,
        "metadata.manufacturer.country"
    )

    assert (
        "country"
        not in updated_payload["metadata"]["manufacturer"]
    )


# =====================================================
# Verify original payload is not modified.
# =====================================================
@pytest.mark.data_management
def test_nested_operations_do_not_modify_original():

    template = {
        "metadata": {
            "brand": "Original"
        }
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        metadata={
            "brand": "Original"
        }
    )

    updated_payload = builder.set_nested(
        payload,
        "metadata.brand",
        "Updated"
    )

    assert (
        payload["metadata"]["brand"]
        == "Original"
    )

    assert (
        updated_payload["metadata"]["brand"]
        == "Updated"
    )


# =====================================================
# Tests for optional field that doesn't exist.
# =====================================================
@pytest.mark.data_management
def test_remove_missing_optional_field_is_safe():

    template = {
        "metadata": {}
    }

    builder = RequestBuilder(template)

    payload = builder.build(
        metadata={}
    )

    updated_payload = builder.remove_optional(
        payload,
        "metadata.brand"
    )

    assert updated_payload == payload


# =====================================================
#
# =====================================================