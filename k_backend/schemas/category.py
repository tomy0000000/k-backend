from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CategoryBase(SQLModel):
    name: str
    description: Optional[str]


class Category(CategoryBase, table=True):
    __tablename__ = "category"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    entries: list["PaymentEntry"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


from .payment import PaymentEntry
