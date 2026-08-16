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