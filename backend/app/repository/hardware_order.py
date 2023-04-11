from typing import List
from sqlalchemy.future import select
from app.model import HardwareOrder
from app.repository.mixins import RetrieveCreateMixin
from sqlalchemy import update as sql_update, delete as sql_delete
from app.config import db, commit_rollback


class HardwareOrderRepository(RetrieveCreateMixin):
    model = HardwareOrder

    @staticmethod
    async def get_by_id(order_id, hardware_id):
        query = select(HardwareOrder).where(HardwareOrder.order_id ==
                                            order_id and HardwareOrder.hardware_id == hardware_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def create_list(hardware_order: List[HardwareOrder]):
        db.add_all(hardware_order)
        await commit_rollback()

    @staticmethod
    async def find_by_order_id(order_id: str):
        query = select(HardwareOrder).where(
            HardwareOrder.order_id == order_id)
        return (await db.execute(query)).scalars().all()

    @staticmethod
    async def update(order_id: str, **kwargs):
        query = sql_update(HardwareOrder).where(
            HardwareOrder.order_id == order_id).values(**kwargs).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(order_id):
        query = sql_delete(HardwareOrder).where(
            HardwareOrder.order_id == order_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete_one(order_id, hardware_id):
        query = sql_delete(HardwareOrder).where(
            HardwareOrder.order_id == order_id and HardwareOrder.hardware_id == hardware_id)
        await db.execute(query)
        await commit_rollback()
