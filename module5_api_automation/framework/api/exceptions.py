# =====================================================
# "ApiClientError" -> Base framework exception.
# It allows future API-related exceptions to have a
# common parent.
# "RequestExecutionError" -> Used when the request
# cannot be executed.
# "HttpResponseError" -> Used when the request
# successfully reaches the server but the server
# responds with an unsuccessful HTTP status.
# =====================================================
class ApiClientError(Exception):
    """Base exception for API client errors."""


class RequestExecutionError(ApiClientError):
    """Raised when an HTTP request cannot be executed."""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class HttpResponseError(ApiClientError):
    """Raised when an API returns an unsuccessful HTTP status."""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response