from app.model import HardwareOrder
from app.repository.base_repo import BaseRepo


class HardwareOrderRepository(BaseRepo):
    model = HardwareOrder
