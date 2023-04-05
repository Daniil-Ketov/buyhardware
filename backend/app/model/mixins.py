from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime
from sqlmodel import Field


class TimeMixin(BaseModel):
    """Mixin to for datetime value of when entity was created and when it was last modified. """

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    )
