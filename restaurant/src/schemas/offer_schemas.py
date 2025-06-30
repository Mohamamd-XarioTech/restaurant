from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class OfferCreate(BaseModel):
    title: str
    description: Optional[str]
    original_price: float
    offer_price: float
    quantity: int
    start_datetime: datetime
    end_datetime: datetime
    restaurant_id: int
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class OfferRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    original_price: float
    offer_price: float
    quantity: int
    start_datetime: datetime
    end_datetime: datetime
    restaurant_id: int
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class OfferUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    original_price: Optional[float] = None
    offer_price: Optional[float] = None
    quantity: Optional[int] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    model_config = ConfigDict(orm_mode=True, from_attributes=True)
