from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import qa_service, user_service
from keyboards import create_list_kb, create_remove_kb
from misc import bot


class QAAddFSM(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()
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
        data["answer"] = str(message.text)

    await bot.send_message(message.from_user.id, "В какую группу добавить пару вопрос-ответ?", reply_markup=create_list_kb(qa_service.QA_FLAGS))
    await QAAddFSM.waiting_for_group.set()


async def wait_for_group(message: Message, state: FSMContext):
    if qa_service.QA_FLAGS.__contains__(message.text):
        async with state.proxy() as data:
            data["flag"] = str(message.text)

        qa_record = await qa_service.get_or_create_qa(data["question"], data["answer"])
        qa_record_dict = dict(qa_record)
        await qa_service.add_flag(qa_record_dict["QuestionAnswer_id"], data["flag"])

        await bot.send_message(message.from_user.id, "Пара вопрос-ответ успешно добавлена.", reply_markup=create_remove_kb())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_qa_add_handler(dp: Dispatcher):
    dp.register_message_handler(add_question_answer, commands=["qa_add"], state=None)
    dp.register_message_handler(wait_for_question, state=QAAddFSM.waiting_for_question)
    dp.register_message_handler(wait_for_answer, state=QAAddFSM.waiting_for_answer)
    dp.register_message_handler(wait_for_group, state=QAAddFSM.waiting_for_group)
