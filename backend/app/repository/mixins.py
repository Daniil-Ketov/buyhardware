from sqlalchemy.future import select
import math
from typing import Generic, TypeVar
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.sql import select, or_, text, func, column
from app.schema import PageResponse
from app.config import db, commit_rollback


T = TypeVar("T")


T = TypeVar("T")


class RetrieveMixin:
    """
    Миксин для получения объектов из базы данных.
    """

    model = Generic[T]

    @classmethod
    async def get_all(cls):
        query = select(cls.model)
        return (await db.execute(query)).scalars.all()

    @classmethod
    async def get_by_id(cls, model_id: str):
        query = select(cls.model).where(cls.model.id == model_id)
        return (await db.execute(query)).scalar_one_or_none()


class CreateMixin:
    """
    Миксин для создания объектов в базе данных.
    """
    model = Generic[T]

    @classmethod
    async def create(cls, **kwargs):
        model = cls.model(**kwargs)
        db.add(model)
        await commit_rollback()
        return model


class UpdateMixin:
    """
    Миксин для обновления объектов в базе данных.
    """
    model = Generic[T]

    @classmethod
    async def update(cls, model_id: str, **kwargs):
        query = sql_update(cls.model).where(
            cls.model.id == model_id).values(**kwargs).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()


class DeleteMixin:
    """
    Миксин для удаления объектов из базы данных.
    """
    model = Generic[T]

    @classmethod
    async def delete(cls, model_id: str):
        query = sql_delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        await commit_rollback()


class RetrieveCreateMixin(RetrieveMixin, CreateMixin):
    """
    Миксин для получения и создания объектов в базе данных.
    """
    model = Generic[T]


class RetrieveUpdateMixin(RetrieveMixin, UpdateMixin):
    """
    Миксин для получения и обновления объектов в базе данных.
    """
    model = Generic[T]


class RetrieveCreateUpdateMixin(RetrieveMixin, CreateMixin, UpdateMixin):
    """
    Миксин для получения, создания и обновления объектов в базе данных.
    """
    model = Generic[T]


class RetrieveCreateDeleteMixin(RetrieveMixin, CreateMixin, DeleteMixin):
    """
    Миксин для получения, создания и удаления объектов в базе данных.
    """
    model = Generic[T]


class PaginationMixin:
    """
    Миксин для постраничного вывода объектов из базы данных.
    """

    model = Generic[T]

    @staticmethod
    async def get_all(
        cls,
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
    ):
        """ Получить все объекты """
        query = select(from_obj=cls.model, columns="*")

        # Выбрать только нужные столбцы
        if columns is not None and columns != "all":
            # Нам нужен такой формат столбцов -> [column(cn1), column(cn2) ...]
            query = select(from_obj=cls.model,
                           columns=convert_columns(columns))

        # Выбрать фильтр динамически
        if filter is not None and filter != "null":
            # Нам нужно отфильтровать данные в таком формате -> {'field1': 'an', 'field2': 'an'}

            # Преобразовать строку в словарь
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # Проверяем каждый ключ в словаре на схожесть с атрибутами таблицы
            for attr, value in criteria.items():
                _attr = getattr(cls.model, attr)

                # Формат фильтрации
                search = "%{}%".format(value)

                # Список критериев
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # Выбораем сортировку динамически
        if sort is not None and sort != "null":
            # Нам нужно отсортировать данные в таком формате -> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # Счетчик запроса
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # Пагинация
        query = (query.offset(offset_page * limit).limit(limit))

        # Итоговое количество записей
        total_record = (await db.execute(count_query)).scalar() or 0

        # Итоговое количество страниц
        total_page = math.ceil(total_record / limit)

        # Результат
        result = (await db.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )


def convert_sort(sort: str) -> str:
    """ Преобразование сортировочной строки в сортировочную строку sqlalchemy """
    return ','.join(sort.split('-'))


def convert_columns(columns: str) -> list:
    """ Преобразовать строку столбцов в список """
    return list(map(lambda x: column(x), columns.split('-')))
