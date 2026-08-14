import pytest

from framework.api.api_client import ApiClient
from framework.auth.auth_manager import AuthenticationManager
from framework.config.environment_manager import EnvironmentManager


@pytest.fixture(scope="session")
def config():
    return EnvironmentManager().load()


@pytest.fixture(scope="session")
def api_client(config):
    return ApiClient(
        base_url=config["api"]["base_url"],
        timeout=config["timeouts"]["request"],
        verify_ssl=config["api"]["verify_ssl"]
    )


@pytest.fixture(scope="session")
def auth_manager(api_client, config):
    return AuthenticationManager(
        api_client=api_client,
        config=config
    )


