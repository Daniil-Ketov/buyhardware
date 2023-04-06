from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class HardwareOrder(SQLModel, table=True):
    __tablename__ = "HardwareOrder"

    hardware_id: Optional[str] = Field(
        default=None, foreign_key="hardware.id", primary_key=True)
    order_id: Optional[str] = Field(
        default=None, foreign_key="orders.id", primary_key=True)

    order: Optional["Orders"] = Relationship(back_populates="hardware_order")
