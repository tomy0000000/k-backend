from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_client
from ..db import engine, get_session
from ..schemas.payment import (
    Payment,
    PaymentCreate,
    PaymentEntry,
    PaymentEntryCreate,
    PaymentRead,
    PaymentReadWithEntries,
)

TAG_NAME = "Payment"
tag = {
    "name": TAG_NAME,
    "description": "Create and edit payment records",
}

payment_router = APIRouter(
    prefix="/payment",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@payment_router.post(
    "",
    response_model=PaymentReadWithEntries,
    tags=[TAG_NAME],
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "Taipei with 3 entries": {
                            "summary": "Taipei with 3 entries",
                            "value": {
                                "payment": {
                                    "timestamp": "2022-09-08T08:07:08.000",
                                    "timezone": "Asia/Taipei",
                                    "description": "Some payment description",
                                },
                                "entries": [
                                    {
                                        "category_id": 1,
                                        "amount": 20,
                                        "quantity": 2,
                                        "description": "First entry",
                                    },
                                    {
                                        "category_id": 2,
                                        "amount": 30,
                                        "quantity": 2,
                                        "description": "Second entry",
                                    },
                                    {
                                        "category_id": 3,
                                        "amount": 10,
                                        "quantity": 1,
                                        "description": "Third entry",
                                    },
                                ],
                            },
                        }
                    }
                }
            }
        }
    },
)
def create_payment(
    *,
    session: Session = Depends(get_session),
    payment: PaymentCreate,
    entries: list[PaymentEntryCreate]
):
    # Calculate total
    payment.total = sum([entry.amount * entry.quantity for entry in entries])

    # Store payment
    db_payment = Payment.from_orm(payment)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)

    # Store entries
    for entry in entries:
        entry.payment_id = db_payment.id
        db_entry = PaymentEntry.from_orm(entry)
        session.add(db_entry)
    session.commit()

    new_payment = session.get(Payment, db_payment.id)
    return new_payment


@payment_router.get("", response_model=list[PaymentReadWithEntries], tags=[TAG_NAME])
def read_payments(*, session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments


@payment_router.patch("", response_model=PaymentRead, tags=[TAG_NAME])
def update_payment(*, session: Session = Depends(get_session), payment: Payment):
    session.merge(payment)
    session.commit()
    session.refresh(payment)
    return payment


@payment_router.get("/{id}", response_model=PaymentReadWithEntries, tags=[TAG_NAME])
def read_payment(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    return payment


@payment_router.delete("/{id}", tags=[TAG_NAME])
def delete_payment(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
