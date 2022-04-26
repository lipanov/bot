from typing import List
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from qa_recognition.routers import RatingRouter
from services import user_service, qa_service

from DAO import SessionLogDAO
from keyboards import create_yes_no_kb, create_remove_kb
from misc import bot


class AnsweringFSM(StatesGroup):
    waiting_for_rate = State()


async def wait_for_question(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        qa_pairs = []

        user_roles = await user_service.get_roles(message.from_user.id)
        qa_flags =  get_qa_flags_by_user_roles(user_roles)

        for flag in qa_flags:
            qa_pairs += await qa_service.get_qa_pairs_by_flag(flag)

        answers = await RatingRouter.get_most_relevant_answers(message.text, qa_pairs)

        answers_queue = []

        if len(answers) > 0:
            answers_queue.append(answers[0])

            if len(answers) > 1:
                answers_queue.append(answers[1])

            async with state.proxy() as data:
                data["answers_queue"] = answers_queue

            await next_answer(message, state)
        else:
            await message.reply("Ответ на данный вопрос не найден!")


def get_qa_flags_by_user_roles(user_roles: List[str]) -> List[str]:
    qa_flags = [qa_service.GENERAL_QA_FLAG]

    if user_roles.__contains__(user_service.ENROLLEE_GENERAL_ROLE_TITLE):
        qa_flags.append(qa_service.ENROLLEE_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_FULL_TIME_ROLE_TITLE):
        qa_flags.append(qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(qa_service.ENROLLEE_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_PART_TIME_ROLE_TITLE):
        qa_flags.append(qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(qa_service.ENROLLEE_PART_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(qa_service.ENROLLEE_QA_FLAG)
        qa_flags.append(qa_service.ENROLLEE_EXTRAMURAL_QA_FLAG)

    if user_roles.__contains__(user_service.ENROLLEE_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(qa_service.STUDENT_QA_FLAG)
        qa_flags.append(qa_service.STUDENT_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_FULL_TIME_ROLE_TITLE):
        qa_flags.append(qa_service.STUDENT_QA_FLAG)
        qa_flags.append(qa_service.STUDENT_FULL_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_PART_TIME_ROLE_TITLE):
        qa_flags.append(qa_service.STUDENT_QA_FLAG)
        qa_flags.append(qa_service.STUDENT_PART_TIME_QA_FLAG)

    if user_roles.__contains__(user_service.STUDENT_EXTRAMURAL_ROLE_TITLE):
        qa_flags.append(qa_service.STUDENT_QA_FLAG)
        qa_flags.append(qa_service.STUDENT_EXTRAMURAL_QA_FLAG)

    return qa_flags


async def wait_for_rate(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await save_rate(True, message, state)
        await clear_answer_queue(state)
        await state.finish()
    elif message.text.lower() == "нет":
        await save_rate(False, message, state)

        if await has_next_answer(state):
            await message.reply("Возможно вас устроит следующий ответ на ваш вопрос...")
            await next_answer(message, state)
        else:
            await state.finish()
    else:
        await message.reply("Если ответ вас устроил, напишите *Да*, если же ответ вас не устроил, напишите *Нет*.", parse_mode="Markdown")


async def has_next_answer(state: FSMContext) -> bool:
    async with state.proxy() as data:
        if "answers_queue" in data:
            answers_queue = data["answers_queue"]

            if len(answers_queue) > 0:
                return True

    return False


async def clear_answer_queue(state: FSMContext):
    if await has_next_answer(state):
        async with state.proxy() as data:
            data["answers_queue"] = []


async def next_answer(message: Message, state: FSMContext):
    if await has_next_answer(state):
        async with state.proxy() as data:
            answers_queue = data["answers_queue"]

        answer = answers_queue.pop(0)

        async with state.proxy() as data:
            data["answers_queue"] = answers_queue
            data["algorithm"] = str(answer.algorithm_key)

        question_message = await bot.send_message(message.from_user.id, answer.qa_pair.answer)

        await AnsweringFSM.waiting_for_rate.set()
        await bot.send_message(message.from_user.id, "Вас устроил ответ на ваш вопрос?", reply_markup=create_yes_no_kb())


async def save_rate(successful: bool, message: Message, state: FSMContext):
    session_log_DAO = SessionLogDAO()

    if await user_service.has_user_record(message.from_user.id):
        user_record_dict = dict(await user_service.get_user_record(message.from_user.id))

        await bot.send_message(message.from_user.id, "Спасибо за вашу оценку", reply_markup=create_remove_kb())

        async with state.proxy() as data:
            user_id = user_record_dict["User_id"]
            algorithm = data["algorithm"]
            await session_log_DAO.create(user_id=user_id, algorithm=algorithm, successful=successful)


def register_answering_handler(dp: Dispatcher):
    dp.register_message_handler(wait_for_question, state=None)
    dp.register_message_handler(wait_for_rate, state=AnsweringFSM.waiting_for_rate)
