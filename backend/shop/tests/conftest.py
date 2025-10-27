import pytest

from .factories import CategoryFactory, OrderFactory, ProductFactory


@pytest.fixture
def product():
    appliances = CategoryFactory(name="Бытовая техника")
    laptops = CategoryFactory(name="Ноутбуки", parent=appliances)

    return ProductFactory(category=laptops)


@pytest.fixture
def order():
    return OrderFactory()
