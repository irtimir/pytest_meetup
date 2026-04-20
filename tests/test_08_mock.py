# Подмена зависимостей без Docker — тестируем CartStorage
# с фейковым Redis-клиентом.
#
# Контраст с test_07_plugins.py:
#   там — интеграционные тесты с реальным Redis
#   здесь — unit-тесты с подменённым клиентом

from unittest.mock import MagicMock

import pytest

from core.shop.cart import Cart
from core.shop.storage import CartStorage


# ---------------------------------------------------------------------------
# Блок 1: Stub-объект — простейшая подмена
# ---------------------------------------------------------------------------

class FakeRedisClient:
    """Имитация Redis-клиента: хранит данные в обычном dict."""

    def __init__(self):
        self.data = {}

    def hset(self, key, mapping):
        self.data[key] = mapping

    def hgetall(self, key):
        return self.data.get(key, {})


def test_save_and_load_with_stub():
    storage = CartStorage(FakeRedisClient())
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    storage.save("user:1", cart)

    loaded = storage.load("user:1")
    assert loaded.count() == 2
    assert loaded.total() == pytest.approx(2.25)


# ---------------------------------------------------------------------------
# Блок 2: monkeypatch — подмена методов на существующем объекте
# ---------------------------------------------------------------------------

def test_load_with_monkeypatch(monkeypatch):
    client = FakeRedisClient()
    storage = CartStorage(client)

    # monkeypatch подменяет hgetall чтобы вернуть нужные данные
    monkeypatch.setattr(client, "hgetall", lambda key: {"milk": "3.99"})

    cart = storage.load("any_id")
    assert cart.count() == 1
    assert cart.total() == pytest.approx(3.99)


def test_save_failure_with_monkeypatch(monkeypatch):
    client = FakeRedisClient()
    storage = CartStorage(client)

    # monkeypatch подменяет hset чтобы он выбрасывал ошибку
    def failing_hset(key, mapping):
        raise ConnectionError("Redis unavailable")

    monkeypatch.setattr(client, "hset", failing_hset)

    cart = Cart()
    cart.add("apple", 1.50)
    with pytest.raises(ConnectionError):
        storage.save("user:1", cart)


# ---------------------------------------------------------------------------
# Блок 3: MagicMock — автоматически создаёт любые методы и атрибуты
# ---------------------------------------------------------------------------

def test_save_with_magicmock():
    # MagicMock не требует определения методов — он "соглашается" на всё
    mock_client = MagicMock()
    storage = CartStorage(mock_client)

    cart = Cart()
    cart.add("apple", 1.50)
    storage.save("user:1", cart)

    # Можно проверить чем был вызван метод
    mock_client.hset.assert_called_once_with(
        "cart:user:1", mapping={"apple": 1.50}
    )


def test_load_with_magicmock():
    mock_client = MagicMock()
    # Настраиваем return_value для конкретного метода
    mock_client.hgetall.return_value = {"banana": "0.75"}

    storage = CartStorage(mock_client)
    cart = storage.load("user:1")

    assert cart.count() == 1
    assert cart.total() == pytest.approx(0.75)
    mock_client.hgetall.assert_called_once_with("cart:user:1")
