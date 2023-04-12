from app.model import Users, Role, UsersRole
from app.repository.base_repo import BaseRepo
from app.config import db, commit_rollback
from sqlalchemy import update as sql_update
from sqlalchemy.sql import select, column


class UsersRepository(BaseRepo):
    model = Users

    @staticmethod
    async def get_all():
        query = select(from_obj=Users, columns=[column('id'), column(
            'username'), column('email'), column('phone_number')])
        return (await db.execute(query)).mappings().all()

    @staticmethod
    async def find_by_username(username: str):
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_email(email: str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(email: str, password: str):
        query = sql_update(Users).where(Users.email == email).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_user_roles(username: str):
        query = select(Role.role_name).join_from(
            Role, UsersRole).join_from(UsersRole, Users).where(Users.username == username)
        return (await db.execute(query)).scalars().all()

    @staticmethod
    async def get_user_id_by_username(username: str):
        user = await UsersRepository.find_by_username(username)

        return user.id
