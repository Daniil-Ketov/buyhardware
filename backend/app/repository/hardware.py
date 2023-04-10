from sqlalchemy.future import select
from app.config import db
from app.model.hardware import Hardware
from app.repository.base_repo import BaseRepo
from app.repository.mixins import PaginationMixin


class HardwareRepository(PaginationMixin, BaseRepo):
    model = Hardware

    @staticmethod
    async def find_by_name(name: str):
        query = select(Hardware).where(Hardware.name == name)
        return (await db.execute(query)).mappings().all()
