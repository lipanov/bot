from aiogram import Dispatcher
from aiogram.types import Message

from services import qa_service, user_service
from constants import ADMIN_ROLE_TITLE
from misc import bot


async def show_question_answer_list(message: Message):
    has_required_role = await user_service.has_role(message.from_user.id, ADMIN_ROLE_TITLE)

    if has_required_role:
        qa_list_message = "Список пар вопрос-ответ:\n"
        qa_records = await qa_service.get_all_qa_records()

        for qa_record in qa_records:
            qa_record_dict = dict(qa_record)

            qa_record_row = str(qa_record_dict["QuestionAnswer_id"]) + ". "
            qa_record_row += str(qa_record_dict["QuestionAnswer_question"]) + " "
            qa_groups = await qa_service.get_qa_groups(qa_record_dict["QuestionAnswer_id"])

            if len(qa_groups) > 0:
                qa_groups_list = "( "
                for qa_group in qa_groups:
                    qa_groups_list += qa_group + " "
                qa_groups_list += ")"
                qa_record_row += " " + qa_groups_list
            else:
                qa_record_row += "(-)"
            qa_record_row += "\n"
            qa_list_message += qa_record_row

        await bot.send_message(message.from_user.id, qa_list_message, parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, "Недостаточно прав.")


def register_show_qa_list_handlers(dp: Dispatcher):
    dp.register_message_handler(show_question_answer_list, commands=["qa_list"], state=None)
