from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class CategoryCreate(BaseModel):
    name: str
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class CategoryRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(orm_mode=True, from_attributes=True)


CategoryRead.model_rebuild()
