import pytest


@pytest.mark.products
def test_get_products_with_headers(api_client):

    headers = {
        "Content-Type": "application/json"
    }

    response = api_client.get(
        "/products",
        headers=headers
    )

    assert response.status_code == 200