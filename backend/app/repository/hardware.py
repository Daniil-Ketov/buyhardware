import base64
from sqlalchemy.future import select
from sqlalchemy import update as sql_update
from app.config import db, commit_rollback
from app.model.hardware import Hardware
from app.repository.base_repo import BaseRepo
from app.repository.mixins import PaginationMixin


class HardwareRepository(PaginationMixin, BaseRepo):
    model = Hardware

    @staticmethod
    async def find_by_name(name: str):
        query = select(Hardware).where(Hardware.name == name)
        return (await db.execute(query)).mappings().all()

    @staticmethod
    async def create(**hardware_form):

        # Конвертация изображения в base64
        if not hardware_form['image']:
            with open("./media/default_hardware.png", "rb") as d:
                default = base64.b64decode(d.read())
            hardware_form['image'] = "data:image/png;base64," + \
                default.decode('utf-8')

        _hardware = Hardware(**hardware_form)
        db.add(_hardware)
        await commit_rollback()
        return _hardware

    @staticmethod
    async def update(id: str, **hardware_form):
        if not hardware_form['image']:
            with open("./media/default_hardware.png", "rb") as d:
                default = base64.b64decode(d.read())
            hardware_form['image'] = "data:image/png;base64," + \
                default.decode('utf-8')

        query = sql_update(Hardware).where(
            Hardware.id == id).values({i: v for i, v in hardware_form.items() if v}).execution_options(
                synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
