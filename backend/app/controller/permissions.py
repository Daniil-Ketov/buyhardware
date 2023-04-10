from typing import List
from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
        username = JWTRepo().extract_token(credentials)['username']

        roles = await UserService().get_user_roles(username)

        allowed = False

        for role in roles:
            if role['role_name'] in self.allowed_roles:
                allowed = True

        if not allowed:
            raise HTTPException(
                status_code=403, detail="Доступ запрещён")


is_admin = RoleChecker(["admin"])
is_manager = RoleChecker(["manager"])
is_client = RoleChecker(["client"])
is_manager_or_admin = RoleChecker(["manager", "admin"])


def check_is_manager_or_admin(roles: List[str]):
    return 'manager' in roles or 'admin' in roles
