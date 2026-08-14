import pytest


@pytest.mark.smoke
@pytest.mark.products
def test_get_products(api_client):

    response = api_client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0