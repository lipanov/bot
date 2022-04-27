from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from localization import LANGUAGE_KEYS

from services import qa_service, user_service
from keyboards import create_list_kb, create_remove_kb

from misc import bot

RU_LANGUAGE = "Русский"
EN_LANGUAGE = "Английский"

LANGUAGES = [RU_LANGUAGE, EN_LANGUAGE]


class QAAddFSM(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()
    waiting_for_language = State()
    waiting_for_group = State()


async def add_question_answer(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            await bot.send_message(message.from_user.id, "Введите вопрос для добавления.")
            await QAAddFSM.waiting_for_question.set()
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = str(message.text)

    await bot.send_message(message.from_user.id, "Введите ответ на заданный вопрос.")
    await QAAddFSM.waiting_for_answer.set()


async def wait_for_answer(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = str(message.text)

    await bot.send_message(message.from_user.id, "На каком языке написан вопрос?", reply_markup=create_list_kb(LANGUAGE_KEYS))
    await QAAddFSM.waiting_for_language.set()


async def wait_for_language(message: Message, state: FSMContext):
    language_key = str(message.text)

    if language_key in LANGUAGE_KEYS:
        async with state.proxy() as data:
            data['language_key'] = language_key

        await bot.send_message(message.from_user.id, "К какой группе относиться вопрос?", reply_markup=create_list_kb(qa_service.RAW_QA_FLAGS))
        await QAAddFSM.waiting_for_group.set()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


async def wait_for_group(message: Message, state: FSMContext):
    raw_flag = str(message.text)

    if raw_flag in qa_service.RAW_QA_FLAGS:
        async with state.proxy() as data:
            question = data['question']
            answer = data['answer']
            language_key = data['language_key']

        qa_record = await qa_service.create_qa(question, answer)
        qa_record_dict = dict(qa_record)

        await qa_service.add_flag(qa_record_dict['QuestionAnswer_id'], language_key + "/" + raw_flag)

        await bot.send_message(message.from_user.id, "Пара вопрос-ответ успешно добавлена.", reply_markup=create_remove_kb())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_qa_add_handler(dp: Dispatcher):
    dp.register_message_handler(add_question_answer, commands=["qa_add"], state=None)
    dp.register_message_handler(wait_for_question, state=QAAddFSM.waiting_for_question)
    dp.register_message_handler(wait_for_answer, state=QAAddFSM.waiting_for_answer)
    dp.register_message_handler(wait_for_language, state=QAAddFSM.waiting_for_language)
    dp.register_message_handler(wait_for_group, state=QAAddFSM.waiting_for_group)
