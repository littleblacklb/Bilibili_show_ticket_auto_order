# https://github.com/Nemo2011/bilibili-api/tree/main/bilibili_api/exceptions/ResponseCodeException.py
"""
API 返回 code 错误。
"""


class ResponseCodeException(Exception):
    """
    API 返回 code 错误。
    """

    def __init__(self, code: int, msg: str, raw: dict = None):
        """
        Args:
            code:错误代码
            msg: 错误信息
            raw: 原始响应数据
        """
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.raw = raw

    def __str__(self):
        return f"接口返回错误代码：{self.code}，信息：{self.msg}。\n{self.raw}"
