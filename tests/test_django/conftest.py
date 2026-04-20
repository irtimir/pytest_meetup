# conftest.py для Django-тестов.
#
# Поднимает PostgreSQL в Docker через testcontainers
# и настраивает Django на использование этой БД.

import pytest
from django.conf import settings
from django.db.utils import ConnectionHandler
from psycopg2 import OperationalError
from pytest_django.lazy_django import skip_if_no_django
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.postgres import PostgresContainer

from tests.test_django.factories import UserFactory


# Кастомный контейнер: расширяет PostgresContainer
# чтобы корректно работать с django_db_blocker
class PostgresContainerDjango(PostgresContainer):
    def __init__(self, db_blocker, *args, **kwargs):
        self.db_blocker = db_blocker
        super().__init__(*args, **kwargs)

    @wait_container_is_ready(*[OperationalError])
    def _connect(self):
        with self.db_blocker.unblock():
            ConnectionHandler({
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': self.POSTGRES_DB,
                    'USER': self.POSTGRES_USER,
                    'PASSWORD': self.POSTGRES_DB,
                    'HOST': self.get_container_host_ip(),
                    'PORT': self.get_exposed_port(self.port_to_expose),
                },
            }).create_connection('default').connect()


# Session-scoped фикстура: один контейнер PostgreSQL на всю сессию.
# autouse=True — применяется ко всем тестам в этой директории.
@pytest.fixture(scope='session', autouse=True)
def postgres_container(django_db_blocker):
    skip_if_no_django()
    db = PostgresContainerDjango(django_db_blocker)
    db.start()

    # Настраиваем Django на использование контейнерной БД
    settings.DATABASES['default']['NAME'] = db.POSTGRES_DB
    settings.DATABASES['default']['USER'] = db.POSTGRES_USER
    settings.DATABASES['default']['PASSWORD'] = db.POSTGRES_PASSWORD
    settings.DATABASES['default']['HOST'] = db.get_container_host_ip()
    settings.DATABASES['default']['PORT'] = db.get_exposed_port(db.port_to_expose)

    yield db
    db.stop()


# Кастомные фикстуры для удобства — используют UserFactory
@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def superuser():
    return UserFactory(is_superuser=True)
