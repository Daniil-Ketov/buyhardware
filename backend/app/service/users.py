from sqlalchemy.future import select
from app.model import Users, Client, Manager, Role, UsersRole, Orders
from app.repository.users import UsersRepository
from app.repository.client import ClientRepository
from app.repository.manager import ManagerRepository
from app.service.shop_service import ShopService
from app.repository.user_role import UsersRoleRepository
from app.config import db
from app.schema import UpdateClientProfile, UpdateManagerProfile, UpdateUser
from fastapi import HTTPException


class UserService:

    @staticmethod
    async def get_client_profile(username: str):
        query = select(Users.username,
                       Users.email,
                       Users.phone_number,
                       Client.name,
                       Client.address,
                       Client.postal_address,
                       Client.tin).join_from(Users, Client).where(Users.username == username)
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def get_manager_profile(username: str):
        query = select(Users.username,
                       Users.email,
                       Users.phone_number,
                       Manager.first_name,
                       Manager.second_name,
                       Manager.patronym).join_from(Users, Manager).where(Users.username == username)
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def get_user_profile(username: str):
        roles = await UsersRepository.get_user_roles(username)

        if 'client' in roles:
            return await UserService.get_client_profile(username)

        elif 'manager' in roles:
            return await UserService.get_manager_profile(username)

        else:
            raise HTTPException(
                status_code=400, detail='У данного пользователя нет прав на владение профилем')

    @staticmethod
    async def update_user_profile(username: str, update_form):
        roles = await UsersRepository.get_user_roles(username)
        user_id = await UsersRepository.get_user_id_by_username(username)

        if not user_id:
            raise HTTPException(
                status_code=404, detail='Пользователь не найден')

        if 'client' in roles:
            _client_form = UpdateClientProfile(**update_form.dict())
            _user_form = UpdateUser(**update_form.dict())
            await UsersRepository.update(user_id, **_user_form.dict())
            await ClientRepository.update(user_id, **_client_form.dict())

        elif 'manager' in roles:
            _manager_form = UpdateManagerProfile(**update_form.dict())
            _user_form = UpdateUser(**update_form.dict())
            await UsersRepository.update(user_id, **_user_form.dict())
            await ManagerRepository.update(user_id, **_manager_form.dict())

        else:
            raise HTTPException(
                status_code=400, detail='У данного пользователя нет прав на владение профилем')

    @staticmethod
    async def delete_user(user_id: str):
        user = await UsersRepository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=404, detail='Пользователь не найден')

        roles = await UsersRepository.get_user_roles(user.username)

        if 'client' in roles:
            await ClientRepository.delete(user_id)
            await UsersRoleRepository.delete(user_id)
            query = select(Orders.id, Users.username).join_from(
                Orders, Users).where(Orders.user_id == user_id)
            orders = (await db.execute(query)).mappings().all()
            for order in orders:
                await ShopService.delete_order_service(order.id, order.username)
            await UsersRepository.delete(user_id)

        elif 'manager' in roles:
            await ManagerRepository.delete(user_id)
            await UsersRoleRepository.delete(user_id)
            query = select(Orders.id, Users.username).join_from(
                Orders, Users).where(Orders.user_id == user_id)
            orders = (await db.execute(query)).mappings().all()
            for order in orders:
                await ShopService.delete_order_service(order.id, order.username)
            await UsersRepository.delete(user_id)

        else:
            await UsersRoleRepository.delete(user_id)
            query = select(Orders.id, Users.username).join_from(
                Orders, Users).where(Orders.user_id == user_id)
            orders = (await db.execute(query)).mappings().all()
            for order in orders:
                await ShopService.delete_order_service(order.id, order.username)
            await UsersRepository.delete(user_id)

    @staticmethod
    async def get_all_users():
        users_map = await UsersRepository.get_all()
        users = []
        for user in users_map:
            roles = await UsersRepository.get_user_roles(user['username'])
            t_roles = []
            if 'client' in roles:
                t_roles.append('client')
            if 'manager' in roles:
                t_roles.append('manager')
            if 'admin' in roles:
                t_roles.append('admin')
            users.append(dict(user))
            users[-1]['roles'] = t_roles
        return users
