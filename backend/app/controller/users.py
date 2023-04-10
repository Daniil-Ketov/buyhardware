from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import ResponseSchema
from app.service.users import UserService
from app.repository.auth_repo import JWTBearer, JWTRepo


router = APIRouter(
    prefix="/users",
    tags=['Users'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_client_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    result = await UserService.get_client_profile(token['username'])
    return ResponseSchema(detail="Данные успешно получены", result=result)


@router.get("/manger", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_manager_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    result = await UserService.get_manager_profile(token['username'])
    return ResponseSchema(detail="Данные успешно получены", result=result)
