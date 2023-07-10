import os
import random
import string

import pytest


def test_bad():
    rnd_string = ''.join(random.choices(string.ascii_lowercase, k=100))
    c_string = rnd_string.capitalize()
    assert isinstance(c_string, str)
    assert len(c_string) == 100
    assert c_string[0].isupper()


@pytest.fixture
def some_string():
    return 'value'


def test_string(some_string):
    assert some_string == 'value'


@pytest.fixture
def rnd_string():
    return ''.join(random.choices(string.ascii_lowercase, k=100))


def test_rnd_string(rnd_string):
    c_string = rnd_string.capitalize()
    assert isinstance(c_string, str)
    assert len(c_string) == 100
    assert c_string[0].isupper()


@pytest.fixture
def ascii_and_digits():
    return string.ascii_letters + string.digits


@pytest.fixture
def rnd_string_1(ascii_and_digits):
    return ''.join(random.choices(ascii_and_digits, k=100))


@pytest.fixture
def rnd_string_factory():
    def factory(symbols, n=100):
        return ''.join(random.choices(symbols, k=n))

    return factory


def test_rnd_string_factory(rnd_string_factory):
    value = rnd_string_factory(symbols='qwerty1234', n=10)
    assert len(value) == 10


@pytest.fixture
def temp_file():
    file_path = '/tmp/pytest_temp_file'
    f = open(file_path, 'w')
    yield f
    f.close()
    os.remove(file_path)


@pytest.fixture
def temp_file_factory():
    f, f_path = None, None

    def factory(file_path):
        nonlocal f, f_path
        f, f_path = open(file_path, 'w'), file_path
        return f

    yield factory

    if f_path is not None and f is not None:
        f.close()
        os.remove(f_path)


def test_temp_file_factory(temp_file_factory):
    f = temp_file_factory('temp_file_name')
    f.write('some text')
