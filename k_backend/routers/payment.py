from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select

from k_backend.schemas.account import Account

from ..auth import get_client
from ..db import get_session
from ..schemas.payment import (
    Payment,
    PaymentCreateDetailed,
    PaymentEntry,
    PaymentRead,
    PaymentReadDetailed,
    PaymentType,
    Transaction,
)
from ..util import CustomValidationError

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

EXAMPLES = {
    "create": {
        "Expense": {
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
        },
        "Income": {
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
        },
        "Transfer with fee": {
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
        },
        "Exchange currency with fee": {
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
        },
    }
}


@payment_router.post("", name="Create Payment", response_model=PaymentReadDetailed)
def create(
    *,
    session: Session = Depends(get_session),
    body: PaymentCreateDetailed = Body(examples=EXAMPLES["create"]),
):
    # Calculate total
    if body.payment.type in (PaymentType.Expense, PaymentType.Income):
        if body.payment.total is not None:
            raise CustomValidationError(
                "Total field is not allowed for expense or income",
                ("body", "payment", "total"),
            )
        entries_total = sum([entry.amount * entry.quantity for entry in body.entries])
        transaction_total = sum(
            [transaction.amount for transaction in body.transactions]
        )
        if entries_total != transaction_total:
            raise CustomValidationError(
                f"Entries total {entries_total} does not"
                f" match transaction total {transaction_total}",
                ("body", "__root__"),
            )
        body.payment.total = transaction_total
    elif body.payment.type is PaymentType.Transfer:
        if body.payment.total is None:
            raise CustomValidationError(
                "Total field is required for transfer", ("body", "payment", "total")
            )
    elif body.payment.type is PaymentType.Exchange:
        if body.payment.total is None:
            raise CustomValidationError(
                "Total field is required for exchange", ("body", "payment", "total")
            )
    else:
        raise CustomValidationError(
            f"Unknown type {body.payment.type}", ("body", "payment", "type")
        )

    # Store payment
    db_payment = Payment.from_orm(body.payment)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)

    # Store entries
    for entry in body.entries:
        entry.payment_id = db_payment.id
        db_entry = PaymentEntry.from_orm(entry)
        session.add(db_entry)
    session.commit()

    for index, transaction in enumerate(body.transactions):
        # Modify account balance
        account = session.query(Account).get(transaction.account_id)
        if not account:
            raise CustomValidationError(
                f"Account with id: {transaction.account_id} does not exist",
                ("body", "transactions", index, "account_id"),
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
        transaction.payment_id = db_payment.id
        transaction.timestamp = body.payment.timestamp
        transaction.timezone = body.payment.timezone
        db_transaction = Transaction.from_orm(transaction)
        session.add(db_transaction)
    session.commit()

    new_payment = session.get(Payment, db_payment.id)
    return new_payment


@payment_router.get("", name="Read Payments", response_model=list[PaymentReadDetailed])
def reads(*, session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments


@payment_router.patch("", name="Update Payment", response_model=PaymentRead)
def update(*, session: Session = Depends(get_session), payment: Payment):
    session.merge(payment)
    session.commit()
    session.refresh(payment)
    return payment


@payment_router.get("/{id}", name="Read Payment", response_model=PaymentReadDetailed)
def read(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    return payment


@payment_router.delete("/{id}", name="Delete Payment")
def delete(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
