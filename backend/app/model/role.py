from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin
from .user_role import UsersRole


class Role(SQLModel, TimeMixin, table=True):
    __tablename__ = "role"

    id: Optional[str] = Field(None, primary_key=True, nullable=True)
    role_name: str

    users: List["Users"] = Relationship(
        back_populates="roles", link_model=UsersRole)
