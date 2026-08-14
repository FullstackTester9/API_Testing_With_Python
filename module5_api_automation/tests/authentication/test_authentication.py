import pytest


@pytest.mark.authentication
def test_login_returns_token(auth_manager):

    token = auth_manager.login()

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

