from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..DataBase import get_db
from .. import models
from ..schemas import CreatePayment, ResPayment
from typing import List

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

@router.post("/create", response_model=ResPayment)
def create_payment(payment: CreatePayment, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == payment.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    payment_db = models.Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=models.PaymentStatus.SUCCESS  # or set logic for status
    )
    db.add(payment_db)
    db.commit()
    db.refresh(payment_db)
    return payment_db

@router.get("/get", response_model=List[ResPayment])
def get_payments(db: Session = Depends(get_db)):
    return db.query(models.Payment).all()

@router.get("/get/{payment_id}", response_model=ResPayment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment