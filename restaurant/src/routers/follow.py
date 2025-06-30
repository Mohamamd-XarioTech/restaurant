from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Follow
from ..schemas.follow_schemas import FollowCreate
from ..database import get_session
from sqlmodel import Session, select
from typing import List

router = APIRouter(prefix="/api/follow", tags=["Follow"])


@router.post("/")
def follow_restaurant(data: FollowCreate, db: Session = Depends(get_session)):
    new_follow = Follow(**data.model_dump())
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow


@router.get("/", response_model=List[Follow])
def get_all_follows(db: Session = Depends(get_session)):
    return db.exec(select(Follow)).all()


@router.get("/{user_id}", response_model=List[Follow])
def get_follows_by_user(user_id: str, db: Session = Depends(get_session)):
    follows = db.exec(select(Follow).where(Follow.user_id == user_id)).all()
    return follows


@router.delete("/{user_id}/{restaurant_id}")
def unfollow_restaurant(user_id: str, restaurant_id: int, db: Session = Depends(get_session)):
    follow = db.exec(
        select(Follow).where(Follow.user_id == user_id,
                             Follow.restaurant_id == restaurant_id)
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Follow not found")

    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed successfully"}
