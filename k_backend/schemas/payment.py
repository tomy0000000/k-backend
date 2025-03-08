import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy
from pydantic_extra_types.timezone_name import TimeZoneName
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from ._custom_types import SATimezone

if TYPE_CHECKING:
    from .category import Category
    from .transaction import Transaction

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
        sa_column=Column(sqlalchemy.Enum(PaymentType), nullable=False)
    )
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        title="Local timestamp, or timezone-aware timestamp",
    )
    timezone: TimeZoneName = Field(sa_column=Column(SATimezone(), nullable=False))
    description: str | None = None


class Payment(PaymentBase, table=True):
    __tablename__ = "payment"
    id: int | None = Field(primary_key=True, default=None)
    # Auto calculated for Expense or Income
    # Manually logged for Transfer or Exchange
    total: Decimal
    transactions: list["Transaction"] = Relationship(back_populates="payment")
    entries: list["PaymentEntry"] = Relationship(back_populates="payment")


class PaymentCreate(PaymentBase):
    total: Decimal | None = None


class PaymentRead(PaymentBase):
    id: int
    total: Decimal


#
# PaymentEntry
#


class PaymentEntryBase(SQLModel):
    payment_id: int | None = Field(foreign_key="payment.id", default=None)
    category_id: int = Field(foreign_key="category.id")
    amount: Decimal
    quantity: int
    description: str | None = None


class PaymentEntry(PaymentEntryBase, table=True):
    __tablename__ = "payment_entry"
    id: int | None = Field(primary_key=True, default=None)
    payment_id: int = Field(foreign_key="payment.id")
    payment: Payment = Relationship(back_populates="entries")
    category: "Category" = Relationship(back_populates="entries")


class PaymentEntryCreate(PaymentEntryBase):
    pass


class PaymentEntryRead(PaymentEntryBase):
    id: int
    payment_id: int
