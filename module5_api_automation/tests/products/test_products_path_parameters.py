import pytest


# =====================================================
# Access products with product id.
# =====================================================
@pytest.mark.products
def test_get_product_by_id(api_client):

    product_id = 1

    response = api_client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == product_id