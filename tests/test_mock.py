from unittest.mock import patch, Mock

from utils import make_request


def test_mock():
    mock_urlopen = Mock()
    mock_urlopen.read.return_value = b'91.246.162.271'
    mock_urlopen.status = 200
    with patch('urllib.request.urlopen', return_value=mock_urlopen):
        body, response = make_request('https://api.ipify.org')
        assert body == b'91.246.162.271'
        assert response.status == 200
