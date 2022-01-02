import logging
import re
from asyncio import get_event_loop

from aiogram import executor
from aiogram.types import InlineQuery, Message, ContentTypes
from asyncpgsa import pg

from DAO import UserDAO
from configs import DataBaseConfig
from constants import CACHE_TIME
from misc import dp


logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)


async def init_connection():
    db_config = DataBaseConfig()
    await pg.init(
        host=db_config.host,
        port=db_config.port,
        database=db_config.name,
        user=db_config.user,
        password=db_config.password.get_secret_value(),
        min_size=5,
        max_size=10
    )


if __name__ == '__main__':
    event_loop = get_event_loop()
    event_loop.run_until_complete(init_connection())
    executor.start_polling(dp, loop=event_loop, skip_updates=True)
