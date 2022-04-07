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

from handlers import answering_handler, welcome_handler

from handlers.admin import (
    add_question_answer_handler,
    remove_question_answer_handler,
    show_question_answer_handler,
    show_question_answer_list_handler
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
    welcome_handler.register_welcome_handlers(dp)

    add_question_answer_handler.register_add_qa_handlers(dp)
    remove_question_answer_handler.register_remove_qa_handlers(dp)
    show_question_answer_handler.register_show_qa_handlers(dp)
    show_question_answer_list_handler.register_show_qa_list_handlers(dp)

    answering_handler.register_answering_handlers(dp)

    event_loop = get_event_loop()
    event_loop.run_until_complete(init_connection())
    executor.start_polling(dp, loop=event_loop, skip_updates=True)
