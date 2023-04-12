from app.model.manager import Manager
from app.repository.base_repo import BaseRepo


class ManagerRepository(BaseRepo):
    model = Manager
    id = "user_id"
