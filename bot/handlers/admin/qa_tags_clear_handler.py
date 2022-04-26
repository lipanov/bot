from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from services import qa_service, user_service
from misc import bot


class QATagsClearFSM(StatesGroup):
    waiting_for_id = State()


async def clear_qa_tags(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            await bot.send_message(message.from_user.id, "Введите id пары вопрос-ответ, для которой хотите очистить ключевые слова.")
            await QATagsClearFSM.waiting_for_id.set()
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_id(message: Message, state: FSMContext):
    if str.isdigit(message.text):
        qa_id = int(message.text)

        if await qa_service.has_qa(qa_id):
            await qa_service.clear_tags(qa_id)
        else:
            await bot.send_message(message.from_user.id, "Пара вопрос-ответ с таким id не найдена.")
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


def register_qa_tags_clear_handler(dp: Dispatcher):
    dp.register_message_handler(clear_qa_tags, commands=["qa_tags_clear"], state=None)
    dp.register_message_handler(wait_for_id, state=QATagsClearFSM.waiting_for_id)
