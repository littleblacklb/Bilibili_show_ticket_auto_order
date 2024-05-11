import random
from dataclasses import dataclass
from typing import Union, Optional

from pydantic import BaseModel

from consts import AuthType


def get_deviceid(separator: str = "-", is_lowercase: bool = False) -> str:
    """
    获取随机 deviceid (dev_id)

    Args:
        separator (str)  : 分隔符 默认为 "-"

        is_lowercase (bool) : 是否以小写形式 默认为False

    参考: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/message/private_msg.md#发送私信web端

    Returns:
        str: device_id
    """

    def join(seperator: str, array: list):
        """
        用指定字符连接数组

        Args:
            seperator (str) : 分隔字符

            array     (list): 数组

        Returns:
            str: 连接结果
        """
        return seperator.join(map(lambda x: str(x), array))

    template = ["xxxxxxxx", "xxxx", "4xxx", "yxxx", "xxxxxxxxxxxx"]
    dev_id_group = []
    for i in range(len(template)):
        s = ""
        group = template[i]
        for k in group:
            rand: int = int(16 * random.random())
            if k in "xy":
                if k == "x":
                    s += hex(rand)[2:]
                else:
                    s += hex(3 & rand | 8)[2:]
            else:
                s += "4"
        dev_id_group.append(s)
    res = join(separator, dev_id_group)
    return res if is_lowercase else res.upper()


@dataclass
class ProjectInfo:
    project_id: str


class DataUser(BaseModel):
    """
    User data in user_data.json
    """
    userid: str
    username: str
    cookies: str


class HttpConfig(BaseModel):
    sleep: float = 1.7
    retry_delay: float = 1.0
    retry_max_times: int = 3
    proxy_http: str = ""
    proxy_https: str = ""


class DeliverInfo(BaseModel):
    name: str = ""
    tel: str = ""
    addr_id: str = ""
    addr: str = ""


class PayloadUniversal(BaseModel):
    count: int = -1
    deviceId: str = get_deviceid()
    order_type: int = 1
    pay_money: int = -1
    project_id: int = -1
    screen_id: int = -1
    sku_id: int = -1
    timestamp: int = -1
    token: str = ""
    deliver_info: Optional[DeliverInfo] = None


class PayloadWithAuth(BaseModel):
    buyer_info: list[dict] = []


class PayloadWithoutAuth(BaseModel):
    name: str = ""
    tel: str = ""


class Project(BaseModel):
    auth_type: AuthType = AuthType.NO_AUTH
    # Complex, thus ignore details
    buyers: list[dict] = []
    payload_universal: PayloadUniversal = PayloadUniversal()
    payload_with_auth: Optional[PayloadWithAuth] = PayloadWithAuth()
    payload_without_auth: Optional[PayloadWithoutAuth] = PayloadWithoutAuth()


class ConfigUser(BaseModel):
    """
    User data in config.json
    """
    uid: Union[int, str]
    project: Project = Project()


class Config(BaseModel):
    http: HttpConfig = HttpConfig()
    users: list[ConfigUser] = []
