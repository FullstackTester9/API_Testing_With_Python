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
