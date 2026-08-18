# =====================================================
# The "ApiClient.py" focuses on how HTTP communication
# occurs.
# "ApiClient.py" handles: Base URL, URL construction,
# GET, POST, PUT, PATCH, DELETE, Headers, JSON body,
# Query parameter, Timeout, SSL verification.
# =====================================================

import time
import requests

from framework.api.request_spec import RequestSpec
from .exceptions import (
    RequestExecutionError,
    HttpResponseError
)


class ApiClient:

    def __init__(
        self,
        base_url,
        timeout=30,
        verify_ssl=True,
        token_provider=None
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.token_provider = token_provider

    def _build_url(self, endpoint):
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    # =====================================================
    # GET = Reads data from resources.
    # =====================================================
    def get(
            self,
            endpoint,
            params=None,
            headers=None,
            authenticated=False
    ):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        final_headers = self._build_headers(
            headers=headers,
            authenticated=authenticated
        )

        return requests.get(
            url,
            params=params,
            headers=final_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

    # =====================================================
    # POST = Create or submit data on resources.
    # =====================================================
    def post(
            self,
            endpoint,
            json=None,
            params=None,
            headers=None,
            authenticated=False
    ):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        final_headers = self._build_headers(
            headers=headers,
            authenticated=authenticated
        )

        return requests.post(
            url,
            json=json,
            params=params,
            headers=final_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

    # =====================================================
    # PUT = replace or update a resource
    # =====================================================
    def put(
            self,
            endpoint,
            json=None,
            headers=None,
            authenticated=False
    ):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        final_headers = self._build_headers(
            headers=headers,
            authenticated=authenticated
        )

        return requests.put(
            url,
            json=json,
            headers=final_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

    # =====================================================
    # PATCH = partially update a resource.
    # =====================================================
    def patch(
            self,
            endpoint,
            json=None,
            headers=None,
            authenticated=False
    ):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        final_headers = self._build_headers(
            headers=headers,
            authenticated=authenticated
        )

        return requests.patch(
            url,
            json=json,
            headers=final_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

    # =====================================================
    # DELETE = delete resource permanently.
    # =====================================================
    def delete(
        self,
        endpoint,
        headers=None,
        authenticated=False
    ):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        final_headers = self._build_headers(
            headers=headers,
            authenticated=authenticated
        )

        return requests.delete(
            url,
            headers=final_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

    # =====================================================
    # The _build_headers() method is responsible for
    # building the final HTTP header. After token is
    # generated.
    # =====================================================
    def _build_headers(self, headers=None, authenticated=False):

        final_headers = {}

        if headers:
            final_headers.update(headers)

        if authenticated:

            if self.token_provider is None:
                raise RuntimeError(
                    "Authentication is required, "
                    "but AuthenticationManager is not configured."
                )

            token = self.token_provider.get_token()

            if not token:
                raise RuntimeError(
                    "Authentication is required, "
                    "but no authentication token is available."
                )

            final_headers["Authorization"] = f"Bearer {token}"

        return final_headers

    # =====================================================
    # This method now supports only GET, POST, PUT, PATCH,
    # DELETE HTTP methods and rejects everything else.
    # =====================================================
    def send(self, request_spec: RequestSpec):

        supported_methods = {
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE"
        }

        method = request_spec.method.upper()

        if method not in supported_methods:
            raise ValueError(
                f"Unsupported HTTP method: {method}"
            )

        endpoint = request_spec.resolved_endpoint()

        url = self._build_url(endpoint)

        final_headers = self._build_headers(
            headers=request_spec.headers,
            authenticated=request_spec.authenticated
        )

        timeout = (
            request_spec.timeout
            if request_spec.timeout is not None
            else self.timeout
        )

        verify_ssl = (
            request_spec.verify_ssl
            if request_spec.verify_ssl is not None
            else self.verify_ssl
        )

        # Number of total attempts.
        # Example:
        # retry_count = 0 → 1 attempt
        # retry_count = 1 → 2 attempts
        # retry_count = 2 → 3 attempts
        total_attempts = request_spec.retry_count + 1

        for attempt in range(1, total_attempts + 1):

            # =====================================================
            # Execute the actual HTTP request.
            # =====================================================
            try:

                response = requests.request(
                    method=method,
                    url=url,
                    params=request_spec.query_params,
                    headers=final_headers,
                    json=request_spec.json,
                    timeout=timeout,
                    verify=verify_ssl
                )

            # =====================================================
            # Timeout handling.
            # Retry if another attempt is available.
            # =====================================================
            except requests.exceptions.Timeout as exc:

                if (
                        self._is_retryable_method(method)
                        and attempt < total_attempts
                ):
                    self._wait_before_retry(
                        request_spec.retry_delay
                    )

                    continue

                raise RequestExecutionError(
                    (
                        f"Request timed out: "
                        f"{method} {url}"
                    ),
                    original_exception=exc
                ) from exc

            # =====================================================
            # Connection failure handling.
            # Retry if another attempt is available.
            # =====================================================
            except requests.exceptions.ConnectionError as exc:

                if (
                        self._is_retryable_method(method)
                        and attempt < total_attempts
                ):
                    self._wait_before_retry(
                        request_spec.retry_delay
                    )

                    continue

                raise RequestExecutionError(
                    (
                        f"Connection failed: "
                        f"{method} {url}"
                    ),
                    original_exception=exc
                ) from exc

            # =====================================================
            # Generic requests exception.
            # These are NOT automatically retried.
            # =====================================================
            except requests.exceptions.RequestException as exc:

                raise RequestExecutionError(
                    (
                        f"HTTP request execution failed: "
                        f"{method} {url}"
                    ),
                    original_exception=exc
                ) from exc

            # =====================================================
            # Unsuccessful HTTP response.
            # =====================================================
            if not response.ok:

                # Retry only transient HTTP statuses.
                if (
                        self._is_retryable_method(method)
                        and self._is_retryable_status(
                    response.status_code
                )
                        and attempt < total_attempts
                ):
                    self._wait_before_retry(
                        request_spec.retry_delay
                    )

                    continue

                raise HttpResponseError(
                    (
                        f"API returned unsuccessful HTTP status "
                        f"{response.status_code} for "
                        f"{method} {url}"
                    ),
                    response=response
                )

            # =====================================================
            # Successful response.
            # =====================================================
            return response

    # =====================================================
    # This is retry helper method.
    # =====================================================
    def _is_retryable_exception(self, exception):

        return isinstance(
            exception,
            (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError
            )
        )

    # =====================================================
    # Retryable HTTP status helper.
    # =====================================================
    def _is_retryable_status(self, status_code):

        return status_code in {
            502,
            503,
            504
        }

    # =====================================================
    # Retry delay helper.
    # The method makes retry timing easy to control and test.
    # =====================================================
    def _wait_before_retry(self, delay):

        if delay > 0:
            time.sleep(delay)

    # =====================================================
    # This gives the framework a centralized definition
    # of retry-safe methods.
    # =====================================================
    def _is_retryable_method(self, method):

        return method.upper() in {
            "GET",
            "PUT",
            "DELETE"
        }