import pytest
from pytest import Metafunc
from testcontainers.redis import RedisContainer


def pytest_generate_tests(metafunc: Metafunc):
    if 'redis_version' in metafunc.fixturenames:
        redis_versions = {'latest'}
        redis_versions.update(metafunc.config.getoption('--redis-version'))
        metafunc.parametrize('redis_version', sorted(redis_versions), scope='session')


def pytest_addoption(parser):
    parser.addoption('--redis-version', action='append', default=[])


@pytest.fixture(scope='session')
def redis_client(redis_version):
    db = RedisContainer(f'redis:{redis_version}')
    db.start()
    yield db.get_client(decode_responses=True)
    db.stop()
