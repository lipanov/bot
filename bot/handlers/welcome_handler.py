from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import user_service

from keyboards import create_list_kb, create_remove_kb
from misc import bot

STUDENT_WHO = "Студент"
ENROLLEE_WHO = "Абитуриент"

FULL_TIME_EDU_FORM = "Очная"
PART_TIME_EDU_FORM = "Очно-заочная"
EXTRAMURAL_EDU_FORM = "Заочная"

WHO_LIST = [ENROLLEE_WHO, STUDENT_WHO]
EDU_FORMS = [FULL_TIME_EDU_FORM, PART_TIME_EDU_FORM, EXTRAMURAL_EDU_FORM]


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

    await bot.send_message(message.from_user.id, "Отлично, " + data["name"] + "! Подскажите пожалуйста, кем вы являетесь?", reply_markup=create_list_kb(WHO_LIST))
    await WelcomeUserFSM.waiting_for_who.set()


async def wait_for_who(message: Message, state: FSMContext):
    if WHO_LIST.__contains__(message.text):
        async with state.proxy() as data:
            data["who"] = str(message.text)

        if data["who"] == STUDENT_WHO:
            await bot.send_message(message.from_user.id, "Не подскажете, на какой форме обучения вы обучаетесь?", reply_markup=create_list_kb(EDU_FORMS))
            await WelcomeUserFSM.waiting_for_edu_form.set()
        elif data["who"] == ENROLLEE_WHO:
            await bot.send_message(message.from_user.id, "Не подскажете, на какой форме обучения вы планируете обучаться?", reply_markup=create_list_kb(EDU_FORMS))
            await WelcomeUserFSM.waiting_for_edu_form.set()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


async def wait_for_edu_form(message: Message, state: FSMContext):
    if EDU_FORMS.__contains__(message.text):
        async with state.proxy() as data:
            data["edu_form"] = str(message.text)

        if data["who"] == STUDENT_WHO:
            if data["edu_form"] == FULL_TIME_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.STUDENT_FULL_TIME_ROLE_TITLE)
            elif data["edu_form"] == PART_TIME_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.STUDENT_PART_TIME_ROLE_TITLE)
            elif data["edu_form"] == EXTRAMURAL_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.STUDENT_EXTRAMURAL_ROLE_TITLE)
        elif data["who"] == ENROLLEE_WHO:
            if data["edu_form"] == FULL_TIME_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.ENROLLEE_FULL_TIME_ROLE_TITLE)
            elif data["edu_form"] == PART_TIME_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.ENROLLEE_PART_TIME_ROLE_TITLE)
            elif data["edu_form"] == EXTRAMURAL_EDU_FORM:
                await user_service.add_role(message.from_user.id, user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE)

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
