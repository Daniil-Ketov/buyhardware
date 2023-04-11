from fastapi import APIRouter, Depends, Path
from uuid import uuid4
from app.schema import ResponseSchema, StatusChangeSchema
from app.repository.auth_repo import JWTBearer
from app.repository.status_changes import StatusChangesRepository
from app.controller.permissions import is_manager_or_admin


router = APIRouter(prefix="/status", tags=['Status'])


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def create_status(
        create_form: StatusChangeSchema
):
    await StatusChangesRepository.create(id=str(uuid4()), **create_form.dict())
    return ResponseSchema(detail="Данные успешно созданы")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def update_status(
        status_change_id: str = Path(..., alias="id"),
        *,
        update_form: StatusChangeSchema
):
    await StatusChangesRepository.update(status_change_id, update_form)
    return ResponseSchema(detail="Данные успешно обновлены")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_status(
        status_change_id: str = Path(..., alias="id"),
):
    await StatusChangesRepository.delete(status_change_id)
    return ResponseSchema(detail="Данные успешно удалены")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_status_by_id(
        status_change_id: str = Path(..., alias="id")
):
    result = await StatusChangesRepository.get_by_id(status_change_id)
    return ResponseSchema(detail="Данные о статусе с данным id успешно извлечены", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_all_status():
    result = await StatusChangesRepository.get_all()
    return ResponseSchema(detail="Успешно получены данные о статусах", result=result)
