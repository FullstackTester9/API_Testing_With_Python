# =====================================================
# The purpose of "conftest.py" is to share fixtures,
# plugins and configurations across multiple tests files
# without importing them.
# It acts as a centralized setup for test suit.
# =====================================================


import pytest

from framework.api.api_client import ApiClient
from framework.auth.auth_manager import AuthenticationManager
from framework.auth.token_manager import TokenManager
from framework.auth.token_provider import TokenProvider
from framework.config.environment_manager import EnvironmentManager
from framework.assertions import ResponseAssertions
from framework.assertions import SchemaValidator
from test_data.test_data import VALID_PRODUCT_DATA
from framework.payloads import build_product_payload


# =====================================================
# The configuration is loaded once per test session
# because scope="session".
# =====================================================
@pytest.fixture(scope="session")
def config():
    return EnvironmentManager().load()


# =====================================================
# Token manager fixture. Handles authentication and
# token provider. They depend on token_manager().
# =====================================================
@pytest.fixture(scope="session")
def token_manager():
    return TokenManager()


# =====================================================
# Dependent on "token_manager()". Gets token from
# "token_manager()" the "ApiClient" can receive it.
# =====================================================
@pytest.fixture(scope="session")
def token_provider(token_manager):
    return TokenProvider(token_manager)


# =====================================================
# Assertion fixture
# =====================================================
@pytest.fixture(scope="session")
def assertions():
    return ResponseAssertions()


# =====================================================
# Validates JSON schema.
# =====================================================
@pytest.fixture(scope="session")
def schema_validator():
    return SchemaValidator()


# =====================================================
# Test data fixture
# =====================================================
@pytest.fixture(scope="session")
def valid_product_data():
    return VALID_PRODUCT_DATA.copy()


# =====================================================
# Receives token from "token_provider()".
# =====================================================
@pytest.fixture(scope="session")
def api_client(config, token_provider):

    return ApiClient(
        base_url=config["api"]["base_url"],
        timeout=config["timeouts"]["request"],
        verify_ssl=config["api"]["verify_ssl"],
        token_provider=token_provider
    )


# =====================================================
# Authentication fixture. It authenticates the entire
# process with token.
# =====================================================
@pytest.fixture(scope="session")
def auth_manager(api_client, config, token_manager):

    return AuthenticationManager(
        api_client=api_client,
        config=config,
        token_manager=token_manager
    )


# =====================================================
# Payload fixture. Tests can simply request
# "valid_product_payload" instead of reconstructing
# payload every time.
# =====================================================
@pytest.fixture
def valid_product_payload(valid_product_data):

    return build_product_payload(
        title=valid_product_data["title"],
        price=valid_product_data["price"],
        description=valid_product_data["description"],
        category=valid_product_data["category"],
        image=valid_product_data["image"]
    )