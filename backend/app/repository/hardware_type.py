from app.model import HardwareType
from app.repository.base_repo import BaseRepo


class HardwareTypeRepository(BaseRepo):
    model = HardwareType
