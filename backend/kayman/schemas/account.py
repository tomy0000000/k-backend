from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from kayman.schemas.currency import Currency
    from kayman.schemas.transaction import Transaction


class AccountBase(SQLModel):
    name: str
    currency_code: str = Field(foreign_key="currency.code")


class Account(AccountBase, table=True):
    __tablename__ = "account"
    id: int | None = Field(primary_key=True, default=None)
    balance: Decimal
    currency: "Currency" = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int
    balance: Decimal


class AccountUpdate(SQLModel):
    name: str | None = None
