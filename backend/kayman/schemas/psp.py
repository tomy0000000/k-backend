from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from kayman.schemas.transaction import Transaction


class PSPBase(SQLModel):
    name: str


class PSP(PSPBase, table=True):
    __tablename__ = "payment_service_providers"
    id: int | None = Field(primary_key=True, default=None)
    transactions: "Transaction" = Relationship(back_populates="psp")


class PSPCreate(PSPBase):
    pass


class PSPRead(PSPBase):
    id: int
