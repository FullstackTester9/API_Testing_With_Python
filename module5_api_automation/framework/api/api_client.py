# =====================================================
# The "ApiClient.py" focuses on how HTTP communication
# occurs.
# "ApiClient.py" handles: Base URL, URL construction,
# GET, POST, PUT, PATCH, DELETE, Headers, JSON body,
# Query parameter, Timeout, SSL verification.
# =====================================================

import requests


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
