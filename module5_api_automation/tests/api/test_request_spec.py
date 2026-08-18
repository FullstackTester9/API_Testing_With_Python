import requests
import pytest
from unittest.mock import patch, Mock

from framework.api.api_client import ApiClient
from framework.api.request_spec import RequestSpec

# =====================================================
# Test HTTP method normalization.
# =====================================================
def test_request_spec_normalizes_http_method():

    request = RequestSpec(
        method="post",
        endpoint="/products"
    )

    assert request.method == "POST"


# =====================================================
# Test endpoints.
# =====================================================
def test_request_spec_stores_endpoint():

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    assert request.endpoint == "/products"


# =====================================================
# Test path parameter.
# =====================================================
def test_request_spec_resolves_path_parameter():

    request = RequestSpec(
        method="GET",
        endpoint="/products/{product_id}",
        path_params={
            "product_id": 5
        }
    )

    assert (
        request.resolved_endpoint()
        == "/products/5"
    )


# =====================================================
# Test missing path parameter.
# =====================================================
def test_request_spec_rejects_unresolved_path_parameter():

    request = RequestSpec(
        method="GET",
        endpoint="/products/{product_id}"
    )

    with pytest.raises(ValueError):

        request.resolved_endpoint()


# =====================================================
# Test query parameter.
# =====================================================
def test_request_spec_stores_query_parameters():

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        query_params={
            "limit": 5
        }
    )

    assert request.query_params["limit"] == 5


# =====================================================
# Test headers.
# =====================================================
def test_request_spec_stores_headers():

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        headers={
            "Accept": "application/json"
        }
    )

    assert (
        request.headers["Accept"]
        == "application/json"
    )


# =====================================================
# Test JSON payload.
# =====================================================
def test_request_spec_stores_json_payload():

    payload = {
        "title": "QA Product",
        "price": 99.99
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        json=payload
    )

    assert request.json == payload


# =====================================================
# Test authentication flag.
# =====================================================
def test_request_spec_stores_authentication_requirement():

    request = RequestSpec(
        method="GET",
        endpoint="/products/1",
        authenticated=True
    )

    assert request.authenticated is True


# =====================================================
# Test empty method.
# =====================================================
def test_request_spec_rejects_empty_method():

    with pytest.raises(ValueError):

        RequestSpec(
            method="",
            endpoint="/products"
        )


# =====================================================
# Test empty endpoint.
# =====================================================
def test_request_spec_rejects_empty_endpoint():

    with pytest.raises(ValueError):

        RequestSpec(
            method="GET",
            endpoint=""
        )


# =====================================================
# Test complete request specification.
# =====================================================
def test_request_spec_supports_complete_request_definition():

    payload = {
        "title": "QA Product",
        "price": 99.99
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products/{product_id}",
        path_params={
            "product_id": 1
        },
        query_params={
            "source": "automation"
        },
        headers={
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30,
        verify_ssl=True,
        authenticated=True
    )

    assert request.method == "POST"

    assert (
        request.resolved_endpoint()
        == "/products/1"
    )

    assert (
        request.query_params["source"]
        == "automation"
    )

    assert (
        request.headers["Content-Type"]
        == "application/json"
    )

    assert request.json == payload

    assert request.timeout == 30

    assert request.verify_ssl is True

    assert request.authenticated is True


# =====================================================
# Test ApiClient.send(). This test doesn't make real
# HTTP request.Only tests actual integration.
# =====================================================
def test_api_client_send_executes_request():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/1"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        mock_request.assert_called_once()


# =====================================================
# Verify method, URL and parameter from "RequestSpec" is
# transferred to the ApiClient.
# =====================================================
def test_api_client_send_builds_request_correctly():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/{product_id}",
        path_params={
            "product_id": 1
        },
        query_params={
            "limit": 5
        },
        headers={
            "Accept": "application/json"
        }
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        mock_request.assert_called_once_with(
            method="GET",
            url="https://fakestoreapi.com/products/1",
            params={
                "limit": 5
            },
            headers={
                "Accept": "application/json"
            },
            json=None,
            timeout=30,
            verify=True
        )


# =====================================================
# Test POST payload through send().
# =====================================================
def test_api_client_send_supports_post_payload():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    payload = {
        "title": "QA Product",
        "price": 99.99
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        json=payload
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        mock_request.assert_called_once_with(
            method="POST",
            url="https://fakestoreapi.com/products",
            params={},
            headers={},
            json=payload,
            timeout=30,
            verify=True
        )


# =====================================================
# Test request-level timeout. It should override
# clients default timeout.
# =====================================================
def test_api_client_send_uses_request_timeout():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        timeout=30
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        timeout=10
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["timeout"]
            == 10
        )


# =====================================================
# Test request level SSL setting.
# =====================================================
def test_api_client_send_uses_request_ssl_setting():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        verify_ssl=True
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        verify_ssl=False
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["verify"]
            is False
        )


# =====================================================
# Test authentication integration.
# =====================================================
def test_api_client_send_supports_authenticated_request():

    class FakeTokenProvider:

        def get_token(self):
            return "test-token"

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        token_provider=FakeTokenProvider()
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/1",
        authenticated=True
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["headers"]
            ["Authorization"]
            == "Bearer test-token"
        )


# =====================================================
# Test for unsupported HTTP method.
# =====================================================
def test_api_client_send_rejects_unsupported_http_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="OPTIONS",
        endpoint="/products"
    )

    with pytest.raises(
        ValueError,
        match="Unsupported HTTP method"
    ):
        client.send(request)


