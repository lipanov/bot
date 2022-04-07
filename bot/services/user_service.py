from asyncpg import Record
from typing import List
from DAO import UserDAO, UserRoleDAO


async def has_user_record(tg_id: int) -> bool:
    user_record = await get_user_record(tg_id)
    return user_record != None


async def get_user_record(tg_id: int) -> Record:
    user_DAO = UserDAO()
    user_record = await user_DAO.get(tg_id=tg_id)
    return user_record


async def get_user_roles(tg_id: int) -> List[str]:
    user_role_DAO = UserRoleDAO()
    roles = []

    if await has_user_record(tg_id):
        user_record = await get_user_record(tg_id)
        user_record_dict = dict(user_record)
        user_role_records = await user_role_DAO.get_many(user_id=user_record_dict["User_id"])

        for user_role_record in user_role_records:
            user_role_record_dict = dict(user_role_record)
            roles.append(user_role_record_dict["UserRole_role_title"])

    return roles


async def create_user(tg_id: int, name: str):
    user_DAO = UserDAO()
    await user_DAO.create(tg_id=tg_id, name=name)


async def has_role(tg_id: int, role_title: str) -> bool:
    if await has_user_record(tg_id) == False:
        return False

    user_record = await get_user_record(tg_id)
    user_record_dict = dict(user_record)

    user_role_DAO = UserRoleDAO()
    user_role_record = await user_role_DAO.get(user_id=user_record_dict["User_id"], role_title=role_title)

    return user_role_record != None


async def add_role(tg_id: int, role_title: str):
    user_record = await get_user_record(tg_id)
    user_record_dict = dict(user_record)

    user_role_DAO = UserRoleDAO()
    await user_role_DAO.create(user_id=user_record_dict["User_id"], role_title=role_title)
