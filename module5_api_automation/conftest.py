import pytest

from framework.api.api_client import ApiClient
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