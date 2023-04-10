from sqlalchemy.future import select
from sqlalchemy import delete as sql_delete
from app.config import db, commit_rollback
from app.model import StatusChanges
from app.repository.base_repo import BaseRepo


class StatusChangesRepository(BaseRepo):
    model = StatusChanges

    @staticmethod
    async def find_by_order_id(order_id: str):
        query = select(StatusChanges).where(
            StatusChanges.orders_id == order_id)
        return (await db.execute(query)).scalars().all()

    @staticmethod
    async def delete_by_order_id(orders_id: str):
        query = sql_delete(StatusChanges).where(
            StatusChanges.orders_id == orders_id)
        await db.execute(query)
        await commit_rollback()
