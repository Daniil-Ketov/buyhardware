from fastapi import APIRouter, Security, Path, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import OrderSchema, ResponseSchema
from app.service.shop_service import ShopService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.orders import OrdersRepository


router = APIRouter(prefix="/orders", tags=['Orders'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_order(order_form: OrderSchema,
                       credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    await ShopService.create_order_service(token["username"], order_form)
    return ResponseSchema(detail="Заказ успешно создан")


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_orders(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    result = await ShopService.retrive_orders_by_username_service(token["username"])
    return ResponseSchema(detail="Заказы пользователя успешно получены", result=result)


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_order(
        order_id: str = Path(..., alias="id"),
        *,
        update_form: OrderSchema,
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo().extract_token(credentials)
    if await ShopService.check_is_order_owner_or_staff(order_id, token["username"]):
        await ShopService.update_order_service(order_id, token["username"], update_form)
        return ResponseSchema(detail="Данные успешно обновлены")
    raise HTTPException(
        status_code=403, detail="Нет прав на обновление заказа")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_order(
        order_id: str = Path(..., alias="id"),
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo().extract_token(credentials)
    result = await ShopService.delete_order_service(order_id, token["username"])
    return ResponseSchema(detail="Данные успешно удалены", result=result)


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_order_by_id(
        order_id: str = Path(..., alias="id"),
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo().extract_token(credentials)
    if await ShopService.check_is_order_owner_or_staff(order_id, token["username"]):
        result = await OrdersRepository.get_by_id(order_id)
        return ResponseSchema(detail="Данные о заказе с данным id успешно извлечены", result=result)
    raise HTTPException(status_code=403, detail="Нет прав на просмотр заказа")
