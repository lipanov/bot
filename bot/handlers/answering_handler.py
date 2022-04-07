from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from qa_recognition import router
from services import user_service, qa_service

from constants import ENROLLEE_ROLE_TITLE
from constants import FULL_TIME_ROLE_TITLE
from constants import PART_TIME_ROLE_TITLE
from constants import EXTRAMURAL_ROLE_TITLE

from constants import GENERAL_QA_GROUP_TITLE
from constants import ENROLLEE_QA_GROUP_TITLE
from constants import FULL_TIME_QA_GROUP_TITLE
from constants import PART_TIME_QA_GROUP_TITLE
from constants import EXTRAMURAL_QA_GROUP_TITLE

from DAO import SessionLogDAO
from keyboards import create_yes_no_kb, create_remove_kb
from misc import bot


class AnsweringFSM(StatesGroup):
    waitingForRate = State()


async def wait_for_question(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        user_roles = await user_service.get_user_roles(message.from_user.id)
        qa_pairs = await qa_service.get_qa_pairs_by_group(GENERAL_QA_GROUP_TITLE)

        if user_roles.__contains__(FULL_TIME_ROLE_TITLE):
            qa_pairs += await qa_service.get_qa_pairs_by_group(FULL_TIME_QA_GROUP_TITLE)

        if user_roles.__contains__(PART_TIME_ROLE_TITLE):
            qa_pairs += await qa_service.get_qa_pairs_by_group(PART_TIME_QA_GROUP_TITLE)

        if user_roles.__contains__(EXTRAMURAL_ROLE_TITLE):
            qa_pairs += await qa_service.get_qa_pairs_by_group(EXTRAMURAL_QA_GROUP_TITLE)

        if user_roles.__contains__(ENROLLEE_ROLE_TITLE):
            qa_pairs += await qa_service.get_qa_pairs_by_group(ENROLLEE_QA_GROUP_TITLE)

        answer = await router.get_most_relevant_answer(message.text, qa_pairs)

        if answer != None:
            async with state.proxy() as data:
                data["algorithm"] = str(answer.algorithm_key)

            await message.reply(answer.answer_text)
            await AnsweringFSM.waitingForRate.set()
            await bot.send_message(message.from_user.id, "Вас устроил ответ на ваш вопрос?", reply_markup=create_yes_no_kb())
        else:
            await message.reply("Ответ на данный вопрос не найден!")


async def rate_positive(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["successful"] = True

    await rate(message, state)


async def rate_negative(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["successful"] = False

    await rate(message, state)


async def rate(message: Message, state: FSMContext):
    session_log_DAO = SessionLogDAO()

    if await user_service.has_user_record(message.from_user.id):
        user_record_dict = dict(await user_service.get_user_record(message.from_user.id))

        await bot.send_message(message.from_user.id, "Спасибо за вашу оценку", reply_markup=create_remove_kb())

        async with state.proxy() as data:
            user_id = user_record_dict["User_id"]
            algorithm = data["algorithm"]
            successful = data["successful"]
            await session_log_DAO.create(user_id=user_id, algorithm=algorithm, successful=successful)

    await state.finish()


async def wait_for_rate(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await rate_positive(message, state)
    elif message.text.lower() == "нет":
        await rate_negative(message, state)
    else:
        await message.reply("Если ответ вас устроил, напишите *Да*, если же ответ вас не устроил, напишите *Нет*.", parse_mode="Markdown")


def register_answering_handlers(dp: Dispatcher):
    dp.register_message_handler(wait_for_question, state=None)
    dp.register_message_handler(wait_for_rate, state=AnsweringFSM.waitingForRate)
