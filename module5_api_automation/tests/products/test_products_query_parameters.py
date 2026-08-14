import pytest


@pytest.mark.products
def test_get_products_with_limit(api_client):

    response = api_client.get(
        "/products",
        params={"limit": 5}
    )

    assert response.status_code == 200