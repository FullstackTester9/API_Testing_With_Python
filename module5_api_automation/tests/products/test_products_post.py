import pytest


# =====================================================
# Verify POST mechanism using product endpoint.
# Returns 201.
# =====================================================
@pytest.mark.products
def test_create_product(api_client):

    payload = {
        "title": "Automation Test Product",
        "price": 99.99,
        "description": "Created by API automation",
        "image": "https://example.com/product.jpg",
        "category": "electronics"
    }

    response = api_client.post(
        "/products",
        json=payload
    )

    assert response.status_code in [200, 201]