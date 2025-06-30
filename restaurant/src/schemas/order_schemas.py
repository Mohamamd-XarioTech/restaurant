from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from ..models.models import OrderStatus


class OrderCreate(BaseModel):
    offer_id: int
    buyer_id: str
    phone: str
    address: str
    quantity: int
    status: OrderStatus
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class OrderRead(BaseModel):
    id: int
    offer_id: int
    buyer_id: str
    phone: str
    address: str
    quantity: int
    status: OrderStatus
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class OrderUpdate(BaseModel):
    buyer_id: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[OrderStatus] = None
    model_config = ConfigDict(orm_mode=True, from_attributes=True)
