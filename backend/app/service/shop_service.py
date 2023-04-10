from uuid import uuid4
from fastapi import HTTPException
from app.schema import OrderSchema
from app.model import Hardware, HardwareOrder, Orders, Users
from app.model.status_changes import StatusChanges, Status
from app.repository.hardware import HardwareRepository
from app.repository.hardware_order import HardwareOrderRepository
from app.repository.status_changes import StatusChangesRepository
from app.repository.orders import OrdersRepository
from app.repository.users import UsersRepository


class ShopService:

    @staticmethod
    async def create_order_service(username: str, order: OrderSchema):
        _order_id = str(uuid4())
        _user: Users = await UsersRepository.find_by_username(username)
        _status_change_id = str(uuid4())

        if not _user:
            raise HTTPException(
                status_code=400, detail="Пользователь не найден")
        _hardware_order = []
        _total = 0
        for item in order.items:
            _hardware: Hardware = await HardwareRepository.get_by_id(item.id)
            _value = _hardware.price * int(item.volume)
            _total += _value
            _hardware_order.append(HardwareOrder(hardware_id=item.id,
                                                 order_id=_order_id,
                                                 volume=item.volume,
                                                 value=_value))
        _order = Orders(id=_order_id,
                        user_id=_user.id,
                        total=_total,
                        shipment_deadline=order.shipment_deadline)

        _status_change = StatusChanges(id=_status_change_id,
                                       orders_id=_order_id,
                                       status=Status.CREATED)

        await OrdersRepository.create(**_order.dict())
        await HardwareOrderRepository.create_list(_hardware_order)
        await StatusChangesRepository.create(**_status_change.dict())

        return _order_id
