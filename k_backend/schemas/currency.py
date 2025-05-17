from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .account import Account


class Currency(SQLModel, table=True):
    __tablename__ = "currency"
    code: str = Field(primary_key=True)
    name: str
    symbol: str
    accounts: list["Account"] = Relationship(back_populates="currency")
