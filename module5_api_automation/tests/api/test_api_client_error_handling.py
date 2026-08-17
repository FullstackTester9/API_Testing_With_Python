# =====================================================
#
#
# =====================================================


import pytest
import requests

from unittest.mock import patch, Mock

from framework.api import (
    ApiClient,
    RequestSpec,
    RequestExecutionError,
    HttpResponseError
)


# =====================================================
# Test timeout handling.
# =====================================================
def test_timeout_is_converted_to_request_execution_error():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = (
            requests.exceptions.Timeout(
                "Connection timed out"
            )
        )

        with pytest.raises(
            RequestExecutionError,
            match="Request timed out"
        ):

            client.send(request)


# =====================================================
# Test original timeout exception preservation.
# This verifies that we don't lose the original error.
# =====================================================
def test_timeout_preserves_original_exception():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    original_exception = requests.exceptions.Timeout(
        "Original timeout"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = original_exception

        with pytest.raises(
            RequestExecutionError
        ) as exc_info:

            client.send(request)

        assert (
            exc_info.value.original_exception
            is original_exception
        )


# =====================================================
# Test connection error.
# =====================================================
def test_connection_error_is_converted_to_request_execution_error():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = (
            requests.exceptions.ConnectionError(
                "Connection refused"
            )
        )

        with pytest.raises(
            RequestExecutionError,
            match="Connection failed"
        ):

            client.send(request)


# =====================================================
# Test generic request exception.
# =====================================================
def test_generic_request_exception_is_handled():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = (
            requests.exceptions.RequestException(
                "Unexpected request error"
            )
        )

        with pytest.raises(
            RequestExecutionError,
            match="HTTP request execution failed"
        ):

            client.send(request)


# =====================================================
# Test HTTP 404.
# =====================================================
def test_404_response_is_converted_to_http_response_error():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/999999"
    )

    mock_response = Mock()

    mock_response.ok = False
    mock_response.status_code = 404

    with patch(
        "framework.api.api_client.requests.request",
        return_value=mock_response
    ):

        with pytest.raises(
            HttpResponseError,
            match="404"
        ) as exc_info:

            client.send(request)

        assert (
            exc_info.value.response
            is mock_response
        )


# =====================================================
# Test HTTP 500.
# =====================================================
def test_500_response_is_converted_to_http_response_error():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    mock_response = Mock()

    mock_response.ok = False
    mock_response.status_code = 500

    with patch(
        "framework.api.api_client.requests.request",
        return_value=mock_response
    ):

        with pytest.raises(
            HttpResponseError,
            match="500"
        ):

            client.send(request)


# =====================================================
# Test successful response.
# =====================================================
def test_successful_response_is_returned():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

    with patch(
        "framework.api.api_client.requests.request",
        return_value=mock_response
    ):

        response = client.send(request)

        assert response is mock_response
        assert response.status_code == 200


# =====================================================
# Test POST success.
# =====================================================
def test_post_success_is_not_affected_by_error_handling():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    payload = {
        "title": "Phase 1.15 Product",
        "price": 100
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        json=payload
    )

    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 201

    with patch(
        "framework.api.api_client.requests.request",
        return_value=mock_response
    ) as mock_request:

        response = client.send(request)

        assert response.status_code == 201

        assert (
            mock_request.call_args.kwargs["json"]
            == payload
        )


# =====================================================
#
#
# =====================================================

# =====================================================
#
#
# =====================================================

# =====================================================
#
#
# =====================================================

# =====================================================
#
#
# =====================================================
