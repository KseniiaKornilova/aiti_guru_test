from django.core.management.base import BaseCommand

from shop.models import Category, Customer, Order, Product


class Command(BaseCommand):
    help = "Заполняет базу данных показательными данными."

    def handle(self, *args, **options):
        categories_data = [
            {"name": "Бытовая техника"},
            {"name": "Стиральные машины", "parent": "Бытовая техника"},
            {"name": "Холодильники", "parent": "Бытовая техника"},
            {"name": "Однокамерные", "parent": "Холодильники"},
            {"name": "Двухкамерные", "parent": "Холодильники"},
            {"name": "Телевизоры", "parent": "Бытовая техника"},
            {"name": "Компьютеры"},
            {"name": "Ноутбуки", "parent": "Компьютеры"},
            {"name": "Моноблоки", "parent": "Компьютеры"},
            {"name": '17"', "parent": "Ноутбуки"},
            {"name": '19"', "parent": "Ноутбуки"},
        ]
        for category in categories_data:
            parent_name = category.get("parent")
            parent = None
            if parent_name:
                parent, _ = Category.objects.get_or_create(name=parent_name)
            Category.objects.get_or_create(name=category["name"], parent=parent)

        products_data = [
            {
                "name": "Apple MacBook Pro M3",
                "category": Category.objects.get(name='19"'),
                "price": 249999,
                "quantity": 50,
            },
            {
                "name": "Apple MacBook Air",
                "category": Category.objects.get(name='17"'),
                "price": 180000,
                "quantity": 30,
            },
            {
                "name": "Телевизор Samsung",
                "category": Category.objects.get(name="Телевизоры"),
                "price": 68000,
                "quantity": 100,
            },
            {
                "name": "Холодильник Bosh",
                "category": Category.objects.get(name="Холодильники"),
                "price": 83000,
                "quantity": 75,
            },
        ]

        for product in products_data:
            Product.objects.get_or_create(
                name=product["name"],
                category=product["category"],
                defaults={
                    "price": product["price"],
                    "quantity": product["quantity"],
                },
            )

        customers_data = [
            {"name": "Иван Иванов", "address": "Москва, Покровка 16"},
            {"name": "Петр Петров", "address": "Санкт-Петербург, Часовая 142"},
        ]

        for customer in customers_data:
            client, _ = Customer.objects.get_or_create(
                name=customer["name"],
                defaults={"address": customer["address"]},
            )
            Order.objects.get_or_create(
                customer=client,
            )

        self.stdout.write(self.style.SUCCESS("База успешно заполнена данными."))
