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
    account_id: int = Field(foreign_key="account.id")
    # Logically, `payment_id` should have been a required field. However, it will be
    # automatically populated when the payment is created, so it should not be
    # explicitly assigened.
    payment_id: int | None = Field(foreign_key="payment.id", default=None)
    amount: Decimal
    timestamp: datetime = Field(default=datetime.now)
    timezone: TimeZoneName | None = None
    description: str | None = None
    reconcile: bool = False
    psp_id: int | None = Field(foreign_key="payment_service_providers.id", default=None)
    psp_reconcile: bool | None = None


class Transaction(TransactionBase, table=True):
    __tablename__ = "transaction"
    id: int | None = Field(primary_key=True, default=None)
    payment_id: int = Field(foreign_key="payment.id")
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
    id: int
    payment_id: int
    timestamp: datetime
    timezone: TimeZoneName
