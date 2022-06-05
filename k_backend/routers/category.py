from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_client
from ..db import engine
from ..schemas.category import Category, CategoryCreate, CategoryRead

TAG_NAME = "Category"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage payment entry categories",
}

category_router = APIRouter(
    prefix="/category",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@category_router.post("", response_model=CategoryRead, tags=[TAG_NAME])
def create_category(category: CategoryCreate):
    with Session(engine) as session:
        db_category = Category.from_orm(category)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category


@category_router.get("", response_model=list[CategoryRead], tags=[TAG_NAME])
def read_categories():
    with Session(engine) as session:
        categories = session.exec(select(Category)).all()
        return categories


@category_router.patch("", response_model=CategoryRead, tags=[TAG_NAME])
def update_category(category: Category):
    with Session(engine) as session:
        session.merge(category)
        session.commit()
        session.refresh(category)
        return category


# TODO: Think about how this should work
# @category_router.delete("/{id}", tags=[TAG_NAME])
# def delete_category(id: int):
#     with Session(engine) as session:
#         category = session.query(Category).get(id)
#         if category is None:
#             raise HTTPException(status_code=404, detail="Category not found")
#         session.delete(category)
#         session.commit()
