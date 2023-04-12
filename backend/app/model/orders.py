from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.model.mixins import TimeMixin


class Orders(SQLModel, TimeMixin, table=True):
    __tablename__ = "orders"

    id: str = Field(None, primary_key=True, nullable=False)
    user_id: str = Field(None, foreign_key="users.id", nullable=False)
    total: float
    shipment_deadline: date

    hardware_order: List["HardwareOrder"] = Relationship(
        back_populates="order")
    status_changes: List["StatusChanges"] = Relationship(
        back_populates="orders")
    user: Optional["Users"] = Relationship(back_populates="orders")
