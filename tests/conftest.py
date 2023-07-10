import sys

import pytest

if sys.version_info[0] > 2:
    collect_ignore = ['test_py2.py']

pytest_plugins = ['redis_fixtures']


@pytest.fixture
def shared_fixture():
    return 'value'


def pytest_addoption(parser):
    parser.addoption('--run-slow', action='store_true', default=False)


def pytest_runtest_setup(item):
    if not item.config.getoption('--run-slow') and 'slow' in item.keywords:
        pytest.skip('Skipping slow tests')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'slow: marks tests as slow',
    )
