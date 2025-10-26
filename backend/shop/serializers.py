from rest_framework import serializers

from .models import Order, OrderItem, Product
from .services import ProductAddService


class AddProductToOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_order_id(self, value):
        try:
            order = Order.objects.get(id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Заказ не найден")
        self._order = order
        return value

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден")
        self._product = product
        return value

    def save(self):
        order = self._order
        product = self._product
        quantity = self.validated_data["quantity"]

        return ProductAddService.add_product(order, product, quantity)


class OrderItemResponseSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price"]
        read_only_fields = ["id", "order", "product", "price"]


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
