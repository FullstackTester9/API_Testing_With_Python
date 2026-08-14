import requests


class ApiClient:

    def __init__(
        self,
        base_url,
        timeout=30,
        verify_ssl=True
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def _build_url(self, endpoint):
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(
        self,
        endpoint,
        params=None,
        headers=None,
        **kwargs
    ):
        return requests.get(
            self._build_url(endpoint),
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )

    def post(
        self,
        endpoint,
        json=None,
        params=None,
        headers=None,
        **kwargs
    ):
        return requests.post(
            self._build_url(endpoint),
            json=json,
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )

    def put(
        self,
        endpoint,
        json=None,
        params=None,
        headers=None,
        **kwargs
    ):
        return requests.put(
            self._build_url(endpoint),
            json=json,
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )

    def patch(
        self,
        endpoint,
        json=None,
        params=None,
        headers=None,
        **kwargs
    ):
        return requests.patch(
            self._build_url(endpoint),
            json=json,
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )

    def delete(
        self,
        endpoint,
        params=None,
        headers=None,
        **kwargs
    ):
        return requests.delete(
            self._build_url(endpoint),
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )