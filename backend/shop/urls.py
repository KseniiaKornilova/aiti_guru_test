from django.urls import path

from .views import AddProductToOrderView

urlpatterns = [
    path("orders/add-product/", AddProductToOrderView.as_view(), name="add-product-to-order")
]
