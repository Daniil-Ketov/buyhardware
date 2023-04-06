from app.model import Contracts
from app.repository.base_repo import BaseRepo


class ContractsRepository(BaseRepo):
    model = Contracts
