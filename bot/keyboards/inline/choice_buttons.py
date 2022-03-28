from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="choice:Yes"),
        InlineKeyboardButton(text="Нет", callback_data="choice:No")
    ]
])
