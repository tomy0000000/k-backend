from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CategoryBase(SQLModel):
    name: str
    description: Optional[str]
    disabled: bool = Field(nullable=False, default=False)
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Category(CategoryBase, table=True):
    __tablename__ = "category"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    entries: list["PaymentEntry"] = Relationship(back_populates="category")
    parent_category: Optional["Category"] = Relationship(
        back_populates="sub_categories",
        sa_relationship_kwargs=dict(remote_side="Category.id"),
    )
    sub_categories: list["Category"] = Relationship(back_populates="parent_category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryReadWithChildren(CategoryRead):
    sub_categories: Optional[list[CategoryRead]]


# FIXME: Find away to prevent this
# flake8: noqa
from .payment import PaymentEntry
