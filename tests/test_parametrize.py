import pytest


def test_sort_same_list():
    assert sorted((1, 1, 1)) == [1, 1, 1]


def test_sort_positive():
    assert sorted((6, 5, 8)) == [5, 6, 8]


def test_sort_positive_negative_mix():
    assert sorted((11, 0, -1)) == [-1, 0, 11]


def test_letters():
    assert sorted(('a', 'z', 'b')) == ['a', 'b', 'z']


@pytest.mark.parametrize(
    ['values', 'expected'],
    [
        ((1, 1, 1), [1, 1, 1]),
        ((6, 5, 8), [5, 6, 8]),
        ((11, 0, -1), [-1, 0, 11]),
        (('a', 'z', 'b'), ['a', 'b', 'z']),
    ],
)
def test_sort(values, expected):
    assert sorted(values) == expected
