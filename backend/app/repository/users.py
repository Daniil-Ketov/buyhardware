from app.model.users import Users
from app.repository.base_repo import BaseRepo
from app.config import db, commit_rollback
from sqlalchemy import update as sql_update
from sqlalchemy.future import select


class UsersRepository(BaseRepo):
    model = Users

    @classmethod
    async def find_by_username(self, username: str):
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()

    @classmethod
    async def find_by_email(self, email: str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()

    @classmethod
    async def update_password(self, email: str, password: str):
        query = sql_update(Users).where(Users.email == email).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
