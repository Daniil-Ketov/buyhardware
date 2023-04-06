from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class HardwareType(SQLModel, TimeMixin, table=True):
    __tablename__ = "hardware_type"

    name: Optional[str] = Field(None, primary_key=True, nullable=False)
    desc: str

    hardware: List["Hardware"] = Relationship(
        back_populates="hardware_type")
