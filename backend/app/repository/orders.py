from sqlalchemy.future import select
from app.model import Orders
from app.repository.base_repo import BaseRepo
from app.config import db


class OrdersRepository(BaseRepo):
    model = Orders

    @classmethod
    async def find_by_user_id(self, user_id: str):
        query = select(Orders).where(Orders.user_id == user_id)
        return (await db.execute(query)).mappings().all()
