from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeCreateMixin


class Status(str, Enum):
    CREATED = "created"
    PACKING = "packing"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
    RECIEVED = "recieved"
    CANCELLED = "cancelled"


class StatusChanges(SQLModel, TimeCreateMixin, table=True):
    __tablename__ = "status_changes"

    id: str = Field(None, primary_key=True, nullable=False)
    status: Status
    orders_id: str = Field(None, foreign_key="orders.id")

    orders: Optional["Orders"] = Relationship(
        back_populates="status_changes")
