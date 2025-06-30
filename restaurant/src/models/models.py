from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    restaurants: List["Restaurant"] = Relationship(back_populates="category")


class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="restaurants")

    offers: List["Offer"] = Relationship(back_populates="restaurant")


class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    original_price: float
    offer_price: float
    quantity: int

    start_datetime: datetime
    end_datetime: datetime

    restaurant_id: int = Field(foreign_key="restaurant.id")
    restaurant: Optional[Restaurant] = Relationship(back_populates="offers")


class Favorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Follow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    offer_id: int = Field(foreign_key="offer.id")

    buyer_id: str = Field(nullable=False)
    phone: str
    address: str
    quantity: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
