import os
import random
import string

import pytest

from core.shop.cart import Cart


def test_add_one_item():
    cart = Cart()
    cart.add("apple")
    assert cart.total() == 1

def test_add_two_items():
    cart = Cart()
    cart.add("apple")
    cart.add("banana")
    assert cart.total() == 2


@pytest.fixture
def empty_cart():
    return Cart()

def test_add_one_item_fixture(empty_cart):
    empty_cart.add("apple")
    assert empty_cart.total() == 1

def test_add_two_items_fixture(empty_cart):
    empty_cart.add("apple")
    empty_cart.add("banana")
    assert empty_cart.total() == 2


@pytest.fixture
def cart_factory():
    def _create_cart_with_items(num_items = 0):
        cart = Cart()
        for _ in range(num_items):
            item = ''.join(random.choices(string.ascii_lowercase, k=5))
            cart.add(item)
        return cart
    return _create_cart_with_items


def test_empty_cart(cart_factory):
    cart = cart_factory()
    assert cart.total() == 0

def test_cart_with_items(cart_factory):
    user = cart_factory(num_items=5)
    assert user.total() == 5
