from datetime import date
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Manager(SQLModel, TimeMixin, table=True):
    __tablename__ = "manager"

    user_id: Optional[str] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        foreign_key="users.id"
    )
    user: Optional["Users"] = Relationship(back_populates="users")
    first_name: str
    second_name: str
    patronym: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="manager")
