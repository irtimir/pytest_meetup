import pytest

from core.shop.cart import Cart


# ---------------------------------------------------------------------------
# Блок 1: scope="function" (по умолчанию) — новая фикстура на каждый тест
# ---------------------------------------------------------------------------

@pytest.fixture
def cart():
    print("\n  CREATING function-scoped cart")
    c = Cart()
    c.add("apple", 1.50)
    c.add("banana", 0.75)
    yield c
    print("  DESTROYING function-scoped cart")


def test_function_scope_add(cart):
    cart.add("milk", 3.99)
    assert cart.count() == 3


def test_function_scope_remove(cart):
    cart.remove("apple")
    assert cart.count() == 1


# ---------------------------------------------------------------------------
# Блок 2: scope="module" — одна фикстура на весь файл
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def catalog():
    print("\n  CREATING module-scoped catalog")
    items = [
        ("apple", 1.50),
        ("banana", 0.75),
        ("milk", 3.99),
        ("bread", 2.49),
    ]
    yield items
    print("  DESTROYING module-scoped catalog")


def test_catalog_has_items(catalog):
    assert len(catalog) == 4


def test_catalog_prices(catalog):
    total = sum(price for _, price in catalog)
    assert total == pytest.approx(8.73)
