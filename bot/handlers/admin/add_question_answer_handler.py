from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import qa_service, user_service
from constants import ADMIN_ROLE_TITLE
from constants import GENERAL_QA_GROUP_TITLE, ENROLLEE_QA_GROUP_TITLE, FULL_TIME_QA_GROUP_TITLE, PART_TIME_QA_GROUP_TITLE, EXTRAMURAL_QA_GROUP_TITLE
from keyboards import create_qa_group_kb, create_remove_kb
from misc import bot


class AddQuestionAnswerFSM(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()
    waiting_for_group = State()


async def add_question_answer(message: Message, state: FSMContext):
    has_required_role = await user_service.has_role(message.from_user.id, ADMIN_ROLE_TITLE)

    if has_required_role:
        await bot.send_message(message.from_user.id, "Введите вопрос для добавления.")
        await AddQuestionAnswerFSM.waiting_for_question.set()
    else:
        await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = str(message.text)

    await bot.send_message(message.from_user.id, "Введите ответ на заданный вопрос.")
    await AddQuestionAnswerFSM.waiting_for_answer.set()


async def wait_for_answer(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = str(message.text)

    await bot.send_message(message.from_user.id, "В какую группу добавить пару вопрос-ответ?", reply_markup=create_qa_group_kb())
    await AddQuestionAnswerFSM.waiting_for_group.set()


async def wait_for_group(message: Message, state: FSMContext):
    if message.text == GENERAL_QA_GROUP_TITLE or ENROLLEE_QA_GROUP_TITLE or FULL_TIME_QA_GROUP_TITLE or PART_TIME_QA_GROUP_TITLE or EXTRAMURAL_QA_GROUP_TITLE:
        async with state.proxy() as data:
            data["group"] = str(message.text)

        qa_record = await qa_service.get_or_create_qa_record(data["question"], data["answer"])
        qa_record_dict = dict(qa_record)
        await qa_service.add_qa_to_group(qa_record_dict["QuestionAnswer_id"], data["group"])

        await bot.send_message(message.from_user.id, "Пара вопрос-ответ успешно добавлена.", reply_markup=create_remove_kb())
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_add_qa_handlers(dp: Dispatcher):
    dp.register_message_handler(add_question_answer, commands=["qa_add"], state=None)
    dp.register_message_handler(wait_for_question, state=AddQuestionAnswerFSM.waiting_for_question)
    dp.register_message_handler(wait_for_answer, state=AddQuestionAnswerFSM.waiting_for_answer)
    dp.register_message_handler(wait_for_group, state=AddQuestionAnswerFSM.waiting_for_group)
