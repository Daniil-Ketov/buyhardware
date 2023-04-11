from fastapi import APIRouter, Depends, Path
from app.schema import ResponseSchema, HardwareOrderSchema
from app.repository.auth_repo import JWTBearer
from app.repository.hardware_order import HardwareOrderRepository
from app.controller.permissions import is_manager_or_admin


router = APIRouter(prefix="/hardware_orders", tags=['Hardware Orders'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def create_hardware_order(
        create_form: HardwareOrderSchema
):
    await HardwareOrderRepository.create(**create_form.dict())
    return ResponseSchema(detail="Данные успешно созданы")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def update_hardware_order(
        order_id: str = Path(..., alias="id"),
        *,
        update_form: HardwareOrderSchema
):
    await HardwareOrderRepository.update(order_id, update_form)
    return ResponseSchema(detail="Данные успешно обновлены")


@router.delete("/{order_id}/{hardware_id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_hardware_order_by_id(
        order_id: str = Path(..., alias="order_id"),
        hardware_id: str = Path(..., alias="hardware_id")
):
    await HardwareOrderRepository.delete_one(order_id, hardware_id)
    return ResponseSchema(detail="Данные успешно удалены")


@router.delete("/{order_id}/all/", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_hardware_order_by_order(
        order_id: str = Path(..., alias="order_id")
):
    await HardwareOrderRepository.delete(order_id)
    return ResponseSchema(detail="Данные успешно удалены")


@router.get("/{order_id}/{hardware_id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_hardware_order_by_id(
        order_id: str = Path(..., alias="order_id"),
        hardware_id: str = Path(..., alias="hardware_id")
):
    result = await HardwareOrderRepository.get_by_id(order_id, hardware_id)
    return ResponseSchema(detail="Данные об оборудовании в заказе с данным id успешно извлечены", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_all_hardware_order():
    result = await HardwareOrderRepository.get_all()
    return ResponseSchema(detail="Успешно получены данные об оборудовании в заказах", result=result)
