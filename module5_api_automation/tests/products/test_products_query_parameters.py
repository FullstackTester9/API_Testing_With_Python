import pytest


# =====================================================
# Query limited number of products using query
# parameter. Here we are accessing 5 products.
# Equivalent URL is: "/products?limit=5".
# =====================================================
@pytest.mark.products
def test_get_products_with_limit(api_client):

    response = api_client.get(
        "/products",
        params={"limit": 5}
    )

    assert response.status_code == 200