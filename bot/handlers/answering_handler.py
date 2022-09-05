from typing import List
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from localization import RU_KEY, EN_KEY
from localization.messages import no_word, yes_no_words, yes_word
from localization.messages.answering import *

from qa_recognition.routers import RatingRouter
from services import user_service, qa_service

from DAO import SessionLogDAO
from keyboards import create_list_kb, create_remove_kb
from misc import bot


class AnsweringFSM(StatesGroup):
    waiting_for_rate = State()


async def clear_str(row: str) -> str:
    row = ''.join(re.findall(r'[a-zA-Zа-яА-Я ]', row))
    return row


async def wait_for_question(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        qa_pairs = []

        user_roles = await user_service.get_roles(message.from_user.id)
        qa_flags = get_qa_flags_by_user_roles(user_roles)

        for flag in qa_flags:
            qa_pairs += await qa_service.get_qa_pairs_by_flag(flag)

        message_text = await clear_str(message.text)
        answers = await RatingRouter.get_most_relevant_answers(message_text, qa_pairs)

        answers_queue = []

        if answers:
            answers_queue.append(answers[0])

            if len(answers) > 1:
                answers_queue.append(answers[1])

            async with state.proxy() as data:
                data['answers_queue'] = answers_queue

            await next_answer(message, state)
        else:
            language_key = await user_service.get_user_language_key(message.from_user.id)
            await message.reply(answer_not_found_message(language_key))


def get_qa_flags_by_user_roles(user_roles: List[str]) -> List[str]: 
    language_key = RU_KEY

    if EN_KEY in user_roles:
        language_key = EN_KEY

    qa_flags = [language_key + "/" + qa_service.GENERAL_QA_FLAG]

    if user_roles.__contains__(user_service.ENROLLEE_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_FULL_TIME_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_PART_TIME_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_PART_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.ENROLLEE_EXTRAMURAL_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.STUDENT_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.STUDENT_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_FULL_TIME_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.STUDENT_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.STUDENT_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_PART_TIME_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.STUDENT_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.STUDENT_PART_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(language_key + "/" + qa_service.STUDENT_QA_FLAG)
        qa_flags.append(language_key + "/" + qa_service.STUDENT_EXTRAMURAL_QA_FLAG)

    return qa_flags


async def wait_for_rate(message: Message, state: FSMContext):
    language_key = await user_service.get_user_language_key(message.from_user.id)

    yes = yes_word(language_key)
    no = no_word(language_key)

    if message.text.lower() == yes.lower():
        await save_rate(True, message, state)
        await clear_answer_queue(state)
        await state.finish()
    elif message.text.lower() == no.lower():
        await save_rate(False, message, state)

        if await has_next_answer(state):
            await message.reply(maybe_next_answer_suits_you_message(language_key))
            await next_answer(message, state)
        else:
            await state.finish()
    else:
        await message.reply(yes_no_hint_message(language_key), parse_mode="Markdown")


async def has_next_answer(state: FSMContext) -> bool:
    async with state.proxy() as data:
        if "answers_queue" in data:
            answers_queue = data['answers_queue']

            if len(answers_queue) > 0:
                return True

    return False


async def clear_answer_queue(state: FSMContext):
    if await has_next_answer(state):
        async with state.proxy() as data:
            data['answers_queue'] = []


async def next_answer(message: Message, state: FSMContext):
    if await has_next_answer(state):
        async with state.proxy() as data:
            answers_queue = data['answers_queue']

        answer = answers_queue.pop(0)

        async with state.proxy() as data:
            data['answers_queue'] = answers_queue
            data['algorithm'] = str(answer.algorithm_key)

        await bot.send_message(message.from_user.id, f"Отвечал: {str(answer.algorithm_key)} "
                                                     f"Текст: {answer.qa_pair.answer}")

        await AnsweringFSM.waiting_for_rate.set()

        language_key = await user_service.get_user_language_key(message.from_user.id)
        message_text = are_you_satisfied_with_the_answer_message(language_key)

        await bot.send_message(message.from_user.id, message_text, reply_markup=create_list_kb(yes_no_words(language_key)))


async def save_rate(successful: bool, message: Message, state: FSMContext):
    session_log_DAO = SessionLogDAO()

    if await user_service.has_user_record(message.from_user.id):
        user_record_dict = dict(await user_service.get_user_record(message.from_user.id))

        language_key = await user_service.get_user_language_key(message.from_user.id)
        await bot.send_message(message.from_user.id, thank_you_for_rate_message(language_key), reply_markup=create_remove_kb())

        async with state.proxy() as data:
            user_id = user_record_dict['User_id']
            algorithm = data['algorithm']

            await session_log_DAO.create(user_id=user_id, algorithm=algorithm, successful=successful)


def register_answering_handler(dp: Dispatcher):
    dp.register_message_handler(wait_for_question, state=None)
    dp.register_message_handler(wait_for_rate, state=AnsweringFSM.waiting_for_rate)
