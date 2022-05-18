from localization import RU_KEY, EN_KEY


def answer_not_found_message(language_key: str) -> str:
    messages = {RU_KEY: "К сожалению, ответ на данный вопрос не найден!",
                EN_KEY: "Unfortunately, the answer to this question has not been found!"}
    
    return messages[language_key]


def maybe_next_answer_suits_you_message(language_key: str) -> str:
    messages = {RU_KEY: "Возможно вас устроит следующий ответ на ваш вопрос...",
                EN_KEY: "Perhaps you will be satisfied with the following answer to your question..."}
    
    return messages[language_key]


def yes_no_hint_message(language_key: str) -> str:
    messages = {RU_KEY: "Если ответ вас устроил, напишите *Да*, если же ответ вас не устроил, напишите *Нет*.",
                EN_KEY: "If the answer suits you, write *Yes*, if the answer does not suit you, write *No*."}
    
    return messages[language_key]


def are_you_satisfied_with_the_answer_message(language_key: str) -> str:
    messages = {RU_KEY: "Вас устроил ответ на ваш вопрос?",
                EN_KEY: "Are you satisfied with the answer to your question?"}
    
    return messages[language_key]


def thank_you_for_rate_message(language_key: str) -> str:
    messages = {RU_KEY: "Спасибо за вашу оценку!",
                EN_KEY: "Thanks for the feedback!"}
    
    return messages[language_key]
