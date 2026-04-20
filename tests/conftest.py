import sys

import pytest

# collect_ignore — список файлов, которые pytest пропустит при сборе тестов.
# test_py2.py содержит синтаксис Python 2 (print 1) — без этого pytest упадёт
# с SyntaxError ещё до запуска тестов.
if sys.version_info[0] > 2:
    collect_ignore = ['test_py2.py']

# Загрузка локального плагина redis_fixtures.py
pytest_plugins = ['redis_fixtures']



def pytest_addoption(parser):
    parser.addoption('--run-slow', action='store_true', default=False)


def pytest_runtest_setup(item):
    if not item.config.getoption('--run-slow') and 'slow' in item.keywords:
        pytest.skip('Skipping slow tests')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'slow: marks tests as slow',
    )
