from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from localization import RU_KEY, EN_KEY
from localization.messages import invalid_data_try_again_message
from localization.messages.change_role import *
from localization.messages.welcome import *

from services import user_service

from keyboards import create_list_kb, create_remove_kb

from misc import bot


class ChangeRoleFSM(StatesGroup):
    waiting_for_who = State()
    waiting_for_edu_form = State()


async def change_who(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        language_key = await user_service.get_user_language_key(message.from_user.id)

        who_list = who_words(language_key)
        await bot.send_message(message.from_user.id, choose_who_message(language_key),
                               reply_markup=create_list_kb(who_list))
        await ChangeRoleFSM.waiting_for_who.set()


async def wait_for_who(message: Message, state: FSMContext):
    language_key = await user_service.get_user_language_key(message.from_user.id)
    enrollee_who = enrollee_who_word(language_key)
    student_who = student_who_word(language_key)
    who_list = who_words(language_key)
    if message.text in who_list:
        who = str(message.text)
        edu_forms = edu_form_words(language_key)

        if who == student_who:
            await bot.send_message(message.from_user.id, edu_from_you_studying_message(language_key),
                                   reply_markup=create_list_kb(edu_forms))
        elif who == enrollee_who:
            await bot.send_message(message.from_user.id, edu_from_you_plan_message(language_key),
                                   reply_markup=create_list_kb(edu_forms))

        async with state.proxy() as data:
            data['who'] = who

        await ChangeRoleFSM.waiting_for_edu_form.set()
    else:
        await bot.send_message(message.from_user.id, invalid_data_try_again_message(language_key))


async def wait_for_edu_form(message: Message, state: FSMContext):
    language_key = await user_service.get_user_language_key(message.from_user.id)

    edu_forms = edu_form_words(language_key)

    if message.text in edu_forms:
        async with state.proxy() as data:
            who = data['who']
        enrollee_who = enrollee_who_word(language_key)
        student_who = student_who_word(language_key)

        full_time_edu_form = full_time_edu_form_word(language_key)
        part_time_edu_form = part_time_edu_form_word(language_key)
        extramural_edu_form = extramural_edu_form_word(language_key)

        edu_form = str(message.text)

        async with state.proxy() as data:
            data['edu_form'] = edu_form

        if who == student_who:
            if edu_form == full_time_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.STUDENT_FULL_TIME_ROLE_TITLE)
            elif edu_form == part_time_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.STUDENT_PART_TIME_ROLE_TITLE)
            elif edu_form == extramural_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.STUDENT_EXTRAMURAL_ROLE_TITLE)
        elif who == enrollee_who:
            if edu_form == full_time_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.ENROLLEE_FULL_TIME_ROLE_TITLE)
            elif edu_form == part_time_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.ENROLLEE_PART_TIME_ROLE_TITLE)
            elif edu_form == extramural_edu_form:
                await user_service.change_who_for_user(message.from_user.id,
                                                       user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE)

        await bot.send_message(message.from_user.id, who_selected_message(language_key),
                               reply_markup=create_remove_kb())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, invalid_data_try_again_message(language_key))


def register_change_role_handler(dp: Dispatcher):
    dp.register_message_handler(change_who, commands=["change_role"], state=None)
    dp.register_message_handler(wait_for_who, state=ChangeRoleFSM.waiting_for_who)
    dp.register_message_handler(wait_for_edu_form, state=ChangeRoleFSM.waiting_for_edu_form)
