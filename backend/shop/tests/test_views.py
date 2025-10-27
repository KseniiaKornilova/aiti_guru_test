import pytest
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import OrderItem


@pytest.mark.django_db
class TestAddProductToOrderView:

    @pytest.fixture(autouse=True)
    def set_url(self):
        self.url = "/api/shop/orders/add-product/"
        self.client = APIClient()

    def test_add_product_success(self, order, product):
        data = {"order_id": order.id, "product_id": product.id, "quantity": 5}

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["order"] == order.id
        assert response.data["product"] == product.id
        assert response.data["quantity"] == 5

        order_item = OrderItem.objects.get(order=order, product=product)
        assert order_item.quantity == 5

    def test_add_product_insufficient_quantity(self, order, product):
        data = {"order_id": order.id, "product_id": product.id, "quantity": product.quantity + 1}

        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    def test_add_same_product(self, order, product):
        data = {"order_id": order.id, "product_id": product.id, "quantity": 2}
        response_1 = self.client.post(self.url, data, format="json")
        assert response_1.data["quantity"] == 2
        response_2 = self.client.post(self.url, data, format="json")
        assert response_2.data["quantity"] == 4

        order.refresh_from_db()
        assert order.items.count() == 1
