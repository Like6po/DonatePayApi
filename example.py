import asyncio
from asyncio import sleep

from DonationPayApi.client import Client
from environs import Env

env = Env()
env.read_env()

KEY = env.str("KEY")


async def main():
    client = Client(KEY)
    user = await client.get_user()
    print(user)
    await sleep(20)

    transactions = await client.get_transactions(limit=5)
    print(transactions)
    await sleep(20)

    notification = await client.set_notification(name="test_name", sum=777, comment="Тестовый платеж!")
    print("result: ", notification)

    await client.close()


asyncio.run(main())
