from aiogram import Dispatcher
from aiogram.types import Message

from services import qa_service, user_service
from misc import bot, network_answer_recognizer


async def train_qa_network(message: Message):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            if not network_answer_recognizer.has_required_data():
                network_answer_recognizer.write_data(await qa_service.get_all_qa_pairs())

            await bot.send_message(message.from_user.id, "Обучение нейронной сети запущено.")
            network_answer_recognizer.train()
            await bot.send_message(message.from_user.id, "Обучение нейронной сети завершено.")
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


def register_qa_network_train_handler(dp: Dispatcher):
    dp.register_message_handler(train_qa_network, commands=["qa_network_train"], state=None)
