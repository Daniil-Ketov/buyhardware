from app.model import Orders
from app.repository.base_repo import BaseRepo


class OrdersRepository(BaseRepo):
    model = Orders
