from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import qa_service, user_service
from constants import ADMIN_ROLE_TITLE
from misc import bot


class RemoveQuestionAnswerFSM(StatesGroup):
    waiting_for_id = State()


async def remove_question_answer(message: Message, state: FSMContext):
    has_required_role = await user_service.has_role(message.from_user.id, ADMIN_ROLE_TITLE)

    if has_required_role:
        await bot.send_message(message.from_user.id, "Введите id пары вопрос-ответ, которую вы хотите удалить.")
        await RemoveQuestionAnswerFSM.waiting_for_id.set()
    else:
        await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_id(message: Message, state: FSMContext):
    if str.isdigit(message.text):
        if await qa_service.has_qa_record(int(message.text)):
            await qa_service.remove_qa_record(int(message.text))
            await bot.send_message(message.from_user.id, "Пара вопрос-ответ успешно удалена!")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Пара вопрос-ответ с таким id не найдена.")
            await state.finish()


def register_remove_qa_handlers(dp: Dispatcher):
    dp.register_message_handler(remove_question_answer, commands=["qa_remove"], state=None)
    dp.register_message_handler(wait_for_id, state=RemoveQuestionAnswerFSM.waiting_for_id)
