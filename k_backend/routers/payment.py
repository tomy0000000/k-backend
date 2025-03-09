from collections.abc import Sequence
from datetime import date

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.openapi.models import Example
from pydantic_core import PydanticCustomError
from sqlmodel import Session

from k_backend.crud.payment import (
    create_payment,
    read_payment,
    read_payments,
)
from k_backend.crud.payment_entry import create_payment_entries
from k_backend.crud.transaction import create_transaction
from k_backend.logics.payment import validate_total
from k_backend.schemas.account import Account

from ..auth import get_client
from ..core.db import get_session
from ..schemas.api_models import PaymentCreateDetailed, PaymentReadDetailed
from ..schemas.payment import (
    Payment,
    PaymentBase,
    PaymentRead,
    PaymentType,
)

TAG_NAME = "Payment"
tag = {
    "name": TAG_NAME,
    "description": "Create and edit payment records",
}

payment_router = APIRouter(
    prefix="/payments",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)

EXAMPLES = {
    "create": {
        "Expense": Example(
            {
                "summary": "Expense",
                "value": {
                    "payment": {
                        "type": "Expense",
                        "timestamp": "2022-09-08T08:07:08.000",
                        "timezone": "Asia/Taipei",
                        "description": "Some payment description",
                    },
                    "transactions": [
                        {
                            "account_id": 2,
                            "amount": 60,
                        },
                        {
                            "account_id": 3,
                            "amount": 50,
                        },
                    ],
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
        ),
        "Income": Example(
            {
                "summary": "Income",
                "value": {
                    "payment": {
                        "type": "Income",
                        "timestamp": "2022-09-08T08:07:08.000",
                        "timezone": "Asia/Taipei",
                        "description": "Some payment description",
                    },
                    "transactions": [
                        {
                            "account_id": 2,
                            "amount": 50,
                        },
                        {
                            "account_id": 3,
                            "amount": 60,
                        },
                    ],
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
        ),
        "Transfer with fee": Example(
            {
                "summary": "Transfer with fee",
                "value": {
                    "payment": {
                        "type": "Transfer",
                        "timestamp": "2022-09-08T08:07:08.000",
                        "timezone": "Asia/Taipei",
                        "total": 60,
                        "description": "Some payment description",
                    },
                    "transactions": [
                        {
                            "account_id": 1,
                            "amount": -14,
                        },
                        {
                            "account_id": 2,
                            "amount": 60,
                        },
                        {
                            "account_id": 3,
                            "amount": -60,
                        },
                    ],
                    "entries": [
                        {
                            "category_id": 4,
                            "amount": 14,
                            "quantity": 1,
                            "description": "Fee",
                        },
                    ],
                },
            }
        ),
        "Exchange currency with fee": Example(
            {
                "summary": "Exchange currency with fee",
                "value": {
                    "payment": {
                        "type": "Exchange",
                        "timestamp": "2022-09-08T08:07:08.000",
                        "timezone": "Asia/Taipei",
                        "total": 100,
                        "description": "Some payment description",
                    },
                    "transactions": [
                        {
                            "account_id": 1,
                            "amount": -150,
                        },
                        {
                            "account_id": 2,
                            "amount": -3000,
                        },
                        {
                            "account_id": 4,
                            "amount": 100,
                        },
                    ],
                    "entries": [
                        {
                            "category_id": 4,
                            "amount": 150,
                            "quantity": 1,
                            "description": "Fee",
                        },
                    ],
                },
            }
        ),
    }
}


@payment_router.post("", name="Create Payment", response_model=PaymentReadDetailed)
def create(
    *,
    session: Session = Depends(get_session),
    body: PaymentCreateDetailed = Body(openapi_examples=EXAMPLES["create"]),
) -> PaymentBase:
    # Validate total
    try:
        validate_total(body)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=err.args[0]) from err

    # Store payment
    db_payment = create_payment(session, body.payment)
    payment_id = PaymentRead.model_validate(db_payment).id

    # Store entries
    create_payment_entries(session, body.entries, payment_id)

    for index, transaction in enumerate(body.transactions):
        # Modify account balance
        account = session.query(Account).get(transaction.account_id)
        if not account:
            raise PydanticCustomError(
                "account_not_found",
                f"Account with id: {transaction.account_id} does not exist",
                {"loc": ("body", "transactions", index, "account_id")},
            )
        if body.payment.type is PaymentType.Expense:
            account.balance -= transaction.amount
        elif body.payment.type in (
            PaymentType.Income,
            PaymentType.Transfer,
            PaymentType.Exchange,
        ):
            account.balance += transaction.amount
        session.add(account)
        # TODO: test what'll happen if two transactions with same account_id are added

        # Store Transactions
        transaction.payment_id = payment_id
        create_transaction(session, transaction)

    new_payment = session.get(Payment, payment_id)
    if new_payment is None:
        raise HTTPException(status_code=500, detail="Failed to create payment")
    return new_payment


@payment_router.get(
    "/{payment_id}", name="Read Payment", response_model=PaymentReadDetailed
)
def read(*, session: Session = Depends(get_session), payment_id: int) -> PaymentBase:
    payment = read_payment(session, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@payment_router.get("", name="Read Payments", response_model=list[PaymentReadDetailed])
def reads(
    *,
    session: Session = Depends(get_session),
    payment_date: date | None = None,
    category_id: int | None = None,
) -> Sequence[PaymentBase]:
    return read_payments(session, payment_date, category_id)


@payment_router.patch("", name="Update Payment", response_model=PaymentRead)
def update(*, session: Session = Depends(get_session), payment: Payment) -> PaymentBase:
    session.merge(payment)
    session.commit()
    session.refresh(payment)
    return payment


@payment_router.delete("/{id}", name="Delete Payment")
def delete(*, session: Session = Depends(get_session), id: int) -> None:
    payment = session.get(Payment, id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
