from typing import List
from sqlalchemy.future import select
from app.model import HardwareOrder
from app.repository.mixins import RetrieveCreateMixin
from sqlalchemy import delete as sql_delete
from app.config import db, commit_rollback


class HardwareOrderRepository(RetrieveCreateMixin):
    model = HardwareOrder

    @staticmethod
    async def create_list(hardware_order: List[HardwareOrder]):
        db.add_all(hardware_order)
        await commit_rollback()

    @staticmethod
    async def find_by_order_id(order_id: str):
        query = select(HardwareOrder).where(
            HardwareOrder.order_id == order_id)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def delete(cls, order_id):
        query = sql_delete(HardwareOrder).where(
            HardwareOrder.order_id == order_id)
        await db.execute(query)
        await commit_rollback()
