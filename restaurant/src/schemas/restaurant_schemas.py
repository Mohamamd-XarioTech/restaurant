from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from ..schemas.offer_schemas import OfferRead  # import OfferRead first


class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    category_id: Optional[int]
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class RestaurantRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]
    category_id: Optional[int]
    created_at: datetime
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class RestaurantWithOffers(RestaurantRead):
    offers: List[OfferRead] = []


class PaginatedRestaurants(BaseModel):
    page: int
    total_items: int
    total_pages: int
    restaurants: List[RestaurantWithOffers]
    model_config = ConfigDict(orm_mode=True, from_attributes=True)
