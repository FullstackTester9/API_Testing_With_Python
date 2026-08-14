import pytest


# ==============================================================
# Authenticated Request Test
# ==============================================================
@pytest.mark.authentication
def test_authenticated_request_uses_token(
    auth_manager,
    api_client
):

    token = auth_manager.login()

    assert token is not None

    response = api_client.get(
        "/products/1",
        authenticated=True
    )

    assert response.status_code == 200


# ==============================================================
# Test Without Authentication
# ==============================================================
@pytest.mark.authentication
def test_request_without_authentication(
    api_client
):

    response = api_client.get(
        "/products/1"
    )

    assert response.status_code == 200


# ==============================================================
# Test Missing Token
# ==============================================================
@pytest.mark.authentication
def test_authenticated_request_without_token(
    api_client,
    token_manager
):

    token_manager.clear_token()

    with pytest.raises(RuntimeError, match="no authentication token"):
        api_client.get(
            "/products/1",
            authenticated=True
        )