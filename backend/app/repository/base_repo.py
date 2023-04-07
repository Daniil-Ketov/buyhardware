from typing import Generic, TypeVar
from app.repository.mixins import RetrieveCreateUpdateMixin, DeleteMixin


T = TypeVar("T")


class BaseRepo(RetrieveCreateUpdateMixin, DeleteMixin):
    """ Класс для работы с базой данных """
    model = Generic[T]
