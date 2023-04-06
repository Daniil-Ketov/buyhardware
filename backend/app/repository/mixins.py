import math
from typing import Generic, TypeVar
from uuid import uuid4
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.sql import select, or_, text, func, column
from app.schema import PersonCreate, PageResponse
from app.config import db, commit_rollback
from app.model import Person


T = TypeVar("T")


class PaginationMixin:

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
        """ Retrieve all objects """
        query = select(from_obj=cls.model, columns="*")

        # Select columns dynamically
        if columns is not None and columns != "all":
            # We need column format data like this -> [column(cn1), column(cn2) ...]
            query = select(from_obj=cls.model,
                           columns=convert_columns(columns))

        # Select filter dynamically
        if filter is not None and filter != "null":
            # We need filter format data like this -> {'field1': 'an', 'field2': 'an'}

            # Convert string to dict format
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # Check every key in dict. Are there any table attributes that same as the dict key?
            for attr, value in criteria.items():
                _attr = getattr(cls.model, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # Select sort dynamically
        if sort is not None and sort != "null":
            # We need sort format data like this -> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # Count query
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # Pagination
        query = (query.offset(offset_page * limit).limit(limit))

        # Total record
        total_record = (await db.execute(count_query)).scalar() or 0

        # Total page
        total_page = math.ceil(total_record / limit)

        # Result
        result = (await db.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )


def convert_sort(sort: str) -> str:
    """ Convert sort string to sqlalchemy sort string """
    return ','.join(sort.split('-'))


def convert_columns(columns: str) -> list:
    """ Convert columns string to list """
    return list(map(lambda x: column(x), columns.split('-')))
