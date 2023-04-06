from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Hardware(SQLModel, TimeMixin, table=True):
    __tablename__ = "hardware"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    type: Optional[str] = Field(None, foreign_key="hardware_type.name")
    price: int
    short_description: str
    full_description: str
    image: str

    hardware_type: Optional["HardwareType"] = Relationship(
        back_populates="hardware")
