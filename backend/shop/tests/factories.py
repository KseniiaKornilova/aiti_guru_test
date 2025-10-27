import factory

from shop.models import Category, Customer, Order, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    parent = None


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker("name")
    address = factory.Faker("address")
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    quantity = factory.Faker("pyint", min_value=1, max_value=100)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
