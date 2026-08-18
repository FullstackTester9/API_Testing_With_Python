# =====================================================
# Retry delay helper.
# The method makes retry timing easy to control and test.
# =====================================================

import time
import pytest
import requests

from unittest.mock import Mock, patch

from framework.api import (
    ApiClient,
    RequestSpec,
    RequestExecutionError,
    HttpResponseError
)

# =====================================================
# Test successful request without retry.
# A successful first request must not retry.
# =====================================================
def test_successful_request_requires_no_retry():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=2
    )

    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200

    with patch(
        "framework.api.api_client.requests.request",
        return_value=mock_response
    ) as mock_request:

        response = client.send(request)

        assert response.status_code == 200
        assert mock_request.call_count == 1

# =====================================================
# Test timeout retry.
# =====================================================
def test_timeout_is_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=2
    )

    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            mock_response
        ]

        with patch(
            "framework.api.api_client.time.sleep"
        ):

            response = client.send(request)

        assert response.status_code == 200
        assert mock_request.call_count == 3

# =====================================================
# Test connection retry.
# =====================================================
def test_connection_error_is_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=1
    )

    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = [
            requests.exceptions.ConnectionError(),
            mock_response
        ]

        with patch(
            "framework.api.api_client.time.sleep"
        ):

            response = client.send(request)

        assert response.status_code == 200
        assert mock_request.call_count == 2

# =====================================================
# Test 503 retry.
# =====================================================
def test_503_response_is_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=2
    )

    response_503 = Mock()
    response_503.ok = False
    response_503.status_code = 503

    response_200 = Mock()
    response_200.ok = True
    response_200.status_code = 200

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = [
            response_503,
            response_503,
            response_200
        ]

        with patch(
            "framework.api.api_client.time.sleep"
        ):

            response = client.send(request)

        assert response.status_code == 200
        assert mock_request.call_count == 3

# =====================================================
# Test 404 is not retried.
# This request should execute only once.
# =====================================================
def test_404_is_not_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/999999",
        retry_count=3
    )

    response_404 = Mock()
    response_404.ok = False
    response_404.status_code = 404

    with patch(
        "framework.api.api_client.requests.request",
        return_value=response_404
    ) as mock_request:

        with pytest.raises(
            HttpResponseError
        ):

            client.send(request)

        assert mock_request.call_count == 1

# =====================================================
# Test retry exhaustion.
# =====================================================
def test_retry_exhaustion_raises_request_execution_error():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=2
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = (
            requests.exceptions.Timeout(
                "Timeout"
            )
        )

        with patch(
            "framework.api.api_client.time.sleep"
        ):

            with pytest.raises(
                RequestExecutionError
            ):

                client.send(request)

        assert mock_request.call_count == 3

# =====================================================
# Test negative retry count configuration validation.
# =====================================================
def test_negative_retry_count_is_rejected():

    with pytest.raises(
        ValueError,
        match="Retry count cannot be negative"
    ):

        RequestSpec(
            method="GET",
            endpoint="/products",
            retry_count=-1
        )
# =====================================================
# Test negative retry delay configuration validation.
# =====================================================
def test_negative_retry_delay_is_rejected():

    with pytest.raises(
        ValueError,
        match="Retry delay cannot be negative"
    ):

        RequestSpec(
            method="GET",
            endpoint="/products",
            retry_delay=-1
        )

# =====================================================
# Test retry delay.
# =====================================================
def test_retry_delay():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=1,
        retry_delay=2
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = [
            requests.exceptions.Timeout(),
            Mock(
                ok=True,
                status_code=200
            )
        ]

        with patch(
            "framework.api.api_client.time.sleep"
        ) as mock_sleep:

            response = client.send(request)

            assert response.status_code == 200

            mock_sleep.assert_called_once_with(2)


# =====================================================
# Test retry safe methods (Retry policy test).
# =====================================================
def test_get_is_retryable_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    assert client._is_retryable_method("GET") is True


# =====================================================
# Test PUT (Retry policy test).
# =====================================================
def test_put_is_retryable_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    assert client._is_retryable_method("PUT") is True


# =====================================================
# Test DELETE (Retry policy test).
# =====================================================
def test_delete_is_retryable_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    assert client._is_retryable_method("DELETE") is True


# =====================================================
# Tests POST is not automatically retryable.
# =====================================================
def test_post_is_not_retryable_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    assert client._is_retryable_method("POST") is False


# =====================================================
# Test PATCH is not automatically retryable.
# =====================================================
def test_patch_is_not_retryable_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    assert client._is_retryable_method("PATCH") is False


# =====================================================
# Test POST timeout is not retried.
# =====================================================
def test_post_timeout_is_not_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        retry_count=3
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = (
            requests.exceptions.Timeout()
        )

        with pytest.raises(
            RequestExecutionError
        ):

            client.send(request)

        assert mock_request.call_count == 1


# =====================================================
# Test POST 503 is not retried.
# =====================================================
def test_post_503_is_not_retried():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        retry_count=3
    )

    response_503 = Mock()

    response_503.ok = False
    response_503.status_code = 503

    with patch(
        "framework.api.api_client.requests.request",
        return_value=response_503
    ) as mock_request:

        with pytest.raises(
            HttpResponseError
        ):

            client.send(request)

        assert mock_request.call_count == 1


# =====================================================
# Test idempotency-key preservation. Verify that the
# header reaches the HTTP request.
# This test does not make POST retryable.
# =====================================================
def test_idempotency_key_is_preserved():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        headers={
            "Idempotency-Key": "unique-request-123"
        }
    )

    response = Mock()
    response.ok = True
    response.status_code = 201

    with patch(
        "framework.api.api_client.requests.request",
        return_value=response
    ) as mock_request:

        client.send(request)

        call_kwargs = mock_request.call_args.kwargs

        assert (
            call_kwargs["headers"]["Idempotency-Key"]
            == "unique-request-123"
        )


# =====================================================
# Default backoff.
# =====================================================
def test_default_backoff_delay():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_delay=2
    )

    assert (
        client._calculate_retry_delay(
            request,
            1
        )
        == 2
    )


# =====================================================
# Test exponential backoff.
# =====================================================
def test_exponential_backoff_delay():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_delay=2
    )

    assert (
        client._calculate_retry_delay(
            request,
            1
        )
        == 2
    )

    assert (
        client._calculate_retry_delay(
            request,
            2
        )
        == 4
    )

    assert (
        client._calculate_retry_delay(
            request,
            3
        )
        == 8
    )


# =====================================================
# Test backoff factor.
# =====================================================
def test_backoff_factor():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_delay=2,
        backoff_factor=2
    )

    assert (
        client._calculate_retry_delay(
            request,
            1
        )
        == 4
    )

    assert (
        client._calculate_retry_delay(
            request,
            2
        )
        == 8
    )


# =====================================================
# Test maximum delay.
# =====================================================
def test_max_retry_delay():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_delay=2,
        max_retry_delay=5
    )

    assert (
        client._calculate_retry_delay(
            request,
            1
        )
        == 2
    )

    assert (
        client._calculate_retry_delay(
            request,
            2
        )
        == 4
    )

    assert (
        client._calculate_retry_delay(
            request,
            3
        )
        == 5
    )






# =====================================================
#
# =====================================================

# =====================================================
#
# =====================================================