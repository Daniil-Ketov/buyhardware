from datetime import date
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Client(SQLModel, TimeMixin, table=True):
    __tablename__ = "client"

    user_id: Optional[str] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        foreign_key="users.id"
    )
    user: Optional["Users"] = Relationship(back_populates="client")
    name: str
    address: str
    postal_address: str
    tin: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="client")
