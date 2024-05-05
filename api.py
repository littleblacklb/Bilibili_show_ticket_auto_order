from enum import Enum, auto

import httpx

import utils
from customtypes import HttpxProxies


class AuthType(Enum):
    """
    项目实名认证规则
    """
    NO_AUTH = auto()
    AUTH_PER_ORDER = auto()
    AUTH_PER_PERSON = auto()


def load_proxies(http: str, https: str = "") -> HttpxProxies:
    return HttpxProxies({
        "http://": httpx.HTTPTransport(proxy=http),
        "https://": httpx.HTTPTransport(proxy=https if https else http),
    })


class Api:
    def __init__(self, username: str, sleepTime: float, proxies: HttpxProxies):
        self.client = httpx.AsyncClient(proxies=proxies)
        self.user_data = utils.DbUserData.get_user_data(username)
