from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..models.models import Offer
from ..schemas.offer_schemas import OfferCreate, OfferRead, OfferUpdate
from ..database import get_session
from typing import List

router = APIRouter(prefix="/api/offer", tags=["Offer"])


@router.post("/", response_model=OfferRead)
def create_offer(offer: OfferCreate, db: Session = Depends(get_session)):
    new_offer = Offer(**offer.model_dump())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


@router.get("/", response_model=List[OfferRead])
def list_offers(db: Session = Depends(get_session)):
    return db.exec(select(Offer)).all()


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer_by_id(offer_id: int, db: Session = Depends(get_session)):
    offer = db.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


# Update
@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(offer_id: int, offer_data: OfferUpdate, db: Session = Depends(get_session)):
    offer = db.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    offer_data_dict = offer_data.model_dump(exclude_unset=True)
    for key, value in offer_data_dict.items():
        setattr(offer, key, value)

    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer


# Delete
@router.delete("/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_session)):
    offer = db.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return {"message": "Offer deleted successfully"}
