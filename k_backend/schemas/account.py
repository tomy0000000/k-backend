from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class AccountBase(SQLModel):
    name: str
    currency_code: str = Field(foreign_key="currency.code", nullable=False)


class Account(AccountBase, table=True):
    __tablename__ = "account"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    currency: "Currency" = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int


class Currency(SQLModel, table=True):
    __tablename__ = "currency"
    code: str = Field(primary_key=True, nullable=False)
    name: str
    symbol: str
    accounts: List[Account] = Relationship(back_populates="currency")


from .payment import Transaction
