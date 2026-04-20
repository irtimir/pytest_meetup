# Этот файл демонстрирует кастомные маркеры
# и pytest-хуки, которые их обрабатывают.
#
# Хуки определены в conftest.py:
#   pytest_configure    — регистрация маркера 'slow'
#   pytest_addoption    — CLI флаг --run-slow
#   pytest_runtest_setup — пропуск slow тестов без флага
#
# Запуск:
#   pytest tests/test_06_hooks.py -v            → test_slow SKIPPED
#   pytest tests/test_06_hooks.py -v --run-slow  → test_slow PASSED

import time

import pytest

from core.shop.cart import Cart


def test_fast():
    cart = Cart()
    cart.add("apple", 1.50)
    assert cart.total() == pytest.approx(1.50)


@pytest.mark.slow
def test_slow():
    time.sleep(2)
    cart = Cart()
    for i in range(1000):
        cart.add(f"item_{i}", 0.01)
    assert cart.total() == pytest.approx(10.0)
