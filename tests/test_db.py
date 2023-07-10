import pytest


@pytest.fixture(autouse=True)
def cleanup_redis(redis_client):
    redis_client.flushall()


def test_get_set(redis_client):
    assert redis_client.set('a', '1') is True
    assert redis_client.get('a') == '1'
