import time

import pytest


@pytest.mark.slow
def test_slow_test():
    time.sleep(10)
