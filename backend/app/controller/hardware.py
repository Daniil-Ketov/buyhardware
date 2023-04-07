from fastapi import APIRouter, Depends, Security, Query
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import HardwareCreate, OrderSchema, PageResponse, ResponseSchema, HardwareTypeCreate
from app.service.shop_service import ShopService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.hardware import HardwareRepository
from app.repository.hardware_type import HardwareTypeRepository
from app.controller.permissions import allow_create_manager


router = APIRouter(prefix="/hardware", tags=['Hardware'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_hardware(
        create_form: HardwareCreate
):
    await HardwareRepository.create(create_form)
    return ResponseSchema(detail="Данные успешно созданы")


@router.post("/hardware_type", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_hardware_type(
        create_form: HardwareTypeCreate
):
    await HardwareTypeRepository.create(create_form)
    return ResponseSchema(detail="Данные успешно созданы")


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_hardware(page: int = 1,
                           limit: int = 10,
                           columns: str = Query(None, alias="columns"),
                           sort: str = Query(None, alias="sort"),
                           filter: str = Query(None, alias="filter")):
    result = await HardwareRepository.get_all(page, limit, columns, sort, filter)
    return ResponseSchema(detail="Успешно получены данные об оборудовании", result=result)
