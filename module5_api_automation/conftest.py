import pytest

from framework.api.api_client import ApiClient
from framework.auth.auth_manager import AuthenticationManager
from framework.auth.token_manager import TokenManager
from framework.auth.token_provider import TokenProvider
from framework.config.environment_manager import EnvironmentManager
from framework.assertions import ResponseAssertions
from framework.assertions import SchemaValidator


@pytest.fixture(scope="session")
def config():
    return EnvironmentManager().load()


@pytest.fixture(scope="session")
def token_manager():
    return TokenManager()


@pytest.fixture(scope="session")
def token_provider(token_manager):
    return TokenProvider(token_manager)


@pytest.fixture(scope="session")
def assertions():
    return ResponseAssertions()


@pytest.fixture(scope="session")
def schema_validator():
    return SchemaValidator()


@pytest.fixture(scope="session")
def api_client(config, token_provider):

    return ApiClient(
        base_url=config["api"]["base_url"],
        timeout=config["timeouts"]["request"],
        verify_ssl=config["api"]["verify_ssl"],
        token_provider=token_provider
    )


@pytest.fixture(scope="session")
def auth_manager(api_client, config, token_manager):

    return AuthenticationManager(
        api_client=api_client,
        config=config,
        token_manager=token_manager
    )


