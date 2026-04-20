# Этот файл демонстрирует использование локального плагина.
#
# Плагин redis_fixtures.py загружается через pytest_plugins в conftest.py
# и предоставляет фикстуру redis_client (Redis в Docker через testcontainers).
#
# Запуск:
#   pytest tests/test_07_plugins.py -v
#   pytest tests/test_07_plugins.py -v --redis-version 7.0

import pytest

from core.shop.cart import Cart
from core.shop.storage import CartStorage


@pytest.fixture(autouse=True)
def cleanup_redis(redis_client):
    """Очищает Redis перед каждым тестом для изоляции."""
    redis_client.flushall()


@pytest.fixture
def storage(redis_client):
    return CartStorage(redis_client)


def test_save_and_load(storage):
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    storage.save("user:1", cart)

    loaded = storage.load("user:1")
    assert loaded.count() == 2
    assert loaded.total() == pytest.approx(2.25)


def test_load_empty(storage):
    loaded = storage.load("nonexistent")
    assert loaded.count() == 0
    assert loaded.total() == 0


def test_isolation(storage):
    """Доказывает что cleanup_redis работает — данные предыдущих тестов не видны."""
    loaded = storage.load("user:1")
    assert loaded.count() == 0
