from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .payment import PaymentEntry


class CategoryBase(SQLModel):
    name: str
    description: str | None = None
    disabled: bool = Field(default=False)
    parent_id: int | None = Field(foreign_key="category.id", default=None)


class Category(CategoryBase, table=True):
    __tablename__ = "category"
    id: int | None = Field(primary_key=True, default=None)
    entries: list["PaymentEntry"] = Relationship(back_populates="category")
    parent_category: Optional["Category"] = Relationship(
        back_populates="sub_categories",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    sub_categories: list["Category"] = Relationship(back_populates="parent_category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryReadWithChildren(CategoryRead):
    sub_categories: list[CategoryRead] | None = None
