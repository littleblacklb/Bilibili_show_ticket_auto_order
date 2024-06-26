import asyncio
import json
import os
import sys
from functools import wraps
from inspect import iscoroutinefunction
from json import JSONDecodeError
from typing import Any, Union

import httpx
from httpx import Cookies
from loguru import logger
from pydantic import ValidationError

from customdataclasses import DataUser, Config, ConfigUser

from ResponseCodeException import ResponseCodeException
from consts import Urls
from customtypes import HttpxProxies

# The config.json normally is stored in the same folder of the utils.py
_config, SRC_PATH = None, os.path.join(os.path.dirname(os.path.abspath(__file__)), "./config.json")


class DbUserData:
    _data: dict = None

    @staticmethod
    def get_all_users_data():
        if DbUserData._data:
            return DbUserData._data
        with open("users_data.json", "r") as f:
            try:
                DbUserData._data = json.load(f)
            except json.JSONDecodeError:
                logger.error("Oops! 错误的JSON结构，请删除 users_data.json 并且重新登录后重试")
                sys.exit(-1)
            logger.success("读取 users_data.json 成功!")
            return DbUserData._data

    @staticmethod
    def get_available_users() -> list[str]:
        data = DbUserData.get_all_users_data()
        return list(data.keys())

    @staticmethod
    def get_user_data(username: str) -> DataUser:
        user = DbUserData.get_all_users_data()[username]
        return DataUser(
            userid=user["userid"],
            username=username,
            cookies=user["cookies"]
        )


def get_config() -> Config:
    """
    Get config.json configurations
    @return: Cached config if having been loaded from disk
    """
    global _config
    if not _config:
        _config = load_and_validate_config_from_file()
    return _config


@logger.catch
def save_config(new_config: Config):
    with open(SRC_PATH, "w") as src_f:
        json.dump(json.loads(new_config.model_dump_json()), src_f, ensure_ascii=False, indent=4)
        logger.success("新配置写入 config.json 成功")


def load_and_validate_config_from_file() -> Config:
    try:
        with open(SRC_PATH, "r") as src_f:
            raw_json_data = src_f.read()
        return Config.model_validate_json(raw_json_data)
    except FileNotFoundError:
        logger.info("config.json 未在运行目录找到，使用缺省值")
        return Config()
    except ValidationError as e:
        logger.error("错误的 config.json, 查看以下信息以更正:")
        logger.error(e)
        sys.exit(-1)


def retry(times: int = get_config().http.retry_max_times, delay: float = get_config().http.retry_delay):
    """
    Retry decorator

    Args:
        times: Retry times
        delay: Interval between each retry (Unit: second)
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Jump out of the local namespace (within the decorator func) to get times variable
            nonlocal times
            # It's a hard-to-detect bug :~|
            # When use `@retry()` instead of `@retry`, the retry func will be only called one time.
            # So the times variable won't be refreshed each time the decorated function is called.
            # remaining_times includes the first time normal request, so plus 1
            remaining_times = times + 1
            while remaining_times:
                await asyncio.sleep(delay)
                remaining_times -= 1
                try:
                    return await func(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    code = e.response.status_code
                    if code == 429:
                        logger.error(f"429 Too many requests")
                    else:
                        logger.error(e)
                except ResponseCodeException as e:
                    logger.error(e)
                logger.info(f"还剩第{remaining_times}次重试机会")
            logger.error("超过最大重试次数!")
            sys.exit(-1)

        return wrapper

    # https://stackoverflow.com/questions/35572663/using-python-decorator-with-or-without-parentheses
    # Following statement will be True when someone forget to add the parentheses
    if iscoroutinefunction(times):
        f = times
        times = 3
        # noinspection PyTypeChecker
        return decorator(f)
    return decorator


@retry()
async def request(client: httpx.AsyncClient, url: Urls, params: dict[str, Any] = None, data: dict[str, Any] = None,
                  raw_content=False) -> Union[Any]:
    if data:
        resp = await client.request("POST", url.value, params=params, data=data)
    else:
        resp = await client.request("GET", url.value, params=params, data=data)
    if raw_content:
        return resp.text
    try:
        resp_json: dict = resp.json()
    except JSONDecodeError as e:
        logger.error(resp.text)
        raise e
    code = resp_json.get("code")
    msg = resp_json.get("msg")
    if msg is None:
        msg = resp_json.get("message")
    if code is None:
        code = resp_json.get("errno")
    if code != 0:
        raise ResponseCodeException(code, msg, resp_json)
    return resp_json


@logger.catch
def cookie_str2httpx_cookie(cookie: str) -> Cookies:
    cookie_dict = dict()
    for kv in cookie.split(";"):
        kv_pair = kv.split("=")
        k = kv_pair[0].strip()
        if not k:
            continue
        v = kv_pair[1].strip()
        cookie_dict[k] = v
    return httpx.Cookies(cookie_dict)


def get_user_in_config(uid: str) -> ConfigUser:
    for o in get_config().users:
        if str(o.uid) == str(uid):
            return o
    logger.error(f"{uid} 还未进行选票配置，请运行 ShowConfiguration.py 进行配置!")
    sys.exit(-1)


def get_payload(uid: str) -> dict:
    user_obj = get_user_in_config(uid)
    proj = user_obj.project
    m1 = proj.payload_universal
    m2 = proj.payload_with_auth
    m1_: dict = json.loads(m1.model_dump_json())
    m2_: dict = json.loads(m2.model_dump_json())
    m1_.update(m2_)
    return m1_


def load_proxies(http: str, https: str = "") -> HttpxProxies:
    """
    Transform str proxies to Httpx format proxies
    @param http: http proxy url
    @param https: https proxy url
    @return: dict[str, HTTPTransport]
    """
    return HttpxProxies({
        "http://": httpx.HTTPTransport(proxy=http),
        "https://": httpx.HTTPTransport(proxy=https if https else http),
    })
