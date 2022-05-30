from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    name: str
    currency_code: str = Field(foreign_key="currency.code", nullable=False)
    currency: str = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class Currency(SQLModel, table=True):
    __tablename__ = "currency"
    code: str = Field(primary_key=True, nullable=False)
    name: str
    symbol: str
    accounts: List[Account] = Relationship(back_populates="currency")


from .payment import Transaction
