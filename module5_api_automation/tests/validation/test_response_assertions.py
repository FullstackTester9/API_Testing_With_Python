import pytest


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