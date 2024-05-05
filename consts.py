from enum import Enum

import httpx


class HttpRelated:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.1.4.514 Safari/537.36",
        "Referer": "https://mall.bilibili.com/", "Origin": "https://mall.bilibili.com/", "Pregma": "no-cache",
        "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Cookie": "a=b;",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9", "Accept-Encoding": "", "Connection": "keep-alive"
    }

    GLOBAL_CLIENT = httpx.AsyncClient(headers=HEADERS)


class Urls(Enum):
    # GET
    # version 134
    # id
    PROJECT_INFO = "https://show.bilibili.com/api/ticket/project/get"
    # GET
    # projectId
    BUYER_INFO = "https://show.bilibili.com/api/ticket/buyer/list"
    # GET
    ADDRESS_INFO = "https://show.bilibili.com/api/ticket/addr/list"
    # GET
    # project_id
    ACQUIRE_TOKEN = "https://show.bilibili.com/api/ticket/order/prepare"
    # POST
    # urlencode(data["data"]["ga_data"]["riskParams"])
    GEETEST__ACQUIRE_GT_CGE_CODE = "https://api.bilibili.com/x/gaia-vgate/v1/register"
    # POST
    # challenge, token, seccode, csrf, validate
    GEETEST__VALIDATION = "https://api.bilibili.com/x/gaia-vgate/v1/validate"
    # POST
    # params: project_id
    # payload: <complex Line273+>
    ORDER_CREATION = "https://show.bilibili.com/api/ticket/order/createV2"
    # GET
    # token
    ACQUIRE_PAYMENT_QR_CODE = "https://show.bilibili.com/api/ticket/order/createstatus"


class AuthType(Enum):
    """
    项目实名认证规则
    """
    NO_AUTH = "NO_AUTH"
    AUTH_PER_ORDER = "AUTH_PER_ORDER"
    AUTH_PER_PERSON = "AUTH_PER_PERSON"
