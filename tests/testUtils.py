import asyncio

import consts
from utils import request

client = consts.HttpRelated.GLOBAL_CLIENT


async def main():
    await test_request_get()
    await test_retry()


async def test_retry():
    r = await request(client, consts.Urls.PROJECT_INFO, params={"id": 0})
    print(r)


async def test_request_get():
    r = await request(client, consts.Urls.PROJECT_INFO, params={"id": 81122})
    print(r)


if __name__ == '__main__':
    asyncio.run(main())
