from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .payment import Transaction


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
    balance: Decimal | None = None


class AccountRead(AccountBase):
    id: int
    balance: Decimal


class Currency(SQLModel, table=True):
    __tablename__ = "currency"
    code: str = Field(primary_key=True)
    name: str
    symbol: str
    accounts: list[Account] = Relationship(back_populates="currency")
