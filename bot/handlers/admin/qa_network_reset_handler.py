import multiprocessing

from aiogram import Dispatcher
from aiogram.types import Message

from services import user_service
from misc import bot, network_answer_recognizer


async def reset_qa_network(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            network_answer_recognizer.clear_model()
            network_answer_recognizer.clear_data()

            await bot.send_message(message.from_user.id, "Нейронная сеть успешно очищена.")
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


def register_qa_network_train_handler(dp: Dispatcher):
    dp.register_message_handler(reset_qa_network, commands=["qa_network_reset"], state=None)
