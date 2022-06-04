from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..db import engine
from ..schemas.account import Currency

TAG_NAME = "Currency"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage currencies",
}

currency_router = APIRouter(
    prefix="/currency",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@currency_router.post("", response_model=Currency, tags=[TAG_NAME])
def create_currency(currency: Currency):
    with Session(engine) as session:
        session.add(currency)
        session.commit()
        session.refresh(currency)
        return currency


@currency_router.get("", response_model=Currency, tags=[TAG_NAME])
def read_currencies():
    with Session(engine) as session:
        currencys = session.exec(select(Currency)).all()
        return currencys
