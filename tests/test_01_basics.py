import pytest


# --- Что является тестом? ---

# pytest НЕ найдёт: нет префикса test_
def check_sum():
    assert 2 + 2 == 4


# pytest НЕ найдёт: класс без префикса Test
class CheckMath:
    def test_sum(self):
        assert 2 + 2 == 4


# pytest найдёт: класс с Test + метод с test_
class TestMath:
    def test_sum(self):
        assert 2 + 2 == 4

    # pytest НЕ найдёт: нет префикса test_
    def helper(self):
        return 42


# --- Сравнение значений ---

def test_sum():
    assert 2 + 2 == 4


def test_string_equality():
    greeting = "hello world"
    assert greeting == "hello world"


# --- Проверка вхождения ---

def test_substring():
    assert "hello" in "hello world"


def test_list_membership():
    colors = ["red", "green", "blue"]
    assert "green" in colors


# --- Сравнение коллекций ---

def test_set_comparison():
    expected = {"apple", "banana", "cherry"}
    actual = {"apple", "banana", "cherry"}
    assert actual == expected


def test_list_equality():
    expected = [1, 2, 3]
    actual = sorted([3, 1, 2])
    assert actual == expected


# --- Исключения ---

def test_raises():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")
