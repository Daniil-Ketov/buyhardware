import logging
import re
from datetime import date, datetime
from typing import Optional, TypeVar, Generic, List
from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel


T = TypeVar('T')


# Get root logger
logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):

    username: str
    email: str
    name: str
    password: str
    phone_number: str
    address: str
    postal_address: str
    tin: str

    # Phone number validation
    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # Regex phone number
        regex = r"^[\+]?[0-9]{1,3}-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Неподдерживаемый формат номера"})
        return v


class RegisterManagerSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    second_name: str
    patronym: str
    phone_number: str


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class HardwareCreate(BaseModel):
    name: str
    type: str
    price: int
    short_description: str
    full_description: str
    image: str

    @validator("price")
    def price_validation(cls, v):
        logger.debug(f"price in 2 validator: {v}")
        if v and v < 0:
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Цена не может быть отрицательной"})
        return v


class HardwareTypeCreate(BaseModel):
    name: str
    desc: str


class OrderItemSchema(BaseModel):
    id: str
    volume: str


class OrderSchema(BaseModel):
    items: List[OrderItemSchema]
    shipment_deadline: date

    @validator("shipment_deadline")
    def shipment_deadline_validation(cls, v):
        logger.debug(f"shipment_deadline in 2 validator: {v}")
        if v and v < datetime.now().date():
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Дата доставки не может быть меньше текущей"})
        return v


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
