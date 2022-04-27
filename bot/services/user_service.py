from email import message
from asyncpg import Record
from typing import List

from localization import RU_KEY, EN_KEY

from DAO import UserDAO, UserRoleDAO

ENROLLEE_ROLE_TITLE = 'Абитуриент'
ENROLLEE_FULL_TIME_ROLE_TITLE = 'Абитуриент/Очная'
ENROLLEE_PART_TIME_ROLE_TITLE = 'Абитуриент/Очно-заочная'
ENROLLEE_EXTRAMURAL_ROLE_TITLE = 'Абитуриент/Заочная'

STUDENT_ROLE_TITLE = 'Студент'
STUDENT_FULL_TIME_ROLE_TITLE = 'Студент/Очная'
STUDENT_PART_TIME_ROLE_TITLE = 'Студент/Очно-заочная'
STUDENT_EXTRAMURAL_ROLE_TITLE = 'Студент/Заочная'

ADMIN_ROLE_TITLE = 'Администратор'

WHO_ROLE_TITLES = [
    ENROLLEE_ROLE_TITLE,
    ENROLLEE_FULL_TIME_ROLE_TITLE,
    ENROLLEE_PART_TIME_ROLE_TITLE,
    ENROLLEE_EXTRAMURAL_ROLE_TITLE,
    STUDENT_FULL_TIME_ROLE_TITLE,
    STUDENT_PART_TIME_ROLE_TITLE,
    STUDENT_EXTRAMURAL_ROLE_TITLE
]

LANGUAGE_KEYS = [
    RU_KEY,
    EN_KEY
]

STAFF_ROLE_TITLES = [
    ADMIN_ROLE_TITLE
]

ROLE_TITLES = WHO_ROLE_TITLES + LANGUAGE_KEYS + STAFF_ROLE_TITLES


async def has_user_record(tg_id: int) -> bool:
    user_record = await get_user_record(tg_id)
    return user_record != None


async def get_user_record(tg_id: int) -> Record:
    user_DAO = UserDAO()
    user_record = await user_DAO.get(tg_id=tg_id)
    return user_record


async def create_user(tg_id: int, name: str):
    user_DAO = UserDAO()
    await user_DAO.create(tg_id=tg_id, name=name)


async def has_role(tg_id: int, role_title: str) -> bool:
    if ROLE_TITLES.__contains__(role_title) == False:
        return False

    if await has_user_record(tg_id) == False:
        return False

    user_record = await get_user_record(tg_id)
    user_record_dict = dict(user_record)

    user_role_DAO = UserRoleDAO()
    user_role_record = await user_role_DAO.get(user_id=user_record_dict["User_id"], role_title=role_title)

    return user_role_record != None


async def get_roles(tg_id: int) -> List[str]:
    user_role_DAO = UserRoleDAO()
    roles = []

    if await has_user_record(tg_id):
        user_record = await get_user_record(tg_id)
        user_record_dict = dict(user_record)
        user_role_records = await user_role_DAO.get_many(user_id=user_record_dict["User_id"])

        for user_role_record in user_role_records:
            user_role_record_dict = dict(user_role_record)

            if ROLE_TITLES.__contains__(user_role_record_dict['UserRole_role_title']):
                roles.append(user_role_record_dict["UserRole_role_title"])

    return roles


async def add_role(tg_id: int, role_title: str):
    user_record = await get_user_record(tg_id)
    user_record_dict = dict(user_record)

    user_role_DAO = UserRoleDAO()
    await user_role_DAO.create(user_id=user_record_dict["User_id"], role_title=role_title)


async def remove_role(tg_id: int, role_title: str):
    if await has_user_record(tg_id):
        if await has_role(tg_id, role_title):
            user_record = await get_user_record(tg_id)
            user_record_dict = dict(user_record)
            user_id = user_record_dict["User_id"]

            user_role_DAO = UserRoleDAO()
            user_role_record = await user_role_DAO.get(user_id=user_id, role_title=role_title)
            user_role_record_dict = dict(user_role_record)
            user_role_id = user_role_record_dict['UserRole_id']

        await user_role_DAO.delete_by_id(user_role_id)


async def get_user_language_key(tg_id) -> str:
    role_titles = await get_roles(tg_id)

    for title in role_titles:
        if title in LANGUAGE_KEYS:
            return title
    
    await change_language_for_user(tg_id, RU_KEY)
    return RU_KEY


async def change_language_for_user(tg_id: int, language_key: str):
    await change_role_for_user(tg_id, language_key, LANGUAGE_KEYS)


async def change_who_for_user(tg_id: int, who_role_title: str):
    await change_role_for_user(tg_id, who_role_title, WHO_ROLE_TITLES)


async def change_role_for_user(tg_id: int, role_title: str, role_titles: List[str]):
    if role_title in role_titles:
        if await has_user_record(tg_id):
            for title in role_titles:
                if await has_role(tg_id, title):
                    await remove_role(tg_id, title)

            await add_role(tg_id, role_title)
