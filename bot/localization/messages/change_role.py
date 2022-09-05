from localization import RU_KEY, EN_KEY


def choose_who_message(language_key: str) -> str:
    messages = {RU_KEY: "Выберите вашу роль из списка.",
                EN_KEY: "Choose your role from the list."}

    return messages[language_key]


def who_selected_message(language_key: str) -> str:
    messages = {RU_KEY: "Роль успешно установлена!",
                EN_KEY: "Role set successfully!"}

    return messages[language_key]