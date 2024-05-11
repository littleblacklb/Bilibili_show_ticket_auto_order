from enum import Enum

import httpx


class HttpRelated:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.1.4.514 Safari/537.36",
        "Referer": "https://mall.bilibili.com/",
        "Origin": "https://mall.bilibili.com/",
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
