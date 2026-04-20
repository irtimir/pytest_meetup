import sys

import pytest

from core.shop.cart import Cart


# ---------------------------------------------------------------------------
# skip — безусловный пропуск
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="пример пропущенного теста")
def test_skipped():
    assert 1 == 2


# ---------------------------------------------------------------------------
# skipif — условный пропуск
# ---------------------------------------------------------------------------

@pytest.mark.skipif(sys.platform != "darwin", reason="Only macOS")
def test_mac_only():
    assert sys.platform == "darwin"


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Requires Python 3.12+")
def test_python_312_feature():
    assert sys.version_info >= (3, 12)


# ---------------------------------------------------------------------------
# xfail — ожидаемое падение (документация известного бага)
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="known bug: remove удаляет только первый дубликат")
def test_remove_all_duplicates():
    cart = Cart()
    cart.add("apple", 1.50)
    cart.add("apple", 1.50)
    cart.remove("apple")
    # remove удаляет только первый, а хотим все
    assert cart.count() == 0


@pytest.mark.xfail(strict=True)
def test_strict_xfail():
    # strict: если тест вдруг пройдёт — это XPASS и pytest пометит FAIL
    assert 1 == 2


# ---------------------------------------------------------------------------
# usefixtures — применяет фикстуру без передачи в аргументы
# ---------------------------------------------------------------------------

@pytest.fixture
def populate_cart(cart_state):
    cart_state.append(("apple", 1.50))
    cart_state.append(("banana", 0.75))


@pytest.fixture
def cart_state():
    return []


@pytest.mark.usefixtures("populate_cart")
class TestCartWithUsefixtures:
    def test_has_items(self, cart_state):
        assert len(cart_state) == 2

    def test_first_item(self, cart_state):
        assert cart_state[0] == ("apple", 1.50)
