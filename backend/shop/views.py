from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AddProductToOrderSerializer,
    ErrorResponseSerializer,
    OrderItemResponseSerializer,
)


class AddProductToOrderView(APIView):
    @extend_schema(
        summary="Добавить товар в заказ",
        description="Эндпоинт принимает ID заказа, ID товара и количество, "
        "и добавляет их в заказ пользователя.",
        request=AddProductToOrderSerializer,
        responses={
            status.HTTP_201_CREATED: OrderItemResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer,
        },
    )
    def post(self, request):
        serializer = AddProductToOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order_item = serializer.save()
        except DjangoValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = OrderItemResponseSerializer(order_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
