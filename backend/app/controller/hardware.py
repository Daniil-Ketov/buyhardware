from fastapi import APIRouter, Depends, Query, Path
from uuid import uuid4
from app.schema import HardwareCreate, ResponseSchema, HardwareTypeCreate
from app.repository.auth_repo import JWTBearer
from app.repository.hardware import HardwareRepository
from app.repository.hardware_type import HardwareTypeRepository
from app.controller.permissions import is_manager_or_admin


router = APIRouter(prefix="/hardware", tags=['Hardware'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def create_hardware(
        create_form: HardwareCreate
):
    await HardwareRepository.create(id=str(uuid4()), **create_form.dict())
    return ResponseSchema(detail="Данные успешно созданы")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def update_hardware(
        hardware_id: str = Path(..., alias="id"),
        *,
        update_form: HardwareCreate
):
    await HardwareRepository.update(hardware_id, update_form)
    return ResponseSchema(detail="Данные успешно обновлены")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_hardware(
        hardware_id: str = Path(..., alias="id"),
):
    await HardwareRepository.delete(hardware_id)
    return ResponseSchema(detail="Данные успешно удалены")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_hardware_by_id(
        hardware_id: str = Path(..., alias="id")
):
    result = await HardwareRepository.get_by_id(hardware_id)
    return ResponseSchema(detail="Данные об оборудовании с данным id успешно извлечены", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_hardware(page: int = 1,
                           limit: int = 10,
                           columns: str = Query(None, alias="columns"),
                           sort: str = Query(None, alias="sort"),
                           filter: str = Query(None, alias="filter")):
    result = await HardwareRepository.get_all(page, limit, columns, sort, filter)
    return ResponseSchema(detail="Успешно получены данные об оборудовании", result=result)


@router.post("/type/", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def create_hardware_type(
        create_form: HardwareTypeCreate
):
    await HardwareTypeRepository.create(**create_form.dict())
    return ResponseSchema(detail="Данные успешно созданы")


@router.get("/type/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_hardware_type():
    result = await HardwareTypeRepository.get_all()
    print(result)
    return ResponseSchema(detail="Успешно получены данные о типах оборудования", result=result)


@router.patch("/type/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def update_hardware(
        hardware_type_id: str = Path(..., alias="id"),
        *,
        update_form: HardwareTypeCreate
):
    await HardwareTypeRepository.update(hardware_type_id, update_form)
    return ResponseSchema(detail="Данные успешно обновлены")


@router.delete("/type/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_hardware(
        hardware_type_id: str = Path(..., alias="id"),
):
    await HardwareTypeRepository.delete(hardware_type_id)
    return ResponseSchema(detail="Данные успешно удалены")
