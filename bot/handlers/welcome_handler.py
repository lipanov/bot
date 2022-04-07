from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import user_service

from constants import ENROLLEE_ROLE_TITLE
from constants import STUDENT_ROLE_TITLE
from constants import FULL_TIME_ROLE_TITLE
from constants import PART_TIME_ROLE_TITLE
from constants import EXTRAMURAL_ROLE_TITLE

from keyboards import create_who_kb, create_edu_form_kb, create_remove_kb
from misc import bot


class WelcomeUserFSM(StatesGroup):
    welcome = State()
    waiting_for_name = State()
    waiting_for_who = State()
    waiting_for_edu_form = State()


async def start_command(message: Message, state: FSMContext):
    await WelcomeUserFSM.welcome.set()
    await welcome(message, state)


async def welcome(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        user_record = await user_service.get_user_record(message.from_user.id)
        user_record_dict = dict(user_record)

        await bot.send_message(message.from_user.id, "С возвращением, " + user_record_dict["User_name"] + "! Какой вопрос вас интересует?")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Добро пожаловать! Подскажите, как к вам лучше обращаться?")
        await WelcomeUserFSM.waiting_for_name.set()


async def wait_for_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = str(message.text)

    await user_service.create_user(message.from_user.id, data["name"])

    await bot.send_message(message.from_user.id, "Отлично, " + data["name"] + "! Подскажите пожалуйста, кем вы являетесь?", reply_markup=create_who_kb())
    await WelcomeUserFSM.waiting_for_who.set()


async def wait_for_who(message: Message, state: FSMContext):
    if message.text == ENROLLEE_ROLE_TITLE or message.text == STUDENT_ROLE_TITLE:
        async with state.proxy() as data:
            data["who"] = str(message.text)

        if data["who"] == STUDENT_ROLE_TITLE:
            await user_service.add_role(message.from_user.id, STUDENT_ROLE_TITLE)
            await bot.send_message(message.from_user.id, "Не подскажете, на какой форме обучения вы обучаетесь?", reply_markup=create_edu_form_kb())
            await WelcomeUserFSM.waiting_for_edu_form.set()
        elif data["who"] == ENROLLEE_ROLE_TITLE:
            await user_service.add_role(message.from_user.id, ENROLLEE_ROLE_TITLE)
            await bot.send_message(message.from_user.id, "Авторизация успешно завершена! Какой вопрос вас интересует?", reply_markup=create_remove_kb())
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


async def wait_for_edu_form(message: Message, state: FSMContext):
    if message.text == FULL_TIME_ROLE_TITLE:
        await user_service.add_role(message.from_user.id, FULL_TIME_ROLE_TITLE)
        await bot.send_message(message.from_user.id, "Авторизация успешно завершена! Какой вопрос вас интересует?", reply_markup=create_remove_kb())
        await state.finish()
    elif message.text == PART_TIME_ROLE_TITLE:
        await user_service.add_role(message.from_user.id, PART_TIME_ROLE_TITLE)
        await bot.send_message(message.from_user.id, "Авторизация успешно завершена! Какой вопрос вас интересует?", reply_markup=create_remove_kb())
        await state.finish()
    elif message.text == EXTRAMURAL_ROLE_TITLE:
        await user_service.add_role(message.from_user.id, EXTRAMURAL_ROLE_TITLE)
        await bot.send_message(message.from_user.id, "Авторизация успешно завершена! Какой вопрос вас интересует?", reply_markup=create_remove_kb())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_welcome_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(welcome, state=WelcomeUserFSM.welcome)
    dp.register_message_handler(wait_for_name, state=WelcomeUserFSM.waiting_for_name)
    dp.register_message_handler(wait_for_who, state=WelcomeUserFSM.waiting_for_who)
    dp.register_message_handler(wait_for_edu_form, state=WelcomeUserFSM.waiting_for_edu_form)
