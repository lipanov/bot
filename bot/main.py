"""
The basis for working with a telegram.
Commands are registered to which the bot will respond.

DO NOT USE FOR BASIC LOGIC.
"""
import logging
from asyncio import get_event_loop
from asyncpgsa import pg
from misc import dp
from configs import DataBaseConfig

from aiogram import executor
from aiogram import Bot, types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def echo(message: Message) -> None:
    """
    :param message: Telegram message
    """
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

#Имитатор бд############################
def obl_id(id_):
    d = {
        0: 'Нет',
        1: 'Да',
    }
    return d[id_]


def id_obl(id_):
    d = {
        'Нет': 0,
        'Да': 1,
    }
    return d[id_]


def obl_names():
    return ['Да', 'Нет']


def obl_con_obl_list():
    return [[None, 0], [0, 1]]
########################################

@dp.message_handler(lambda message: types.Message)
async def show_que(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in obl_con_obl_list():
        buttons = [obl_id(i[1])]
        keyboard.add(*buttons)
    await message.answer("кк", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Да")
async def show_yes_menu(message: types.Message):
    #Пользователя устроил ответ => ДА заносится в бд
    pass


@dp.message_handler(lambda message: message.text == "Нет")
async def show_no_menu(message: types.Message):
    #Пользователя не устроил ответ => НЕТ заносится в бд
    pass


if __name__ == '__main__':
    event_loop = get_event_loop()
    event_loop.run_until_complete(init_connection())
    executor.start_polling(dp, loop=event_loop, skip_updates=True)
