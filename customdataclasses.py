from dataclasses import dataclass
from typing import Union

from pydantic import BaseModel


@dataclass
class ProjectInfo:
    project_id: str


class UserData(BaseModel):
    userid: str
    username: str
    cookies: str


class HttpConfig(BaseModel):
    sleep: float
    retry_delay: float
    retry_max_times: int
    proxy_http: str = ""
    proxy_https: str = ""


class User(BaseModel):
    uid: Union[int, str]
    project_id: Union[int, str]
    idcard_name: str


class Config(BaseModel):
    http: HttpConfig
    users: list[User]
