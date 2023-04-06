from app.model import StatusChanges
from app.repository.base_repo import BaseRepo


class StatusChangesRepository(BaseRepo):
    model = StatusChanges
