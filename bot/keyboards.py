from typing import List
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove


def create_yes_no_kb() -> ReplyKeyboardMarkup:
    yes_button = KeyboardButton("Да")
    no_button = KeyboardButton("Нет")
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(yes_button, no_button)
    return kb


def create_list_kb(str_list: List[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for item in str_list:
        kb.add(KeyboardButton(item))

    return kb


def create_remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
