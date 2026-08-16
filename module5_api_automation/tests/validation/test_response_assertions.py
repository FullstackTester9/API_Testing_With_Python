import pytest


# =====================================================
# Tests for status codes.
# =====================================================
@pytest.mark.validation
def test_status_code_assertion(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_status_code(
        response,
        200
    )

# =====================================================
# Tests for JSON content type.
# =====================================================
@pytest.mark.validation
def test_json_content_type_assertion(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_json_content_type(
        response
    )

# =====================================================
# Tests for JSONs response
# =====================================================
@pytest.mark.validation
def test_response_is_json(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_response_is_json(
        response
    )

# =====================================================
# Tests existence of JSON field.
# =====================================================
@pytest.mark.validation
def test_json_field_exists(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_json_field_exists(
        response,
        "id"
    )

# =====================================================
# Tests value of JSON field.
# =====================================================
@pytest.mark.validation
def test_json_field_value(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_json_field_value(
        response,
        "id",
        1
    )

# =====================================================
# Tests JSON field type.
# =====================================================
@pytest.mark.validation
def test_json_field_type(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_json_field_type(
        response,
        "id",
        int
    )

# =====================================================
# Tests for existence of header.
# =====================================================
@pytest.mark.validation
def test_response_header_exists(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_header_exists(
        response,
        "Content-Type"
    )

# =====================================================
# Tests for response time.
# This is only a basic sanity threshold.
# =====================================================
@pytest.mark.validation
def test_response_time(
    api_client,
    assertions
):

    response = api_client.get(
        "/products/1"
    )

    assertions.assert_response_time_less_than(
        response,
        5
    )