from typing import NewType

from httpx import HTTPTransport

HttpxProxies = NewType("HttpxProxies", dict[str, HTTPTransport])
