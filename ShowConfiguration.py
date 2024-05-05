"""
0. 选用户
1. 选展
2. 选票
3. 判断身份认证类型 (AuthType)
4. 选身份证
5. 写入config.json
"""
import asyncio
import re
import sys

import consts
from customdataclasses import *
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
                        user_obj.project.auth_type = AuthType.AUTH_PER_ORDER
                    elif "一人一证" in i["content"] or "一人一票" in i["content"]:
                        user_obj.project.auth_type = AuthType.AUTH_PER_PERSON
                else:
                    user_obj.project.auth_type = AuthType.NO_AUTH


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
                  data["addr_list"][i]["addr"] + " 收件人:" + data["addr_list"][i]["name"] + " " +
                  data["addr_list"][i]["phone"])
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
        print(
            str(i + 1) + ":",
            data["screen_list"][date]["ticket_list"][i]["desc"], "-",
            data["screen_list"][date]["ticket_list"][i]["price"] // 100, "RMB"
        )
    choice = int(input("票种序号 >>> ").strip()) - 1
    user_obj.project.ticket.screen_id = data["screen_list"][date]["id"]
    user_obj.project.ticket.sku_id = data["screen_list"][date]["ticket_list"][choice]["id"]
    user_obj.project.ticket.pay_money = data["screen_list"][date]["ticket_list"][choice]["price"]
    selected_ticket_info = (
            data["name"] + " " + data["screen_list"][date]["name"] + " " +
            data["screen_list"][date]["ticket_list"][choice]["desc"] + " " +
            str(data["screen_list"][date]["ticket_list"][choice]["price"] // 100) + " " + "RMB")
    print("\n已选择：", selected_ticket_info)
    deliver_info = user_obj.project.ticket.deliver_info
    if data["has_paper_ticket"]:
        a = await address_info()
        fa = a["prov"] + a["city"] + a["area"] + a["addr"]
        deliver_info.needed = True
        deliver_info.name = a["name"]
        deliver_info.tel = a["phone"]
        deliver_info.addr_id = a["id"]
        deliver_info.addr = fa
    else:
        deliver_info.needed = False


def get_user_in_config():
    uid = DbUserData.get_user_data(username).userid
    for o in CONFIG.users:
        if str(o.uid) == str(uid):
            return o
    return None


async def main():
    data: dict = await request(CLIENT, consts.Urls.PROJECT_INFO, params={"version": 234, "id": project_id})
    set_auth_type(data)
    await ticket_related(data)


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
        user_obj = ConfigUser(uid=DbUserData.get_user_data(username).userid,
                              project=Project(project_id=-1, ticket=Ticket(
                                  screen_id="-1",
                                  sku_id="-1",
                                  pay_money=-1,
                                  deliver_info=DeliverInfo()
                              )),
                              idcard_name="")
        CONFIG.users.append(user_obj)

    # 1.
    unprocessed_project_id = (input(
        "请输入购票链接并按回车继续 格式例如 https://show.bilibili.com/platform/detail.html?id=73711\n>>> ")
                              .strip())
    project_id = re.search(r"id=\d+", unprocessed_project_id).group().split("=")[1]

    asyncio.run(main())

    save_config(CONFIG)
