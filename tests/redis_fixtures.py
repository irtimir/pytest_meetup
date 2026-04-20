# Локальный плагин — загружается через pytest_plugins в conftest.py.
# Предоставляет фикстуру redis_client и CLI-опцию --redis-version.

import pytest
from pytest import Metafunc
from testcontainers.redis import RedisContainer


# Хук: динамическая параметризация — позволяет задать версии Redis через CLI
def pytest_generate_tests(metafunc: Metafunc):
    if 'redis_version' in metafunc.fixturenames:
        redis_versions = {'latest'}
        redis_versions.update(metafunc.config.getoption('--redis-version'))
        metafunc.parametrize('redis_version', sorted(redis_versions), scope='session')


# Хук: регистрация CLI-опции --redis-version
def pytest_addoption(parser):
    parser.addoption('--redis-version', action='append', default=[])


# Session-scoped фикстура: один контейнер на всю сессию тестов
# yield обеспечивает teardown — контейнер останавливается после всех тестов
@pytest.fixture(scope='session')
def redis_client(redis_version):
    db = RedisContainer(f'redis:{redis_version}')
    db.start()
    yield db.get_client(decode_responses=True)
    db.stop()
