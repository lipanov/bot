from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from misc import bot

from DAO import UserDAO

users = UserDAO()


async def start_command(message: Message, state: FSMContext):
    await WelcomeUserFSM.welcome.set()
    await welcome(message, state)


class WelcomeUserFSM(StatesGroup):
    welcome = State()
    waitingForName = State()


async def welcome(message: Message, state: FSMContext):
    record = await users.get(tg_id = message.from_user.id)

    if record == None:
        await bot.send_message(message.from_user.id, "Добро пожаловать! Подскажите, как к вам лучше обращаться?")
        await WelcomeUserFSM.waitingForName.set()
    else:
        await bot.send_message(message.from_user.id, "С возвращением, " + dict(record)["User_name"] + "! Какой вопрос вас интересует?")
        await state.finish()


async def wait_for_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = str(message.text)

    await users.create(tg_id = message.from_user.id, name=data["name"])

    await bot.send_message(message.from_user.id, "Отлично, " + data["name"] + "! Какой вопрос вас интересует?")
    await state.finish()


def register_welcome_handlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(welcome, state=WelcomeUserFSM.welcome)
    dp.register_message_handler(wait_for_name, state=WelcomeUserFSM.waitingForName)