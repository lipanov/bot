from typing import List

from localization import RU_KEY, EN_KEY


def invalid_data_message(language_key: str) -> str:
    messages = {RU_KEY: "Некорректно введены данные.",
                EN_KEY: "Data entered incorrectly."}
    
    return messages[language_key]


def try_again_message(language_key: str) -> str:
    messages = {RU_KEY: "Попробуйте ещё раз.",
                EN_KEY: "Try again."}
    
    return messages[language_key]


def invalid_data_try_again_message(language_key: str) -> str:
    return invalid_data_message(language_key) + " " + try_again_message(language_key)


def back_word(language_key: str) -> str:
    messages = {RU_KEY: "Назад",
                EN_KEY: "Back"}

    return messages[language_key]


def yes_word(language_key: str) -> str:
    messages = {RU_KEY: "Да",
                EN_KEY: "Yes"}
    
    return messages[language_key]


def no_word(language_key: str) -> str:
    messages = {RU_KEY: "Нет",
                EN_KEY: "No"}
    
    return messages[language_key]


def yes_no_words(language_key: str) -> List[str]:
    return [yes_word(language_key), no_word(language_key)]
