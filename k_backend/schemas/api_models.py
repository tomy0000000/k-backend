"""Composite Models for direct use in the API."""

from sqlmodel import SQLModel

from k_backend.schemas.payment import (
    PaymentCreate,
    PaymentEntryCreate,
    PaymentEntryRead,
    PaymentRead,
)
from k_backend.schemas.transaction import TransactionCreate, TransactionRead


class PaymentReadDetailed(PaymentRead):
    """Includes transactions and entries."""

    transactions: list[TransactionRead]
    entries: list[PaymentEntryRead]


class PaymentCreateDetailed(SQLModel):
    """Includes transactions and entries."""

    payment: PaymentCreate
    transactions: list[TransactionCreate]
    entries: list[PaymentEntryCreate]
