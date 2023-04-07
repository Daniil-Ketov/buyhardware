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
    async def create_order_service(order: OrderSchema):

        _order_id = str(uuid4())
        _user_id = UsersRepository.find_by_username(order.username)['id']
        _status_change_id = str(uuid4())

        if not _user_id:
            raise HTTPException(
                status_code=400, detail="Пользователь не найден")

        _hardware_order = [HardwareOrder(hardware_id=item.id,
                                         order_id=_order_id,
                                         volume=item.volume,
                                         value=HardwareRepository.get_by_id(item.id)["price"] * item.volume)
                           for item in order.items]

        _total = sum([item.value for item in _hardware_order])

        _order = Orders(id=_order_id,
                        user_id=_user_id,
                        total=_total,
                        shipment_deadline=order.shipment_deadline)

        _status_change = StatusChanges(id=_status_change_id,
                                       orders_id=_order_id,
                                       status=Status.CREATED)

        await OrdersRepository.create(_order)
        await HardwareOrderRepository.create_many(_hardware_order)
        await StatusChangesRepository.create(_status_change)

        return _order_id
