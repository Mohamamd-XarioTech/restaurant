from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..database import get_session
from ..models.models import Order, Offer
from ..schemas.order_schemas import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/api/order", tags=["Order"])


@router.post("/", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_session)):
    offer = db.get(Offer, order.offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    if offer.quantity < order.quantity:
        raise HTTPException(
            status_code=400, detail=f"Only {offer.quantity} left in stock"
        )

    # Reduce available quantity
    offer.quantity -= order.quantity
    db.add(offer)

    new_order = Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[OrderRead])
def list_orders(db: Session = Depends(get_session)):
    return db.exec(select(Order)).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status in ["delivered", "cancelled"]:
        raise HTTPException(
            status_code=400, detail="Cannot update a delivered or cancelled order")

    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
