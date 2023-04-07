from typing import List
from app.model import HardwareOrder
from app.repository.base_repo import BaseRepo
from app.config import db, commit_rollback


class HardwareOrderRepository(BaseRepo):
    model = HardwareOrder

    @staticmethod
    async def create_list(hardware_order: List[HardwareOrder]):
        db.add_all(hardware_order)
        await commit_rollback()
