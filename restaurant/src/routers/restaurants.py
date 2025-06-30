from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from ..models.models import Restaurant, Offer
from ..schemas.restaurant_schemas import RestaurantCreate, RestaurantWithOffers, PaginatedRestaurants
from ..database import get_session
from typing import List, Optional
from datetime import datetime
from math import ceil


router = APIRouter(prefix="/api/restaurant", tags=["Restaurant"])


@router.post("/", response_model=RestaurantWithOffers)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_session),):
    db_restaurant = Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


@router.get("/", response_model=PaginatedRestaurants)
def list_restaurants(db: Session = Depends(get_session), page: int = Query(1, ge=1),
                     per_page: int = Query(10, ge=1, le=100),
                     search: Optional[str] = Query(
                         None, description="Search by restaurant name"),
                     category_id: Optional[int] = Query(
                         None, description="Filter by category id"),
                     active_offers_only: bool = Query(False, description="Only include active offers"),):

    query = select(Restaurant)

    # Search by name
    if search:
        query = query.where(Restaurant.name.ilike(f"%{search}%"))

    # Filter by category
    if category_id:
        query = query.where(Restaurant.category_id == category_id)

    # Pagination
    offset = (page - 1) * per_page
    restaurants = db.exec(query.offset(offset).limit(per_page)).all()

    # Total before pagination
    total_items = len(db.exec(query).all())

    offset = (page - 1) * per_page
    restaurants = db.exec(query.offset(offset).limit(per_page)).all()

    now = datetime.now()

    # Attach offers (and filter them if needed)
    result = []
    for r in restaurants:
        offers = r.offers
        if active_offers_only:
            offers = [o for o in offers if o.start_datetime <=
                      now <= o.end_datetime]
        result.append({
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "image": r.image,
            "category_id": r.category_id,
            "created_at": r.created_at,
            "offers": offers
        })

    response = PaginatedRestaurants(
        page=page,
        total_items=total_items,
        total_pages=ceil(total_items / per_page),
        restaurants=result
    )
    return response


@router.get("/search")
def search_restaurants(q: str = Query(...), db: Session = Depends(get_session)):
    results = db.exec(
        select(Restaurant).where(Restaurant.name.ilike(f"%{q}%"))
    ).all()
    return results
