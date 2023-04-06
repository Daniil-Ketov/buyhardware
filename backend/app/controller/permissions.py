from typing import List
from app.model import Users
from fastapi import Depends, Security, logger, HTTPException
from app.repository.users import UsersRepository


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, username: str):
        user = UsersRepository.find_by_username(username)

        allowed = False

        for role in user.roles:
            if role in self.allowed_roles:
                allowed = True

        if not allowed:
            logger.debug(
                f"User roles {user.roles} not in {self.allowed_roles}")
            raise HTTPException(
                status_code=403, detail="Доступ запрещён")


allow_create_manager = RoleChecker(["admin"])
