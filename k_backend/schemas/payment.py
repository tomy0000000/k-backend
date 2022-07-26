import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional

import sqlalchemy
from pydantic import root_validator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from ..util import PYDANTIC_JSON_ENCODERS
from ._custom_types import (
    PydanticTimezone,
    SATimezone,
    create_timestamp_validator,
    tz_timestamp_reader,
)

#
# Payment Category
#


class PaymentType(enum.Enum):
    Expense = "Expense"
    Income = "Income"
    Transfer = "Transfer"
    Exchange = "Exchange"


#
# Payment
#


class PaymentBase(SQLModel):
    type: PaymentType = Field(
        sa_column=Column(sqlalchemy.Enum(PaymentType), nullable=False),
        nullable=False,
    )
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        nullable=False,
        title="Local timestamp, or timezone-aware timestamp",
    )
    timezone: PydanticTimezone = Field(
        sa_column=Column(SATimezone(), nullable=False), nullable=False
    )
    description: Optional[str]


class Payment(PaymentBase, table=True):
    __tablename__ = "payment"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    total: Decimal
    transactions: list["Transaction"] = Relationship(back_populates="payment")
    entries: list["PaymentEntry"] = Relationship(back_populates="payment")


class PaymentCreate(PaymentBase):
    total: Optional[Decimal]

    @root_validator
    def verify_timezone(cls, values):
        return create_timestamp_validator(values)


class PaymentRead(PaymentBase):
    id: int
    total: Decimal

    @root_validator
    def convert_timezone(cls, values):
        return tz_timestamp_reader(values)

    class Config:
        json_encoders = PYDANTIC_JSON_ENCODERS


#
# PaymentEntry
#


class PaymentEntryBase(SQLModel):
    payment_id: Optional[int] = Field(foreign_key="payment.id", nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    amount: Decimal
    quantity: int
    description: Optional[str]


class PaymentEntry(PaymentEntryBase, table=True):
    __tablename__ = "payment_entry"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    payment_id: int = Field(foreign_key="payment.id", nullable=False)
    payment: Payment = Relationship(back_populates="entries")
    category: "Category" = Relationship(back_populates="entries")


class PaymentEntryCreate(PaymentEntryBase):
    pass


class PaymentEntryRead(PaymentEntryBase):
    id: int
    payment_id: int


#
# Transaction
#


class TransactionBase(SQLModel):
    account_id: int = Field(primary_key=True, foreign_key="account.id", nullable=False)
    payment_id: Optional[int]
    amount: Decimal
    timestamp: Optional[datetime]
    timezone: Optional[PydanticTimezone]
    description: Optional[str]
    reconcile: bool = Field(nullable=False, default=False)
    psp_id: Optional[int] = Field(foreign_key="payment_service_providers.id")
    psp_reconcile: Optional[bool] = Field(nullable=False, default=False)


class Transaction(TransactionBase, table=True):
    __tablename__ = "transaction"
    payment_id: int = Field(primary_key=True, foreign_key="payment.id", nullable=False)
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False), nullable=False
    )
    timezone: PydanticTimezone = Field(
        sa_column=Column(SATimezone(), nullable=False), nullable=False
    )
    account: "Account" = Relationship(back_populates="transactions")
    payment: Payment = Relationship(back_populates="transactions")
    psp: Optional["PSP"] = Relationship(back_populates="transactions")

    @root_validator
    def verify_timezone(cls, values):
        return create_timestamp_validator(values)


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    payment_id: int
    timestamp: datetime
    timezone: PydanticTimezone

    @root_validator
    def convert_timezone(cls, values):
        return tz_timestamp_reader(values)

    class Config:
        json_encoders = PYDANTIC_JSON_ENCODERS


#
# Relationship Models
#


class PaymentReadDetailed(PaymentRead):
    """Includes transactions and entries."""

    transactions: list[TransactionRead]
    entries: list[PaymentEntryRead]


# FIXME: Find away to prevent this
# flake8: noqa
from .account import Account
from .category import Category
from .psp import PSP
