from localization import RU_KEY, EN_KEY


def choose_language_message(language_key: str) -> str:
    messages = {RU_KEY: "Выберите удобный вам язык из списка.",
                EN_KEY: "Choose your preferred language from the list."}
    
    return messages[language_key]


def language_selected_message(language_key: str) -> str:
    messages = {RU_KEY: "Язык успешно установлен!",
                EN_KEY: "Language set successfully!"}
    
    return messages[language_key]
