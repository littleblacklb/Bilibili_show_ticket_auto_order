from dataclasses import dataclass
from typing import Union

from pydantic import BaseModel

from consts import AuthType


@dataclass
class ProjectInfo:
    project_id: str


class DataUser(BaseModel):
    """
    User data in user_data.json
    """
    userid: Union[str, int]
    username: str
    cookies: str


class HttpConfig(BaseModel):
    sleep: float
    retry_delay: float
    retry_max_times: int
    proxy_http: str = ""
    proxy_https: str = ""


class DeliverInfo(BaseModel):
    needed: bool = False
    name: str = ""
    tel: str = ""
    addr_id: str = ""
    addr: str = ""


class Ticket(BaseModel):
    screen_id: int
    sku_id: int
    pay_money: int
    deliver_info: DeliverInfo


class Project(BaseModel):
    project_id: Union[int, str]
    auth_type: AuthType = AuthType.NO_AUTH
    ticket: Ticket


class ConfigUser(BaseModel):
    """
    User data in config.json
    """
    uid: Union[int, str]
    project: Project
    idcard_name: str = ""


class Config(BaseModel):
    http: HttpConfig
    users: list[ConfigUser]
