from fastapi import APIRouter, Depends, Security, Path
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import ResponseSchema, UpdateProfileSchema
from app.service.users import UserService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.users import UsersRepository
from app.controller.permissions import is_manager_or_admin


router = APIRouter(
    prefix="/users",
    tags=['Users'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    result = await UserService.get_user_profile(token["username"])
    return ResponseSchema(detail="Данные успешно получены", result=result)


@router.patch("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user_profile(
        update_form: UpdateProfileSchema,
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    result = await UserService.update_user_profile(token["username"], update_form)
    return ResponseSchema(detail="Данные успешно обновлены", result=result)


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def update_user_by_id(
        user_id: str = Path(..., alias="id"),
        *,
        update_form: UpdateProfileSchema
):
    user = await UsersRepository.get_by_id(user_id)
    result = await UserService.update_user_profile(user.username, update_form)
    return ResponseSchema(detail="Данные успешно обновлены", result=result)


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def delete_user(
        user_id: str = Path(..., alias="id"),
):
    await UserService.delete_user(user_id)
    return ResponseSchema(detail="Данные успешно удалены")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_user_by_id(
        user_id: str = Path(..., alias="id")
):
    user = await UsersRepository.get_by_id(user_id)
    result = await UserService.get_user_profile(user.username)
    return ResponseSchema(detail="Данные о пользователе с данным id успешно извлечены", result=result)


@router.get("/all/", response_model=ResponseSchema, response_model_exclude_none=True, dependencies=[Depends(JWTBearer()), Depends(is_manager_or_admin)])
async def get_all_users():
    result = await UserService.get_all_users()
    return ResponseSchema(detail="Успешно получены данные о пользователях", result=result)
