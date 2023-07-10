import urllib.request
from urllib.request import Request


def make_request(url, headers=None, data=None):
    request = Request(url, headers=headers or {}, data=data)
    response = urllib.request.urlopen(request)
    return response.read(), response
