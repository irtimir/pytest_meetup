# Тесты Django-моделей с pytest-django.
#
# Каждый тест помечен @pytest.mark.django_db — без этого
# pytest-django не даст доступ к базе данных.
#
# Инфраструктура (PostgreSQL в Docker) настроена в conftest.py.

import pytest

from core.models import Product, Order
from core.utils import get_customer_orders
from tests.test_django.factories import UserFactory, ProductFactory, OrderFactory


# ---------------------------------------------------------------------------
# Блок 1: Встроенные фикстуры pytest-django
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_create_user(django_user_model):
    """django_user_model — встроенная фикстура, возвращает модель User."""
    customer = django_user_model.objects.create(username='alice')
    assert not customer.is_superuser


# ---------------------------------------------------------------------------
# Блок 2: Factory Boy — генерация тестовых данных
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_product_factory():
    product = ProductFactory()
    assert Product.objects.count() == 1
    assert product.price > 0


@pytest.mark.django_db
def test_order_factory():
    order = OrderFactory()
    assert Order.objects.count() == 1
    assert order.customer is not None


@pytest.mark.django_db
def test_order_with_products():
    order = OrderFactory()
    product1 = ProductFactory(name="apple", price=1.50)
    product2 = ProductFactory(name="banana", price=0.75)
    order.products.add(product1, product2)
    assert order.products.count() == 2


@pytest.mark.django_db
def test_user_fixture(user):
    """user — кастомная фикстура из conftest.py, использует UserFactory."""
    assert not user.is_superuser


@pytest.mark.django_db
def test_superuser_fixture(superuser):
    assert superuser.is_superuser


# ---------------------------------------------------------------------------
# Блок 3: django_assert_num_queries — контроль N+1
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_no_n_plus_1(django_assert_num_queries):
    """django_assert_num_queries — проверяет количество SQL-запросов."""
    for _ in range(10):
        customer = UserFactory()
        order = OrderFactory(customer=customer)
        order.products.add(ProductFactory(), ProductFactory())

    with django_assert_num_queries(3):
        get_customer_orders()
