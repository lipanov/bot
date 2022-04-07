from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove

from constants import ENROLLEE_ROLE_TITLE
from constants import STUDENT_ROLE_TITLE
from constants import FULL_TIME_ROLE_TITLE
from constants import PART_TIME_ROLE_TITLE
from constants import EXTRAMURAL_ROLE_TITLE

from constants import GENERAL_QA_GROUP_TITLE
from constants import ENROLLEE_QA_GROUP_TITLE
from constants import FULL_TIME_QA_GROUP_TITLE
from constants import PART_TIME_QA_GROUP_TITLE
from constants import EXTRAMURAL_QA_GROUP_TITLE


def create_who_kb() -> ReplyKeyboardMarkup:
    enrollee_button = KeyboardButton(ENROLLEE_ROLE_TITLE)
    student_button = KeyboardButton(STUDENT_ROLE_TITLE)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(enrollee_button)
    kb.add(student_button)
    return kb


def create_edu_form_kb() -> ReplyKeyboardMarkup:
    full_time_button = KeyboardButton(FULL_TIME_ROLE_TITLE)
    part_time_button = KeyboardButton(PART_TIME_ROLE_TITLE)
    extramural_time_button = KeyboardButton(EXTRAMURAL_ROLE_TITLE)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(full_time_button)
    kb.add(part_time_button)
    kb.add(extramural_time_button)
    return kb


def create_yes_no_kb() -> ReplyKeyboardMarkup:
    yes_button = KeyboardButton("Да")
    no_button = KeyboardButton("Нет")
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row(yes_button, no_button)
    return kb


def create_qa_group_kb() -> ReplyKeyboardMarkup:
    general_group_button = KeyboardButton(GENERAL_QA_GROUP_TITLE)
    enrollee_group_button = KeyboardButton(ENROLLEE_QA_GROUP_TITLE)
    full_time_group_button = KeyboardButton(FULL_TIME_QA_GROUP_TITLE)
    part_time_group_button = KeyboardButton(PART_TIME_QA_GROUP_TITLE)
    extramural_time_group_button = KeyboardButton(EXTRAMURAL_QA_GROUP_TITLE)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(general_group_button)
    kb.add(enrollee_group_button)
    kb.add(full_time_group_button)
    kb.add(part_time_group_button)
    kb.add(extramural_time_group_button)

    return kb


def create_remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
