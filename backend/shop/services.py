from django.core.exceptions import ValidationError

from .models import Order, OrderItem, Product


class ProductAddService:
    @staticmethod
    def add_product(order: Order, product: Product, quantity: int) -> OrderItem:
        if product.quantity < quantity:
            raise ValidationError("Недостаточно товара на складе")

        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product, defaults={"quantity": 0, "price": product.price}
        )

        order_item.quantity += quantity
        order_item.save()

        return order_item