# =====================================================
# Test all supported HTTP method.
# =====================================================
@pytest.mark.parametrize(
    "method",
    [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
def test_api_client_send_supports_http_methods(method):

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method=method,
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["method"]
            == method
        )


# =====================================================
# Test lowercase HTTP method. Verifies that execution
# layer receives normalized value.
# =====================================================
def test_api_client_send_normalizes_lowercase_method():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="post",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["method"]
            == "POST"
        )


# =====================================================
# Test request level timeout.
# =====================================================
def test_request_timeout_overrides_client_timeout():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        timeout=30
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        timeout=10
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["timeout"]
            == 10
        )


# =====================================================
# Test client level timeout fallback.
# =====================================================
def test_client_timeout_used_when_request_timeout_missing():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        timeout=45
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["timeout"]
            == 45
        )


# =====================================================
# Test request level SSL override.
# =====================================================
def test_request_ssl_setting_overrides_client_setting():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        verify_ssl=True
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        verify_ssl=False
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["verify"]
            is False
        )


# =====================================================
# Test client level SSL fallback.
# =====================================================
def test_client_ssl_setting_used_when_request_setting_missing():

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        verify_ssl=False
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products"
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["verify"]
            is False
        )


# =====================================================
# Test query parameter dispatch.
# =====================================================
def test_query_parameters_are_dispatched():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        query_params={
            "limit": 5
        }
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["params"]
            == {"limit": 5}
        )


# =====================================================
# Test header dispatch.
# =====================================================
def test_headers_are_dispatched():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        headers={
            "Accept": "application/json"
        }
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["headers"]
            == {
                "Accept": "application/json"
            }
        )


# =====================================================
# Test JSON payload dispatch.
# =====================================================
def test_json_payload_is_dispatched():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    payload = {
        "title": "Automation Product",
        "price": 99.99
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products",
        json=payload
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["json"]
            == payload
        )


# =====================================================
# Test path parameter dispatch.
# =====================================================
def test_path_parameter_is_resolved_before_dispatch():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/{product_id}",
        path_params={
            "product_id": 1
        }
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        assert (
            mock_request.call_args.kwargs["url"]
            == "https://fakestoreapi.com/products/1"
        )


# =====================================================
# Test authentication dispatch
# =====================================================
def test_authenticated_request_injects_authorization_header():

    class FakeTokenProvider:

        def get_token(self):
            return "phase14-token"

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        token_provider=FakeTokenProvider()
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/1",
        authenticated=True
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        headers = (
            mock_request.call_args.kwargs["headers"]
        )

        assert (
            headers["Authorization"]
            == "Bearer phase14-token"
        )


# =====================================================
# Test header & authentication in combination.
# =====================================================
def test_authenticated_request_preserves_custom_headers():

    class FakeTokenProvider:

        def get_token(self):
            return "phase14-token"

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        token_provider=FakeTokenProvider()
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products/1",
        headers={
            "Accept": "application/json"
        },
        authenticated=True
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        headers = (
            mock_request.call_args.kwargs["headers"]
        )

        assert (
            headers["Accept"]
            == "application/json"
        )

        assert (
            headers["Authorization"]
            == "Bearer phase14-token"
        )


# =====================================================
# Test complete request dispatch. This is an end-to-end
# framework-level dispatch test.
# =====================================================
def test_complete_request_dispatch():

    class FakeTokenProvider:

        def get_token(self):
            return "complete-token"

    client = ApiClient(
        base_url="https://fakestoreapi.com",
        timeout=30,
        verify_ssl=True,
        token_provider=FakeTokenProvider()
    )

    payload = {
        "title": "Complete Request",
        "price": 150
    }

    request = RequestSpec(
        method="POST",
        endpoint="/products/{product_id}",
        path_params={
            "product_id": 1
        },
        query_params={
            "source": "pytest"
        },
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=15,
        verify_ssl=False,
        authenticated=True
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        client.send(request)

        mock_request.assert_called_once_with(
            method="POST",
            url="https://fakestoreapi.com/products/1",
            params={
                "source": "pytest"
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer complete-token"
            },
            json=payload,
            timeout=15,
            verify=False
        )


# =====================================================
# Test invalid backoff factor.
# =====================================================
def test_negative_backoff_factor_is_rejected():

    with pytest.raises(ValueError):

        RequestSpec(
            method="GET",
            endpoint="/products",
            backoff_factor=-1
        )


# =====================================================
# Test zero backoff factor.
# =====================================================
def test_zero_backoff_factor_is_rejected():

    with pytest.raises(ValueError):

        RequestSpec(
            method="GET",
            endpoint="/products",
            backoff_factor=0
        )


# =====================================================
# Test invalid maximum delay.
# =====================================================
def test_negative_max_retry_delay_is_rejected():

    with pytest.raises(ValueError):

        RequestSpec(
            method="GET",
            endpoint="/products",
            max_retry_delay=-1
        )


# =====================================================
# Test actual retry scheduling
# =====================================================
def test_retry_uses_exponential_backoff():

    client = ApiClient(
        base_url="https://fakestoreapi.com"
    )

    request = RequestSpec(
        method="GET",
        endpoint="/products",
        retry_count=2,
        retry_delay=2
    )

    with patch(
        "framework.api.api_client.requests.request"
    ) as mock_request:

        mock_request.side_effect = [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            Mock(ok=True)
        ]

        with patch(
            "framework.api.api_client.time.sleep"
        ) as mock_sleep:

            client.send(request)

            assert mock_sleep.call_count == 2

            mock_sleep.assert_any_call(2)
            mock_sleep.assert_any_call(4)


# =====================================================
#
# =====================================================

# =====================================================
#
# =====================================================