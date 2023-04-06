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


# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register_client_service(register: RegisterSchema):

        # Create uuid
        _user_id = str(uuid4())

        # Mapping request data to class entity table
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

        # Everyone who registers through our registration page makes the default as client
        _role = await RoleRepository.find_by_role_name("client")
        _users_role = UsersRole(users_id=_user_id, role_id=_role.id)

        # Checking the same username
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Username already exist")

        # Checking the same email
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exist")

        else:
            # Insert into tables
            await UsersRepository.create(**_users.dict())
            await ClientRepository.create(**_client.dict())
            await UsersRoleRepository.create(**_users_role.dict())

    @staticmethod
    async def register_manager_service(register: RegisterManagerSchema):

        # Create uuid
        _user_id = str(uuid4())

        # Mapping request data to class entity table
        _manager = Manager(user_id=_user_id,
                           first_name=register.first_name,
                           second_name=register.second_name,
                           patronym=register.patronym)

        _users = Users(id=_user_id,
                       username=register.username,
                       email=register.email,
                       password=pwd_context.hash(register.password),
                       phone_number=register.phone_number)

        # Everyone who registers through our registration page makes the default as client
        _role = await RoleRepository.find_by_role_name("manager")
        _users_role = UsersRole(users_id=_user_id, role_id=_role.id)

        # Checking the same username
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Username already exist")

        # Checking the same email
        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exist")

        else:
            # Insert into tables
            await UsersRepository.create(**_users.dict())
            await ManagerRepository.create(**_manager.dict())
            await UsersRoleRepository.create(**_users_role.dict())

    @staticmethod
    async def login_service(login: LoginSchema):
        _username = await UsersRepository.find_by_username(login.username)
        if _username is not None:
            if not pwd_context.verify(login.password, _username.password):
                raise HTTPException(status_code=400, detail="Invalid password")
            return JWTRepo(data={"username": _username.username}).generate_token()
        raise HTTPException(status_code=400, detail="Username not found")

    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _email = await UsersRepository.find_by_email(forgot_password.email)
        if _email is None:
            raise HTTPException(status_code=400, detail="Email not found")
        await UsersRepository.update_password(forgot_password.email,
                                              pwd_context.hash(forgot_password.new_password))


# Generate roles manually
async def generate_role():
    _role = await RoleRepository.find_by_list_role_name(["admin", "client", "manager"])
    if not _role:
        await RoleRepository.create_list(
            [Role(id=str(uuid4()), role_name="admin"),
             Role(id=str(uuid4()), role_name="client"),
             Role(id=str(uuid4()), role_name="manager")])
