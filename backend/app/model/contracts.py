from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.model.mixins import TimeCreateMixin


class Contracts(SQLModel, TimeCreateMixin, table=True):
    __tablename__ = "contracts"

    id: str = Field(None, primary_key=True, nullable=False)
    order_id: str = Field(None, foreign_key="orders.id", nullable=False)

    orders: Optional["Orders"] = Relationship(
        back_populates="contract")
