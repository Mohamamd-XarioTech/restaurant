from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class FavoriteCreate(BaseModel):
    user_id: int
    restaurant_id: int
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class FollowRead(BaseModel):
    id: int
    user_id: str
    restaurant_id: int
    model_config = ConfigDict(orm_mode=True, from_attributes=True)
