from fastapi import APIRouter, Depends, Security, Query
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import HardwareCreate, OrderSchema, PageResponse, ResponseSchema, HardwareTypeCreate
from app.service.shop_service import ShopService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.hardware import HardwareRepository
from app.repository.hardware_type import HardwareTypeRepository
from app.controller.permissions import allow_create_manager


router = APIRouter(prefix="/orders", tags=['Orders'])


@router.post("/order", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_order(order_form: OrderSchema,
                       credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    order_form.username = JWTRepo().extract_token(credentials)["username"]
    await ShopService.create_order(order_form)
    return ResponseSchema(detail="Заказ успешно создан")
