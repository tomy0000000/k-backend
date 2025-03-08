from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic_extra_types.timezone_name import TimeZoneName
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from ._custom_types import SATimezone

if TYPE_CHECKING:
    from .account import Account
    from .payment import Payment
    from .psp import PSP


class TransactionBase(SQLModel):
    account_id: int = Field(primary_key=True, foreign_key="account.id")
    payment_id: int | None = None
    amount: Decimal
    timestamp: datetime = Field(default=datetime.now)
    timezone: TimeZoneName | None = None
    description: str | None = None
    reconcile: bool = False
    psp_id: int | None = Field(foreign_key="payment_service_providers.id", default=None)
    psp_reconcile: bool | None = None


class Transaction(TransactionBase, table=True):
    __tablename__ = "transaction"
    payment_id: int = Field(primary_key=True, foreign_key="payment.id")
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    timezone: TimeZoneName = Field(sa_column=Column(SATimezone(), nullable=False))
    account: "Account" = Relationship(back_populates="transactions")
    payment: "Payment" = Relationship(back_populates="transactions")
    psp: Optional["PSP"] = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    payment_id: int
    timestamp: datetime
    timezone: TimeZoneName
