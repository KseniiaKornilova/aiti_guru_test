import pytest
from django.core.exceptions import ValidationError

from shop.models import OrderItem
from shop.services import ProductAddService


@pytest.mark.django_db
class TestProductAddService:
    def test_add_new_product_creates_order_item(self, order, product):
        order_item = ProductAddService.add_product(order, product, quantity=3)
        assert order_item.order == order
        assert order_item.product == product
        assert order_item.quantity == 3

    def test_add_existing_product_increments_quantity(self, order, product):
        existing_order_item = OrderItem.objects.create(
            order=order, product=product, quantity=2, price=product.price
        )
        order_item = ProductAddService.add_product(order, product, quantity=3)
        assert order_item.id == existing_order_item.id
        assert order_item.quantity == 5

    def test_add_product_insufficient_stock_error(self, order, product):
        with pytest.raises(ValidationError):
            ProductAddService.add_product(order, product, quantity=product.quantity + 3)
