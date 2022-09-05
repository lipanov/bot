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

from handlers import answering_handler, welcome_handler, change_language_handler, change_role_handler

from handlers.admin import (
    qa_add_handler,
    qa_remove_handler,
    qa_list_handler,
    qa_show_handler,
    qa_tags_set_handler,
    qa_tags_clear_handler,
    qa_network_train_handler,
    qa_network_reset_handler
)

from misc import dp

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
    welcome_handler.register_welcome_handler(dp)

    qa_add_handler.register_qa_add_handler(dp)
    qa_remove_handler.register_qa_remove_handler(dp)

    qa_list_handler.register_qa_list_handler(dp)
    qa_show_handler.register_qa_show_handler(dp)

    qa_tags_set_handler.register_qa_tags_set_handler(dp)
    qa_tags_clear_handler.register_qa_tags_clear_handler(dp)

    qa_network_train_handler.register_qa_network_train_handler(dp)
    qa_network_reset_handler.register_qa_network_train_handler(dp)

    change_language_handler.register_change_language_handler(dp)
    change_role_handler.register_change_role_handler(dp)

    answering_handler.register_answering_handler(dp)

    event_loop = get_event_loop()
    event_loop.run_until_complete(init_connection())
    executor.start_polling(dp, loop=event_loop, skip_updates=True)
