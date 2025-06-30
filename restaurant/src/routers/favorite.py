from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Favorite
from ..schemas.favorite_schemas import FavoriteCreate
from ..database import get_session
from sqlmodel import Session, select
from typing import List


router = APIRouter(prefix="/api/favorite", tags=["Favorite"])


@router.post("/")
def favorite_restaurant(data: FavoriteCreate, db: Session = Depends(get_session)):
    favorite = Favorite(**data.dict())
    db.add(favorite)
    db.commit()
    return {"message": "Favorited successfully"}


@router.get("/", response_model=List[Favorite])
def get_all_favorites(db: Session = Depends(get_session)):
    return db.exec(select(Favorite)).all()


@router.get("/{user_id}", response_model=List[Favorite])
def get_favorites_by_user(user_id: str, db: Session = Depends(get_session)):
    favorites = db.exec(select(Favorite).where(
        Favorite.user_id == user_id)).all()
    return favorites


@router.delete("/{user_id}/{restaurant_id}")
def unfavorite_restaurant(user_id: str, restaurant_id: int, db: Session = Depends(get_session)):
    favorite = db.exec(
        select(Favorite).where(Favorite.user_id == user_id,
                               Favorite.restaurant_id == restaurant_id)
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
    return {"message": "Unfavorited successfully"}
