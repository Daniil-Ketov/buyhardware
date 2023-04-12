from app.model.client import Client
from app.repository.base_repo import BaseRepo


class ClientRepository(BaseRepo):
    model = Client
    id = "user_id"
