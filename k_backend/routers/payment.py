from fastapi import APIRouter, Depends, HTTPException
from k_backend.schemas.account import Account
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.payment import (
    Payment,
    PaymentCategory,
    PaymentCreate,
    PaymentEntry,
    PaymentEntryCreate,
    PaymentRead,
    PaymentReadDetailed,
    Transaction,
    TransactionCreate,
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


@payment_router.post(
    "",
    response_model=PaymentReadDetailed,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "Expense": {
                            "summary": "Expense",
                            "value": {
                                "payment": {
                                    "category": "Expense",
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
                                    "category": "Income",
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
                                    "category": "Transfer",
                                    "timestamp": "2022-09-08T08:07:08.000",
                                    "timezone": "Asia/Taipei",
                                    "total": 60,
                                    "description": "Some payment description",
                                },
                                "transactions": [
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
    transactions: list[TransactionCreate],
    entries: list[PaymentEntryCreate],
):
    # Calculate total
    if payment.category in (PaymentCategory.Expense, PaymentCategory.Income):
        if payment.total is not None:
            raise CustomValidationError(
                "Total field is not allowed for expense or income",
                ("body", "payment", "total"),
            )
        entries_total = sum([entry.amount * entry.quantity for entry in entries])
        transaction_total = sum([transaction.amount for transaction in transactions])
        if entries_total != transaction_total:
            raise CustomValidationError(
                f"Entries total {entries_total} does not"
                f" match transaction total {transaction_total}",
                ("body", "__root__"),
            )
        payment.total = transaction_total
    elif payment.category is PaymentCategory.Transfer:
        if payment.total is None:
            raise CustomValidationError(
                "Total field is required for transfer", ("body", "payment", "total")
            )
    else:
        raise CustomValidationError(
            f"Unknown category {payment.category}", ("body", "payment", "category")
        )

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

    for index, transaction in enumerate(transactions):
        # Modify account balance
        account = session.query(Account).get(transaction.account_id)
        if not account:
            raise CustomValidationError(
                f"Account with id: {transaction.account_id} does not exist",
                ("body", "transactions", index, "account_id"),
            )
        if payment.category is PaymentCategory.Expense:
            account.balance -= transaction.amount
        elif payment.category in (PaymentCategory.Income, PaymentCategory.Transfer):
            account.balance += transaction.amount
        session.add(account)
        # TODO: test what'll happen if two transactions with same account_id are added

        # Store Transactions
        transaction.payment_id = db_payment.id
        transaction.timestamp = payment.timestamp
        transaction.timezone = payment.timezone
        db_transaction = Transaction.from_orm(transaction)
        session.add(db_transaction)
    session.commit()

    new_payment = session.get(Payment, db_payment.id)
    return new_payment


@payment_router.get("", response_model=list[PaymentReadDetailed])
def read_payments(*, session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments


@payment_router.patch("", response_model=PaymentRead)
def update_payment(*, session: Session = Depends(get_session), payment: Payment):
    session.merge(payment)
    session.commit()
    session.refresh(payment)
    return payment


@payment_router.get("/{id}", response_model=PaymentReadDetailed)
def read_payment(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    return payment


@payment_router.delete("/{id}")
def delete_payment(*, session: Session = Depends(get_session), id: int):
    payment = session.query(Payment).get(id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
