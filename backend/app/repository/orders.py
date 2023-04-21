from sqlalchemy.future import select
from app.model import Orders
from app.repository.base_repo import BaseRepo
from sqlalchemy import update as sql_update, delete as sql_delete
from app.config import db, commit_rollback


class OrdersRepository(BaseRepo):
    model = Orders

    @staticmethod
    async def find_by_user_id(user_id: str):
        query = select(Orders).where(Orders.user_id == user_id)
        return (await db.execute(query)).scalars().all()

    @staticmethod
    async def delete_by_user_id(user_id: str):
        query = sql_delete(Orders).where(
            getattr(Orders, user_id) == user_id)
        await db.execute(query)
        await commit_rollback()
