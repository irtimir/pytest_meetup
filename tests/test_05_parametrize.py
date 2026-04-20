import pytest

from core.shop.cart import Cart


# ---------------------------------------------------------------------------
# Блок 1: Без parametrize — одинаковая структура, разные данные
# ---------------------------------------------------------------------------

def test_single_item():
    cart = Cart()
    cart.add("apple", 1.50)
    assert cart.total() == pytest.approx(1.50)


def test_two_items():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    assert cart.total() == pytest.approx(2.25)


def test_expensive_item():
    cart = Cart()
    cart.add("steak", 24.99)
    assert cart.total() == pytest.approx(24.99)


# ---------------------------------------------------------------------------
# Блок 2: parametrize — одна функция, много кейсов
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "items, expected_total",
    [
        ([("apple", 1.50)], 1.50),
        ([("apple", 1.50), ("banana", 0.75)], 2.25),
        ([("steak", 24.99)], 24.99),
        ([], 0),
    ],
)
def test_cart_total(items, expected_total):
    cart = Cart()
    for item, price in items:
        cart.add(item, price)
    assert cart.total() == pytest.approx(expected_total)


# ---------------------------------------------------------------------------
# Блок 3: pytest.param — читаемые id в выводе pytest -v
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "items, expected_total",
    [
        pytest.param([("apple", 1.50)], 1.50, id="one_item"),
        pytest.param([("apple", 1.50), ("banana", 0.75)], 2.25, id="two_items"),
        pytest.param([("steak", 24.99)], 24.99, id="expensive"),
        pytest.param([], 0, id="empty_cart"),
    ],
)
def test_cart_total_readable(items, expected_total):
    cart = Cart()
    for item, price in items:
        cart.add(item, price)
    assert cart.total() == pytest.approx(expected_total)
