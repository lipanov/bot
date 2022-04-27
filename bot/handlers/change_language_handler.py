from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from localization import RU_KEY, EN_KEY
from localization.messages import invalid_data_try_again_message
from localization.messages.change_language import *

from services import user_service

from keyboards import create_list_kb, create_remove_kb

from misc import bot

RU_LANGUAGE = "Русский"
EN_LANGUAGE = "English"

LANGUAGES = [RU_LANGUAGE, EN_LANGUAGE]


class ChangeLanguageFSM(StatesGroup):
    waiting_for_language = State()


async def change_language(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        language_key = await user_service.get_user_language_key(message.from_user.id)

        await bot.send_message(message.from_user.id, choose_language_message(language_key), reply_markup=create_list_kb(LANGUAGES))
        await ChangeLanguageFSM.waiting_for_language.set()


async def wait_for_language(message: Message, state: FSMContext):
    if message.text in LANGUAGES:
        language_key = RU_KEY

        if message.text == EN_LANGUAGE:
            language_key = EN_KEY
        
        await user_service.change_language_for_user(message.from_user.id, language_key)

        await bot.send_message(message.from_user.id, language_selected_message(language_key), reply_markup=create_remove_kb())
        await state.finish()
    else:
        language_key = await user_service.get_user_language_key(message.from_user.id)
        await bot.send_message(message.from_user.id, invalid_data_try_again_message(language_key))


def register_change_language_handler(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=["change_language"], state=None)
    dp.register_message_handler(wait_for_language, state=ChangeLanguageFSM.waiting_for_language)
