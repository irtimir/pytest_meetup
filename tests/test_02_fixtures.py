import typing
import pytest

from core.shop.cart import Cart


# ---------------------------------------------------------------------------
# Блок 1: Без фикстур — заметьте дублирование setup в каждом тесте
# ---------------------------------------------------------------------------

def test_total_price():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    cart.add("milk", 3.99)
    cart.add("bread", 2.49)
    assert cart.total() == pytest.approx(8.73)


def test_item_count():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    cart.add("milk", 3.99)
    cart.add("bread", 2.49)
    assert cart.count() == 4


def test_remove_item():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    cart.add("milk", 3.99)
    cart.add("bread", 2.49)
    cart.remove("banana")
    assert cart.total() == pytest.approx(7.98)
    assert cart.count() == 3


def test_remove_missing_item():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    cart.add("milk", 3.99)
    cart.add("bread", 2.49)
    with pytest.raises(ValueError):
        cart.remove("orange")


# ---------------------------------------------------------------------------
# Блок 2: Простая фикстура — setup написан один раз, инжектится везде
# ---------------------------------------------------------------------------

@pytest.fixture
def grocery_cart():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("banana", 0.75)
    cart.add("milk", 3.99)
    cart.add("bread", 2.49)
    return cart


def test_total_price_fixture(grocery_cart):
    assert grocery_cart.total() == pytest.approx(8.73)


def test_item_count_fixture(grocery_cart):
    assert grocery_cart.count() == 4


def test_remove_item_fixture(grocery_cart):
    grocery_cart.remove("banana")
    assert grocery_cart.total() == pytest.approx(7.98)
    assert grocery_cart.count() == 3


def test_remove_missing_item_fixture(grocery_cart):
    with pytest.raises(ValueError):
        grocery_cart.remove("orange")


# ---------------------------------------------------------------------------
# Блок 3: Фабрика — когда разным тестам нужен разный setup
# ---------------------------------------------------------------------------

CATALOG = [
    ("apple", 1.50),
    ("banana", 0.75),
    ("milk", 3.99),
    ("bread", 2.49),
    ("eggs", 4.99),
    ("cheese", 6.50),
]


@pytest.fixture
def cart_factory() -> typing.Callable[[int], Cart]:
    def _create_cart(num_items: int = 0) -> Cart:
        cart = Cart()
        for item, price in CATALOG[:num_items]:
            cart.add(item, price)
        return cart
    return _create_cart


def test_empty_cart(cart_factory):
    cart = cart_factory()
    assert cart.total() == 0
    assert cart.count() == 0


def test_cart_with_three_items(cart_factory):
    cart = cart_factory(num_items=3)
    assert cart.count() == 3
    assert cart.total() == pytest.approx(6.24)


def test_full_cart(cart_factory):
    cart = cart_factory(num_items=6)
    assert cart.count() == 6
    assert cart.total() == pytest.approx(20.22)


# ---------------------------------------------------------------------------
# Блок 4: Yield-фикстура — setup И teardown
# ---------------------------------------------------------------------------

import sqlite3


@pytest.fixture
def cart_db():
    # -- setup --
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE cart (item TEXT, price REAL)")
    conn.execute("INSERT INTO cart VALUES ('apple', 1.50)")
    conn.execute("INSERT INTO cart VALUES ('banana', 0.75)")
    conn.commit()
    yield conn
    # -- teardown --
    conn.close()


def test_cart_items(cart_db):
    rows = cart_db.execute("SELECT * FROM cart").fetchall()
    assert len(rows) == 2


def test_cart_total(cart_db):
    total = cart_db.execute("SELECT SUM(price) FROM cart").fetchone()[0]
    assert total == pytest.approx(2.25)
