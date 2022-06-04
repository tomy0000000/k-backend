from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from ._custom_types import PydanticTimezone, SATimezone


class Payment(SQLModel, table=True):
    __tablename__ = "payment"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    total: float
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=False
    )
    timezone: PydanticTimezone = Field(sa_column=Column(SATimezone()), nullable=False)
    description: str
    transactions: List["Transaction"] = Relationship(back_populates="payment")


class PaymentEntryBase(SQLModel):
    payment_id: Optional[int] = Field(foreign_key="payment.id", nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    amount: float
    quantity: int
    description: str
    payment: Payment = Relationship(back_populates="entries")
    category: "Category" = Relationship(back_populates="entries")


class PaymentEntry(PaymentEntryBase, table=True):
    __tablename__ = "payment_entry"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    payment_id: int = Field(foreign_key="payment.id", nullable=False)


class PaymentEntryCreate(PaymentEntryBase):
    pass


class PaymentEntryRead(PaymentEntryBase):
    id: int
    payment_id: int


class Transaction(SQLModel, table=True):

    __tablename__ = "transaction"
    account_id: int = Field(primary_key=True, foreign_key="account.id", nullable=False)
    payment_id: int = Field(primary_key=True, foreign_key="payment.id", nullable=False)
    amount: float
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), nullable=False
    )
    timezone: PydanticTimezone = Field(sa_column=Column(SATimezone()), nullable=False)
    account: "Account" = Relationship(back_populates="transactions")
    payment: Payment = Relationship(back_populates="transactions")


from .account import Account
from .category import Category
