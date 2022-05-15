from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from localization import RU_KEY, EN_KEY
from localization.messages import invalid_data_try_again_message, back_word
from localization.messages.welcome import *

from services import user_service

from keyboards import create_list_kb, create_remove_kb
from misc import bot

RU_LANGUAGE = "Русский"
EN_LANGUAGE = "English"

LANGUAGES = [RU_LANGUAGE, EN_LANGUAGE]


class WelcomeUserFSM(StatesGroup):
    waiting_for_language = State()
    waiting_for_name = State()
    waiting_for_who = State()
    waiting_for_edu_form = State()


async def start_command(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        user_record = await user_service.get_user_record(message.from_user.id)
        user_record_dict = dict(user_record)

        language_key = await user_service.get_user_language_key(message.from_user.id)
        user_name = user_record_dict['User_name']

        await bot.send_message(message.from_user.id, welcome_back_message(language_key, user_name))
        await state.finish()
    else:
        message_text = choose_language_message(RU_KEY) + "\n\n" + choose_language_message(EN_KEY)

        await bot.send_message(message.from_user.id, message_text, reply_markup=create_list_kb(LANGUAGES))
        await WelcomeUserFSM.waiting_for_language.set()


async def wait_for_language(message: Message, state: FSMContext):
    if message.text in LANGUAGES:
        language_key = RU_KEY

        if message.text == EN_LANGUAGE:
            language_key = EN_KEY
    
        await bot.send_message(message.from_user.id, language_selected_message(language_key))
        await bot.send_message(message.from_user.id, welcome_message(language_key), reply_markup=create_list_kb([back_word(language_key)]))

        async with state.proxy() as data:
            data['language_key'] = language_key

        await WelcomeUserFSM.waiting_for_name.set()
    else:
        message_text = invalid_data_try_again_message(RU_KEY) + "\n\n" + invalid_data_try_again_message(EN_KEY)

        await bot.send_message(message.from_user.id, message_text)


async def wait_for_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        language_key = data['language_key']

    if message.text == back_word(language_key):
        await bot.send_message(message.from_user.id, choose_language_message(language_key), reply_markup=create_list_kb(LANGUAGES))
        await WelcomeUserFSM.waiting_for_language.set()
    else:
        name = str(message.text)

        async with state.proxy() as data:
            data['name'] = name

        who_list = who_words(language_key)

        await bot.send_message(message.from_user.id, who_are_you_message(language_key, name), reply_markup=create_list_kb(who_list + [back_word(language_key)]))
        await WelcomeUserFSM.waiting_for_who.set()


async def wait_for_who(message: Message, state: FSMContext):
    async with state.proxy() as data:
        language_key = data['language_key']
    
    if message.text == back_word(language_key):
        await bot.send_message(message.from_user.id, welcome_message(language_key), reply_markup=create_list_kb([back_word(language_key)]))
        await WelcomeUserFSM.waiting_for_name.set()
    else:
        enrollee_who = enrollee_who_word(language_key)
        student_who = student_who_word(language_key)
        who_list = who_words(language_key)

        if message.text in who_list:
            who = str(message.text)
            edu_forms = edu_form_words(language_key)

            if who == student_who:
                await bot.send_message(message.from_user.id, edu_from_you_studying_message(language_key), reply_markup=create_list_kb(edu_forms + [back_word(language_key)]))
            elif who == enrollee_who:
                await bot.send_message(message.from_user.id, edu_from_you_plan_message(language_key), reply_markup=create_list_kb(edu_forms + [back_word(language_key)]))

            async with state.proxy() as data:
                data['who'] = who

            await WelcomeUserFSM.waiting_for_edu_form.set()
        else:
            await bot.send_message(message.from_user.id, invalid_data_try_again_message(language_key))


async def wait_for_edu_form(message: Message, state: FSMContext):
    async with state.proxy() as data:
        language_key = data['language_key']

    if message.text == back_word(language_key):
        who_list = who_words(language_key)
        name = data['name']

        await bot.send_message(message.from_user.id, who_are_you_message(language_key, name), reply_markup=create_list_kb(who_list + [back_word(language_key)]))
        await WelcomeUserFSM.waiting_for_who.set()
    else:
        edu_forms = edu_form_words(language_key)

        if message.text in edu_forms:
            who = data['who']
            enrollee_who = enrollee_who_word(language_key)
            student_who = student_who_word(language_key)

            full_time_edu_form = full_time_edu_form_word(language_key)
            part_time_edu_form = part_time_edu_form_word(language_key)
            extramural_edu_form = extramural_edu_form_word(language_key)

            edu_form = str(message.text)

            async with state.proxy() as data:
                data['edu_form'] = edu_form
            
            name = data['name']

            await user_service.create_user(message.from_user.id, name)
            await user_service.change_language_for_user(message.from_user.id, language_key)

            if who == student_who:
                if edu_form == full_time_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.STUDENT_FULL_TIME_ROLE_TITLE)
                elif edu_form == part_time_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.STUDENT_PART_TIME_ROLE_TITLE)
                elif edu_form == extramural_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.STUDENT_EXTRAMURAL_ROLE_TITLE)
            elif who == enrollee_who:
                if edu_form == full_time_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.ENROLLEE_FULL_TIME_ROLE_TITLE)
                elif edu_form == part_time_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.ENROLLEE_PART_TIME_ROLE_TITLE)
                elif edu_form == extramural_edu_form:
                    await user_service.change_who_for_user(message.from_user.id, user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE)

            await bot.send_message(message.from_user.id, auth_success_message(language_key), reply_markup=create_remove_kb())
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, invalid_data_try_again_message(language_key))


def register_welcome_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(wait_for_language, state=WelcomeUserFSM.waiting_for_language)
    dp.register_message_handler(wait_for_name, state=WelcomeUserFSM.waiting_for_name)
    dp.register_message_handler(wait_for_who, state=WelcomeUserFSM.waiting_for_who)
    dp.register_message_handler(wait_for_edu_form, state=WelcomeUserFSM.waiting_for_edu_form)
