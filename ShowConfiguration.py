"""
0. 选用户
1. 选展
2. 判断身份认证类型 (AuthType)
3. 选票
4. 购票人信息
5. 写入config.json
"""
import asyncio
import re
import sys

import consts
import utils
from customdataclasses import AuthType, ConfigUser
from utils import request, save_config, get_config, DbUserData
from loguru import logger

CLIENT = consts.HttpRelated.GLOBAL_CLIENT
CONFIG = get_config()


def set_auth_type(data: dict):
    logger.debug(data)
    for _ in data["data"]["performance_desc"]["list"]:
        if _["module"] == "base_info":
            for i in _["details"]:
                if i["title"] == "实名认证" or i["title"] == "实名登记" or i["title"] == "实名":
                    if "一单一证" in i["content"]:
                        logger.debug("一单一证")
                        user_obj.project.auth_type = AuthType.AUTH_PER_ORDER
                    elif "一人一证" in i["content"] or "一人一票" in i["content"]:
                        logger.debug("一人一证/票")
                        user_obj.project.auth_type = AuthType.AUTH_PER_PERSON
                    else:
                        user_obj.project.auth_type = AuthType.NO_AUTH
                    break


async def ticket_related(data: dict):
    async def address_info():
        data = await request(CLIENT, consts.Urls.ADDRESS_INFO)
        if len(data["data"]["addr_list"]) <= 0:
            logger.error("无可用地址，请先前往会员购地址管理添加收货地址")
            sys.exit(-1)
        print("\n请选择实体票发货地址(仅单地址)")
        for i in range(len(data["addr_list"])):
            print(str(i + 1) + ":",
                  data["addr_list"][i]["prov"] + data["addr_list"][i]["city"] + data["addr_list"][i]["area"] +
                  data["addr_list"][i]["addr"] + " 收件人:" + data["addr_list"][i]["name"] + " " + data["addr_list"][i][
                      "phone"])
        n = int(input("收货地址序号 >>> ").strip()) - 1
        return data["data"]["addr_list"][n]

    data = data["data"]
    print("\n演出名称: " + data["name"])
    print("票务状态: " + data["sale_flag"])
    if data["has_eticket"] == 1:
        print("本演出/展览票面为电子票/兑换票。")
    if data["has_paper_ticket"] == 1:
        print("本演出/展览包含纸质票。")
    print("\n请选择场次序号并按回车继续，格式例如 1")
    for i in range(len(data["screen_list"])):
        print(str(i + 1) + ":", data["screen_list"][i]["name"])
    date = input("场次序号 >>> ").strip()
    date = int(date) - 1
    print("已选择：", data["screen_list"][date]["name"])
    print("\n请输入票种并按回车继续，格式例如 1")
    for i in range(len(data["screen_list"][date]["ticket_list"])):
        print(str(i + 1) + ":", data["screen_list"][date]["ticket_list"][i]["desc"], "-",
              data["screen_list"][date]["ticket_list"][i]["price"] // 100, "RMB")
    choice = int(input("票种序号 >>> ").strip()) - 1
    user_obj.project.payload_universal.screen_id = data["screen_list"][date]["id"]
    user_obj.project.payload_universal.sku_id = data["screen_list"][date]["ticket_list"][choice]["id"]
    user_obj.project.payload_universal.pay_money = data["screen_list"][date]["ticket_list"][choice]["price"]
    selected_ticket_info = (data["name"] + " " + data["screen_list"][date]["name"] + " " +
                            data["screen_list"][date]["ticket_list"][choice]["desc"] + " " + str(
                data["screen_list"][date]["ticket_list"][choice]["price"] // 100) + " " + "RMB")
    print("\n已选择：", selected_ticket_info)
    deliver_info = user_obj.project.payload_universal.deliver_info
    if data["has_paper_ticket"]:
        a = await address_info()
        fa = a["prov"] + a["city"] + a["area"] + a["addr"]
        deliver_info.needed = True
        deliver_info.name = a["name"]
        deliver_info.tel = a["phone"]
        deliver_info.addr_id = a["id"]
        deliver_info.addr = fa


def get_user_in_config():
    uid = DbUserData.get_user_data(username).userid
    for o in CONFIG.users:
        if str(o.uid) == str(uid):
            return o
    return None


# 1: 一单一证
# 2: 一人一证 / 一人一票
# 0: NO AUTH

async def buyer_info_related():
    def get_t_count():
        print("\n请输入购买数量")
        n = input(">>> ").strip()
        if not re.match(r"^\d{1,2}$", n):
            logger.error("请输入正确的数量")
            sys.exit(-1)
        return int(n)

    def handle_AUTH_PER_PERSON():
        if len(data["list"]) <= 0:
            logger.error(
                "你的账号里一个购票人信息都没填写哦，请前往哔哩哔哩客户端-会员购-个人中心-购票人信息提前填写购票人信息")
            sys.exit(-1)
        print(
            "\n此演出为一人一证，请选择购票人, 全部购票请输入0，其他请输入购票人序号，多个购票请用空格分隔，如 1 2")
        for i in range(len(data["list"])):
            print(str(i + 1) + ":", "姓名: " + data["list"][i]["name"], "手机号:", data["list"][i]["tel"],
                  "身份证:", data["list"][i]["personal_id"])
        p = input("购票人序号 >>> ").strip()
        t = []
        if p == "0":
            print("\n已选择列表中全部购票人")
            return data["list"]
        elif " " in p:
            print("\n已选择: ", end="")
            for i in p.split(" "):
                if i:
                    print(data["list"][int(i) - 1]["name"], end=" ")
                    t.append(data["list"][int(i) - 1])
            print("")
            return t
        else:
            print("\n已选择: ", data["list"][int(p) - 1]["name"])
            t.append(data["list"][int(p) - 1])
            return t

    auth_type = user_obj.project.auth_type
    if auth_type == AuthType.NO_AUTH:
        # self.user_data["buyer_name"], self.user_data["buyer_phone"] = self.menu("GET_NORMAL_INFO")
        print("\n此演出无需身份电话信息，请填写姓名和联系方式后按回车")
        name = input("姓名 >>> ").strip()
        tel = input("电话 >>> ").strip()
        if not re.match(r"^\d{9,14}$", tel):
            logger.error("请输入正确格式的电话号码")
            sys.exit(-1)
        payload = user_obj.project.payload_without_auth
        payload.name = name
        payload.tel = tel
        user_obj.project.payload_universal.count = get_t_count()
        return
    data = (await request(CLIENT, consts.Urls.BUYER_INFO,
                          params={"projectId": user_obj.project.payload_universal.project_id}))["data"]
    if not data:
        logger.error("用户信息为空，请登录或先上传身份信息后重试")
        sys.exit(-1)
    if auth_type == AuthType.AUTH_PER_ORDER:
        print("\n此演出为一单一证，只需选择1个购票人，如 1")
        if len(data["list"]) <= 0:
            logger.error(
                "你的账号里一个购票人信息都没填写哦，请前往哔哩哔哩客户端-会员购-个人中心-购票人信息提前填写购票人信息")
            sys.exit(-1)
        for i in range(len(data["list"])):
            print(str(i + 1) + ":", "姓名: " + data["list"][i]["name"], "手机号:", data["list"][i]["tel"], "身份证:",
                  data["list"][i]["personal_id"])
        p = input("购票人序号 >>> ").strip()
        buyers = []
        print("\n已选择: ", data["list"][int(p) - 1]["name"])
        buyers.append(data["list"][int(p) - 1])
        user_obj.project.payload_with_auth.buyer_info = buyers

    if auth_type == AuthType.AUTH_PER_PERSON:
        buyers = handle_AUTH_PER_PERSON()
        user_obj.project.payload_with_auth.buyer_info = buyers
        user_obj.project.payload_universal.count = len(buyers)
    else:
        user_obj.project.payload_universal.count = get_t_count()

    for buyer in user_obj.project.payload_with_auth.buyer_info:
        buyer["isBuyerInfoVerified"] = True
        buyer["isBuyerValid"] = True


def load_cookie():
    ck = utils.cookie_str2httpx_cookie(DbUserData.get_user_data(username).cookies)
    CLIENT.cookies = ck


async def main():
    data: dict = await request(CLIENT, consts.Urls.PROJECT_INFO, params={"version": 234, "id": project_id})
    # 2.
    set_auth_type(data)
    # 3.
    await ticket_related(data)
    # 4.
    await buyer_info_related()


if __name__ == '__main__':
    # 0.
    usernames = DbUserData.get_available_users()
    for i in range(len(usernames)):
        print(f"{i}. {usernames[i]}")
    i = int(input("请输入要购票的用户编号\n>>>"))
    username = usernames[i]
    print("已选择", username)
    user_obj = get_user_in_config()
    if not user_obj:
        user_obj = ConfigUser(uid=DbUserData.get_user_data(username).userid)
        CONFIG.users.append(user_obj)
    load_cookie()
    # 1.
    unprocessed_project_id = (input(
        "请输入购票链接并按回车继续 格式例如 https://show.bilibili.com/platform/detail.html?id=73711\n>>> ").strip())
    project_id = re.search(r"id=\d+", unprocessed_project_id).group().split("=")[1]

    asyncio.run(main())

    save_config(CONFIG)
