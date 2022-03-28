"""
The basis for working with a telegram.
Commands are registered to which the bot will respond.

DO NOT USE FOR BASIC LOGIC.
"""
import logging
from asyncio import get_event_loop

from aiogram import executor
from asyncpgsa import pg

from configs import DataBaseConfig
from misc import dp

from handlers import welcome, answering, admin

logging.basicConfig(level=logging.INFO)


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
    welcome.register_welcome_handlers(dp)
    admin.register_admin_handlers(dp)
    answering.register_answering_handlers(dp)

    event_loop = get_event_loop()
    event_loop.run_until_complete(init_connection())
    executor.start_polling(dp, loop=event_loop, skip_updates=True)
