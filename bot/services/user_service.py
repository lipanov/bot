from asyncpg import Record
from typing import List
from DAO import UserDAO, UserRoleDAO

ENROLLEE_GENERAL_ROLE_TITLE = 'Абитуриент'
ENROLLEE_FULL_TIME_ROLE_TITLE = 'Абитуриент (очная)'
ENROLLEE_PART_TIME_ROLE_TITLE = 'Абитуриент (очно-заочная)'
ENROLLEE_EXTRAMURAL_ROLE_TITLE = 'Абитуриент (заочная)'

STUDENT_FULL_TIME_ROLE_TITLE = 'Студент (очная)'
STUDENT_PART_TIME_ROLE_TITLE = 'Студент (очно-заочная)'
STUDENT_EXTRAMURAL_ROLE_TITLE = 'Студент (заочная)'

ADMIN_ROLE_TITLE = 'Администратор'

ROLE_TITLES = {
    ENROLLEE_GENERAL_ROLE_TITLE,
    ENROLLEE_FULL_TIME_ROLE_TITLE,
    ENROLLEE_PART_TIME_ROLE_TITLE,
    ENROLLEE_EXTRAMURAL_ROLE_TITLE,
    STUDENT_FULL_TIME_ROLE_TITLE,
    STUDENT_PART_TIME_ROLE_TITLE,
    STUDENT_EXTRAMURAL_ROLE_TITLE,
    ADMIN_ROLE_TITLE
}


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
