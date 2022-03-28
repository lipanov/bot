from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

yesButton = KeyboardButton("Да")
noButton = KeyboardButton("Нет")

answeringKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

answeringKeyboard.row(yesButton, noButton)