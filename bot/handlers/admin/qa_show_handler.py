from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import qa_service, user_service
from misc import bot


class QAShowFSM(StatesGroup):
    waiting_for_id = State()


async def show_question_answer(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            await bot.send_message(message.from_user.id, "Введите id пары вопрос-ответ, которую вы хотите посмотреть.")
            await QAShowFSM.waiting_for_id.set()
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_id(message: Message, state: FSMContext):
    if str.isdigit(message.text):
        qa_id = int(message.text)

        if await qa_service.has_qa(qa_id):
            qa_pair = await qa_service.get_qa_pair(qa_id)

            qa_info = "ID: " + str(qa_pair.id) + "\n\n"
            qa_info += "Вопрос: " + str(qa_pair.question) + "\n\n"
            qa_info += "Ответ: " + str(qa_pair.answer)

            await bot.send_message(message.from_user.id, qa_info, parse_mode="Markdown")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Пара вопрос-ответ с таким id не найдена.")
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_qa_show_handler(dp: Dispatcher):
    dp.register_message_handler(show_question_answer, commands=["qa_show"], state=None)
    dp.register_message_handler(wait_for_id, state=QAShowFSM.waiting_for_id)
