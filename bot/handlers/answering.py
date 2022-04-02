from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from misc import bot
from keyboards import answeringKeyboard, ReplyKeyboardRemove

from DAO import UserDAO, SessionLogDAO
from qa_recognition import router


class AnsweringFSM(StatesGroup):
    waitingForRate = State()


async def wait_for_question(message: Message, state: FSMContext):
    users = UserDAO()

    record = await users.get(tg_id = message.from_user.id)

    if record != None:
        answer = await router.get_most_relevant_answer(message.text)

        if answer != None:
            async with state.proxy() as data:
                data["algorithm"] = str(answer.algorithm_key)

            await message.reply(answer.answerText)
            await AnsweringFSM.waitingForRate.set()
            await bot.send_message(message.from_user.id, "Вас устроил ответ на ваш вопрос?", reply_markup=answeringKeyboard)
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
    users = UserDAO()
    sessionLogs = SessionLogDAO()

    record = await users.get(tg_id = message.from_user.id)

    if record != None:
        user = dict(record)

        await bot.send_message(message.from_user.id, "Спасибо за вашу оценку", reply_markup=ReplyKeyboardRemove())

        async with state.proxy() as data:
            user_id = user["User_id"]
            algorithm = data["algorithm"]
            successful = data["successful"]
            await sessionLogs.create(user_id=user_id, algorithm=algorithm, successful=successful)

    await state.finish()


async def wait_for_rate(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await rate_positive(message, state)
    elif message.text.lower() == "нет":
        await rate_negative(message, state)
    else:
        await message.reply('Если ответ вас устроил, напишите "Да", если же ответ вас не устроил, напишите "Нет".')


def register_answering_handlers(dp : Dispatcher):
    dp.register_message_handler(wait_for_question, state=None)
    dp.register_message_handler(wait_for_rate, state=AnsweringFSM.waitingForRate)