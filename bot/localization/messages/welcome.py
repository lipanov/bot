from typing import List

from localization import RU_KEY, EN_KEY


def choose_language_message(language_key: str) -> str:
    messages = {RU_KEY: "Привет! Для начала общения с ботом, выберите удобный вам язык.",
                EN_KEY: "Hi! To start chatting with the bot, select the language that suits you."}
    
    return messages[language_key]


def language_selected_message(language_key: str) -> str:
    messages = {RU_KEY: "Язык успешно установлен!",
                EN_KEY: "Language set successfully!"}
    
    return messages[language_key]


def welcome_message(language_key: str) -> str:
    messages = {RU_KEY: "Добро пожаловать! Подскажите, как к вам лучше обращаться?",
                EN_KEY: "Welcome! Tell me, what is the best name for you?"}
    
    return messages[language_key]


def welcome_back_message(language_key: str, user_name: str) -> str:
    messages = {RU_KEY: "С возвращением, " + user_name + "! Какой вопрос вас интересует?",
                EN_KEY: "Welcome back, " + user_name + "! What question interests you?"}
    
    return messages[language_key]


def who_are_you_message(language_key: str, user_name: str) -> str:
    messages = {RU_KEY: "Отлично, " + user_name + "! Подскажите пожалуйста, кем вы являетесь?",
                EN_KEY: "Great, " + user_name + "! Please tell me who are you?"}
    
    return messages[language_key]


def edu_from_you_studying_message(language_key: str) -> str:
    messages = {RU_KEY: "Не подскажете, на какой форме обучения вы обучаетесь?",
                EN_KEY: "Can you tell me what form of study you are studying?"}
    
    return messages[language_key]


def edu_from_you_plan_message(language_key: str) -> str:
    messages = {RU_KEY: "Не подскажете, на какой форме обучения вы планируете обучаться?",
                EN_KEY: "Can you tell me what form of study you plan to study?"}
    
    return messages[language_key]


def auth_success_message(language_key: str) -> str:
    messages = {RU_KEY: "Авторизация успешно завершена! Какой вопрос вас интересует?",
                EN_KEY: "Authorization completed successfully! What question interests you?"}
    
    return messages[language_key]


def enrollee_who_word(language_key: str) -> str:
    words = {RU_KEY: "Абитуриент", EN_KEY: "Enrollee"}
    
    return words[language_key]


def student_who_word(language_key: str) -> str:
    words = {RU_KEY: "Студент", EN_KEY: "Student"}
    
    return words[language_key]


def full_time_edu_form_word(language_key: str) -> str:
    words = {RU_KEY: "Очная", EN_KEY: "Full-Time"}
    
    return words[language_key]


def part_time_edu_form_word(language_key: str) -> str:
    words = {RU_KEY: "Очно-заочная", EN_KEY: "Part-Time"}
    
    return words[language_key]


def extramural_edu_form_word(language_key: str) -> str:
    words = {RU_KEY: "Заочная", EN_KEY: "Extramural"}
    
    return words[language_key]


def who_words(language_key: str) -> List[str]:
    return [enrollee_who_word(language_key), student_who_word(language_key)]


def edu_form_words(language_key: str) -> List[str]:
    return [full_time_edu_form_word(language_key),
            part_time_edu_form_word(language_key),
            extramural_edu_form_word(language_key)]
