from sqlalchemy.future import select
from app.model import Users, Client, Manager
from app.config import db


class UserService:

    @staticmethod
    async def get_client_profile(username: str):
        query = select(Users.username,
                       Users.email,
                       Client.name,
                       Client.address,
                       Client.postal_address,
                       Client.tin).join_from(Users, Client).where(Users.username == username)
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def get_manager_profile(username: str):
        query = select(Users.username,
                       Users.email,
                       Manager.first_name,
                       Manager.second_name,
                       Manager.patronym).join_from(Users, Manager).where(Users.username == username)
        return (await db.execute(query)).mappings().one()
