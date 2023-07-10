import pytest


def test_contain():
    assert 'I' in 'Ilias'


def test_raise():
    with pytest.raises(KeyError):
        {}.pop(None)
