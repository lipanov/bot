import csv
import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ContentTypes

from services import qa_service, user_service
from misc import bot


class QATagsSetFSM(StatesGroup):
    waiting_for_id = State()
    waiting_for_document = State()


async def set_qa_tags(message: Message, state: FSMContext):
    if await user_service.has_user_record(message.from_user.id):
        has_required_role = await user_service.has_role(message.from_user.id, user_service.ADMIN_ROLE_TITLE)

        if has_required_role:
            await bot.send_message(message.from_user.id, "Введите id пары вопрос-ответ, для которой хотите добавить ключевые слова.")
            await QATagsSetFSM.waiting_for_id.set()
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_id(message: Message, state: FSMContext):
    if str.isdigit(message.text):
        qa_id = int(message.text)
        if await qa_service.has_qa(qa_id):

            async with state.proxy() as data:
                data["qa_id"] = qa_id
            
            await bot.send_message(message.from_user.id, "Прикрепите csv-файл (в формате [qa_id].csv), содержащий теги для указанной пары вопрос-ответ.")
            await QATagsSetFSM.waiting_for_document.set()
        else:
            await bot.send_message(message.from_user.id, "Пара вопрос-ответ с таким id не найдена.")
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неккоректно введены данные, попробуйте ещё раз.")


async def wait_for_document(message: Message, state: FSMContext):
    async with state.proxy() as data:
        qa_id = data["qa_id"]

    if message.document != None:
        if message.document.file_name == str(qa_id) + ".csv":
            output_folder = os.path.join('temp', 'qa', 'tags')

            if not os.path.exists(output_folder):
                os.makedirs(output_folder, exist_ok=True)

            file_path = os.path.join(output_folder, message.document.file_name)

            await message.document.download(destination=file_path)

            with open(file_path, "r") as file:
                reader = csv.reader(file)
                tags = []

                for row in reader:
                    tags.append(row[0])

                await qa_service.set_tags(qa_id, tags)

            await bot.send_message(message.from_user.id, "Ключевые слова успешно установлены.")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Неверный формат документа.")
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Документ не обнаружен.")
        await state.finish()


def register_qa_tags_set_handler(dp: Dispatcher):
    dp.register_message_handler(set_qa_tags, commands=["qa_tags_set"], state=None)
    dp.register_message_handler(wait_for_id, state=QATagsSetFSM.waiting_for_id)
    dp.register_message_handler(wait_for_document, state=QATagsSetFSM.waiting_for_document, content_types=ContentTypes.DOCUMENT)
