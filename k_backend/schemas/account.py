from decimal import Decimal
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from ..util import PYDANTIC_JSON_ENCODERS


class AccountBase(SQLModel):
    name: str
    currency_code: str = Field(foreign_key="currency.code", nullable=False)


class Account(AccountBase, table=True):
    __tablename__ = "account"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    balance: Decimal
    currency: "Currency" = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    balance: Optional[Decimal]


class AccountRead(AccountBase):
    id: int
    balance: Decimal

    class Config:
        json_encoders = PYDANTIC_JSON_ENCODERS


class Currency(SQLModel, table=True):
    __tablename__ = "currency"
    code: str = Field(primary_key=True, nullable=False)
    name: str
    symbol: str
    accounts: list[Account] = Relationship(back_populates="currency")


# FIXME: Find away to prevent this
# flake8: noqa
from .payment import Transaction
