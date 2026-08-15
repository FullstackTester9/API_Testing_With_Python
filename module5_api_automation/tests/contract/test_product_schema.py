import pytest

from framework.schemas import PRODUCT_SCHEMA
from jsonschema import ValidationError


# ==============================================================
# Schema validation test
# ==============================================================
@pytest.mark.contract
def test_product_response_matches_schema(
    api_client,
    schema_validator
):

    response = api_client.get(
        "/products/1"
    )

    schema_validator.validate_json(
        response,
        PRODUCT_SCHEMA
    )


# ==============================================================
# HTTP status validation test
# ==============================================================
@pytest.mark.contract
def test_product_response_contract(
    api_client,
    assertions,
    schema_validator
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_status_code(
        response,
        200
    )

    schema_validator.validate_json(
        response,
        PRODUCT_SCHEMA
    )


# ==============================================================
# JSON content validation test
# ==============================================================
@pytest.mark.contract
def test_product_complete_contract(
    api_client,
    assertions,
    schema_validator
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_status_code(
        response,
        200
    )

    assertions.assert_json_content_type(
        response
    )

    schema_validator.validate_json(
        response,
        PRODUCT_SCHEMA
    )


# ==============================================================
# Negative schema test
# ==============================================================
@pytest.mark.contract
def test_invalid_product_response_fails_schema(
    schema_validator
):

    invalid_response = {
        "id": "1",
        "title": "Test Product"
    }

    with pytest.raises(
        AssertionError,
        match="JSON Schema validation failed"
    ):

        schema_validator.validate_json_data(
            invalid_response,
            PRODUCT_SCHEMA
        )



