from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class PSPBase(SQLModel):
    name: str


class PSP(PSPBase, table=True):
    __tablename__ = "payment_service_providers"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    transactions: "Transaction" = Relationship(back_populates="psp")


class PSPCreate(PSPBase):
    pass


class PSPRead(PSPBase):
    id: int


# FIXME: Find away to prevent this
# flake8: noqa
from .payment import Transaction
