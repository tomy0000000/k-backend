from datetime import datetime
from typing import Optional

from pydantic import root_validator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from ._custom_types import (
    EXTENDED_JSON_ENCODERS,
    PydanticTimezone,
    SATimezone,
    create_timestamp_validator,
    tz_timestamp_reader,
)

#
# Payment
#


class PaymentBase(SQLModel):
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        nullable=False,
        title="Local timestamp, or timezone-aware timestamp",
    )
    timezone: PydanticTimezone = Field(
        sa_column=Column(SATimezone(), nullable=False), nullable=False
    )
    description: str


class Payment(PaymentBase, table=True):
    __tablename__ = "payment"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    total: float
    transactions: list["Transaction"] = Relationship(back_populates="payment")
    entries: list["PaymentEntry"] = Relationship(back_populates="payment")


class PaymentCreate(PaymentBase):
    total: Optional[float]

    @root_validator
    def verify_timezone(cls, values):
        return create_timestamp_validator(values)


class PaymentRead(PaymentBase):
    id: int
    total: float

    @root_validator
    def convert_timezone(cls, values):
        return tz_timestamp_reader(values)

    class Config:
        json_encoders = EXTENDED_JSON_ENCODERS


#
# PaymentEntry
#


class PaymentEntryBase(SQLModel):
    payment_id: Optional[int] = Field(foreign_key="payment.id", nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    amount: float
    quantity: int
    description: str


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


class Transaction(SQLModel, table=True):

    __tablename__ = "transaction"
    account_id: int = Field(primary_key=True, foreign_key="account.id", nullable=False)
    payment_id: int = Field(primary_key=True, foreign_key="payment.id", nullable=False)
    amount: float
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False), nullable=False
    )
    timezone: PydanticTimezone = Field(
        sa_column=Column(SATimezone(), nullable=False), nullable=False
    )
    account: "Account" = Relationship(back_populates="transactions")
    payment: Payment = Relationship(back_populates="transactions")


#
# Relationship Models
#


class PaymentReadWithEntries(PaymentRead):
    entries: list[PaymentEntryRead] = []


from .account import Account
from .category import Category
