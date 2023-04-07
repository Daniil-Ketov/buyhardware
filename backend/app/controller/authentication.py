from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import ResponseSchema, RegisterSchema, RegisterManagerSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.controller.permissions import allow_create_manager


router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post("/register_client", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_client_service(request_body)
    return ResponseSchema(detail="Данные успешно сохранены")


@router.post("/register_manager", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterManagerSchema):
    await AuthService.register_manager_service(request_body)
    return ResponseSchema(detail="Данные успешно сохранены")


@router.post("/login", response_model=ResponseSchema)
async def login(request_body: LoginSchema):
    token = await AuthService.login_service(request_body)
    return ResponseSchema(detail="Успешный вход",
                          result={"token_type": "Bearer", "access_token": token})


@router.post("/forgot_password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Данные успешно обновлены")
