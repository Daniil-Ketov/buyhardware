from fastapi import APIRouter, Security, Path
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from app.schema import ResponseSchema
from app.service.shop_service import ShopService
from app.service.contract_service import ContractService
from app.repository.auth_repo import JWTBearer, JWTRepo


router = APIRouter(prefix="/contracts", tags=['Contracts'])


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_contract(
        order_id: str = Path(..., alias="id"),
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo().extract_token(credentials)
    if await ShopService.check_is_order_owner_or_staff(order_id, token["username"]):
        file = await ContractService.create_contract(order_id)
    return HTMLResponse(file)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_contract():
    file = await ContractService.get_blank()
    return HTMLResponse(file)
