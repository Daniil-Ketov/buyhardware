import logging
import re
from datetime import date, datetime
from typing import Optional, TypeVar, Generic, List
from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
from app.model.status_changes import Status


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

    # Валидация номера телефона
    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # Регулярное выражение для проверки номера телефона
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

    # Валидация номера телефона
    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # Регулярное выражение для проверки номера телефона
        regex = r"^[\+]?[0-9]{1,3}-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Неподдерживаемый формат номера"})
        return v


class UpdateUser(BaseModel):
    email: str
    phone_number: str


class UpdateClientProfile(BaseModel):
    address: str
    postal_address: str
    tin: str


class UpdateManagerProfile(BaseModel):
    first_name: str
    second_name: str
    patronym: str


class UpdateProfileSchema(BaseModel):
    email: str
    phone_number: str
    name: Optional[str]
    first_name: Optional[str]
    second_name: Optional[str]
    patronym: Optional[str]
    address: Optional[str]
    postal_address: Optional[str]
    tin: Optional[str]

    # Валидация номера телефона

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validator: {v}")

        # Регулярное выражение для проверки номера телефона
        regex = r"^[\+]?[0-9]{1,3}-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail={
                                "status": "Bad request", "message": "Неподдерживаемый формат номера"})
        return v


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


class HardwareUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    price: Optional[int]
    short_description: Optional[str]
    full_description: Optional[str]
    image: Optional[str]

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


class StatusChangeSchema(BaseModel):
    status: Status
    orders_id: str


class HardwareOrderSchema(BaseModel):
    hardware_id: str
    order_id: str
    volume: int
    value: int


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
