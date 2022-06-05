from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
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
def create_currency(*, session: Session = Depends(get_session), currency: Currency):
    session.add(currency)
    session.commit()
    session.refresh(currency)
    return currency


@currency_router.get("", response_model=Currency, tags=[TAG_NAME])
def read_currencies(*, session: Session = Depends(get_session)):
    currencys = session.exec(select(Currency)).all()
    return currencys
