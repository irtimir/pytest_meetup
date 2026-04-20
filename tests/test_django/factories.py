# Factory Boy — генерация тестовых данных для Django-моделей.
# Альтернатива ручному Model.objects.create() в каждом тесте.

import factory.fuzzy
from django.contrib.auth import get_user_model

from core.models import Product, Order


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.faker.Faker('bothify', text='customer-###???')
    email = factory.LazyAttribute(lambda x: f'{x.username}@example.com')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.fuzzy.FuzzyChoice(['apple', 'banana', 'milk', 'bread', 'eggs'])
    price = factory.fuzzy.FuzzyDecimal(0.50, 50.00, precision=2)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
