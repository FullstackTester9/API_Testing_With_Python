# =====================================================
# This file represents complete life cycle of a token.
# No token -> login() -> Token created -> Token
# stored -> Token retrieved -> Token cleared -> No token
# =====================================================


import pytest


# =====================================================
# Tests authentication and receives token.
# =====================================================
@pytest.mark.authentication
def test_login_returns_token(auth_manager):

    token = auth_manager.login()

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

# =====================================================
# Test for retrival of token.
# =====================================================
@pytest.mark.authentication
def test_token_is_stored(auth_manager):

    token = auth_manager.login()

    stored_token = auth_manager.get_token()

    assert stored_token == token

# =====================================================
# Test for clearing the token.
# =====================================================
@pytest.mark.authentication
def test_token_can_be_cleared(auth_manager):

    auth_manager.login()

    assert auth_manager.get_token() is not None

    auth_manager.clear_token()

    assert auth_manager.get_token() is None