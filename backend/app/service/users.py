from sqlalchemy.future import select
from app.model import Users, Client, Manager, Role, UsersRole
from app.repository.users import UsersRepository
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

    @staticmethod
    async def get_user_roles(username: str):
        query = select(Role.role_name).join_from(
            Role, UsersRole).join_from(UsersRole, Users).where(Users.username == username)
        return (await db.execute(query)).mappings().all()

    @staticmethod
    async def get_user_id_by_username(username: str):
        user = await UsersRepository.find_by_username(username)
        return user.id
