# =====================================================
# This is request specification layer. We want test to
# describe the "request", while the API client handles
# the execution.
# The class "RequestSpec" represents one HTTP request
# definition.
# "@dataclass" is primarily a data structure. Python
# generates constructure for us.
# The actual URL construction remains the responsibility
# of "ApiClient".
# "authenticated: bool = False" -> This allows a
# request to explicitly declare whether an
# authentication is required.
# =====================================================


from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestSpec:

    method: str
    endpoint: str

    path_params: dict[str, Any] = field(
        default_factory=dict
    )

    query_params: dict[str, Any] = field(
        default_factory=dict
    )

    headers: dict[str, Any] = field(
        default_factory=dict
    )

    json: Any = None

    timeout: int | None = None

    verify_ssl: bool | None = None

    retry_count: int = 0

    retry_delay: float = 0.0

    authenticated: bool = False

    def __post_init__(self):

        self.method = self.method.upper()

        if not self.method:
            raise ValueError(
                "HTTP method cannot be empty"
            )

        if not self.endpoint:
            raise ValueError(
                "Endpoint cannot be empty"
            )

        if self.retry_count < 0:
            raise ValueError(
                "Retry count cannot be negative"
            )

        if self.retry_delay < 0:
            raise ValueError(
                "Retry delay cannot be negative"
            )

    def resolved_endpoint(self) -> str:

        endpoint = self.endpoint

        for key, value in self.path_params.items():

            placeholder = "{" + key + "}"

            endpoint = endpoint.replace(
                placeholder,
                str(value)
            )

        if "{" in endpoint or "}" in endpoint:
            raise ValueError(
                "Unresolved path parameter in endpoint: "
                f"{endpoint}"
            )

        return endpoint