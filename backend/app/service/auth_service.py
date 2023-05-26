from uuid import uuid4
from fastapi import HTTPException
from passlib.context import CryptContext
from app.schema import RegisterSchema, RegisterManagerSchema, LoginSchema, ForgotPasswordSchema
from app.model import Client, Manager, Users, UsersRole, Role
from app.repository.role import RoleRepository
from app.repository.users import UsersRepository
from app.repository.client import ClientRepository
from app.repository.manager import ManagerRepository
from app.repository.user_role import UsersRoleRepository
from app.repository.auth_repo import JWTRepo


# Шифрование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register_client_service(register: RegisterSchema):

        # Создание uuid
        _user_id = str(uuid4())

        # Маппинг данных запроса в класс сущности таблицы
        _client = Client(user_id=_user_id,
                         name=register.name,
                         address=register.address,
                         postal_address=register.postal_address,
                         tin=register.tin)

        _users = Users(id=_user_id,
                       username=register.username,
                       email=register.email,
                       password=pwd_context.hash(register.password),
                       phone_number=register.phone_number)

        # По умолчанию клиент становится клиентом при регистрации пользователя
        _role = await RoleRepository.find_by_role_name("client")
        _users_role = UsersRole(users_id=_user_id, role_id=_role.id)

        # Проверка на существование пользователя с таким же логином в базе данных
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Данный логин уже занят")

        # Проверка на существование пользователя с таким же email в базе данных
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(
                status_code=400, detail="Пользователь с таким email уже существует")

        else:
            # Добавление в базу данных
            await UsersRepository.create(**_users.dict())
            await ClientRepository.create(**_client.dict())
            await UsersRoleRepository.create(**_users_role.dict())

    @staticmethod
    async def register_manager_service(register: RegisterManagerSchema):

        # Создание uuid
        _user_id = str(uuid4())

        # Маппинг данных запроса в класс сущности таблицы
        _manager = Manager(user_id=_user_id,
                           first_name=register.first_name,
                           second_name=register.second_name,
                           patronym=register.patronym)

        _users = Users(id=_user_id,
                       username=register.username,
                       email=register.email,
                       password=pwd_context.hash(register.password),
                       phone_number=register.phone_number)

        # По умолчанию менеджер становится менеджером при регистрации пользователя
        _role = await RoleRepository.find_by_role_name("manager")
        _users_role = UsersRole(users_id=_user_id, role_id=_role.id)

        # Проверка на существование пользователя с таким же логином в базе данных
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Логин уже существует в системе")

        # Проверка на существование пользователя с таким же email в базе данных
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(
                status_code=400, detail="Email уже существует в системе")

        else:
            # Добавление в базу данных
            await UsersRepository.create(**_users.dict())
            await ManagerRepository.create(**_manager.dict())
            await UsersRoleRepository.create(**_users_role.dict())

    @staticmethod
    async def register_admin_service(register: RegisterManagerSchema):

        # Создание uuid
        _user_id = str(uuid4())

        # Маппинг данных запроса в класс сущности таблицы
        _manager = Manager(user_id=_user_id,
                           first_name=register.first_name,
                           second_name=register.second_name,
                           patronym=register.patronym)

        _users = Users(id=_user_id,
                       username=register.username,
                       email=register.email,
                       password=pwd_context.hash(register.password),
                       phone_number=register.phone_number)

        # По умолчанию менеджер становится менеджером при регистрации пользователя
        _role = await RoleRepository.find_by_list_role_name(['admin', 'manager'])
        _users_role1 = UsersRole(users_id=_user_id, role_id=_role[0].id)
        _users_role2 = UsersRole(users_id=_user_id, role_id=_role[1].id)

        # Проверка на существование пользователя с таким же логином в базе данных
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Логин уже существует в системе")

        # Проверка на существование пользователя с таким же email в базе данных
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(
                status_code=400, detail="Email уже существует в системе")

        else:
            # Добавление в базу данных
            await UsersRepository.create(**_users.dict())
            await ManagerRepository.create(**_manager.dict())
            await UsersRoleRepository.create(**_users_role1.dict())
            await UsersRoleRepository.create(**_users_role2.dict())

    @staticmethod
    async def login_service(login: LoginSchema):
        _username = await UsersRepository.find_by_username(login.username)
        if _username is not None:
            if not pwd_context.verify(login.password, _username.password):
                raise HTTPException(status_code=400, detail="Неверный пароль")
            return JWTRepo(data={"username": _username.username}).generate_token()
        raise HTTPException(
            status_code=400, detail="Пользователя с таким логином не существует")

    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _email = await UsersRepository.find_by_email(forgot_password.email)
        if _email is None:
            raise HTTPException(
                status_code=400, detail="Данный email не найден")
        await UsersRepository.update_password(forgot_password.email,
                                              pwd_context.hash(forgot_password.new_password))


# Ручная генерация ролей
async def generate_role():
    _role = await RoleRepository.find_by_list_role_name(["admin", "client", "manager"])
    if not _role:
        await RoleRepository.create_list(
            [Role(id=str(uuid4()), role_name="admin"),
             Role(id=str(uuid4()), role_name="client"),
             Role(id=str(uuid4()), role_name="manager")])
