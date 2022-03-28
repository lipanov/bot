from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from misc import bot

from DAO import UserDAO, QuestionAnswerDAO, AdminDAO


class AddQuestionAnswerFSM(StatesGroup):
    waitingForQuestion = State()
    waitingForAnswer = State()


async def add_question_answer(message: Message, state: FSMContext):
    users = UserDAO()
    admins = AdminDAO()

    user = await users.get(tg_id = message.from_user.id)
    
    if user != None:
        admin = await admins.get(user_id=dict(user)["User_id"])

        if admin != None:
            await bot.send_message(message.from_user.id, "Введите вопрос для добавления.")
            await AddQuestionAnswerFSM.waitingForQuestion.set()
        else:
            await bot.send_message(message.from_user.id, "Недостаточно прав.")


async def wait_for_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = str(message.text)

    await bot.send_message(message.from_user.id, "Введите ответ на заданный вопрос.")
    await AddQuestionAnswerFSM.waitingForAnswer.set()


async def wait_for_answer(message: Message, state: FSMContext):
    questionsAnswers = QuestionAnswerDAO()

    async with state.proxy() as data:
        data["answer"] = str(message.text)
    
    
    await questionsAnswers.create(question=data["question"], answer=data["answer"])
    await bot.send_message(message.from_user.id, "Пара вопрос-ответ успешно добавлена.")
    await state.finish()


def register_admin_handlers(dp : Dispatcher):
    dp.register_message_handler(add_question_answer, commands=["add_question_answer"], state=None)
    dp.register_message_handler(wait_for_question, state=AddQuestionAnswerFSM.waitingForQuestion)
    dp.register_message_handler(wait_for_answer, state=AddQuestionAnswerFSM.waitingForAnswer)