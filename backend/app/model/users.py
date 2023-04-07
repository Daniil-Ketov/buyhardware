from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin
from .user_role import UsersRole


class Users(SQLModel, TimeMixin, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    phone_number: str
    password: str

    roles: List["Role"] = Relationship(
        back_populates="users", link_model=UsersRole)

    client: Optional["Client"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="users")
    manager: Optional["Manager"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="users")
    orders: Optional["Orders"] = Relationship(back_populates="user")
