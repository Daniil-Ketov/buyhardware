from fastapi import APIRouter, Depends, Security, Query
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import HardwareCreate, OrderSchema, PageResponse, ResponseSchema, HardwareTypeCreate
from app.service.shop_service import ShopService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.hardware import HardwareRepository
from app.repository.hardware_type import HardwareTypeRepository
from app.controller.permissions import is_manager_or_admin


router = APIRouter(prefix="/orders", tags=['Orders'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_order(order_form: OrderSchema,
                       credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    await ShopService.create_order_service(JWTRepo().extract_token(credentials)["username"], order_form)
    return ResponseSchema(detail="Заказ успешно создан")
