import platform
import sys

import pytest


@pytest.mark.skip()
def test_a_eq_b():
    assert 'a' == 'b'


@pytest.mark.skipif(sys.platform != 'darwin', reason='Only Darwin')
def test_mac_platform():
    assert platform.mac_ver()
