from fastapi import APIRouter, Body, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..core.db import get_session
from ..schemas.account import Currency

TAG_NAME = "Currency"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage currencies",
}

currency_router = APIRouter(
    prefix="/currencies",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)

EXAMPLES = {
    "create": {
        "United States Dollar": {
            "summary": "United States Dollar",
            "value": {"code": "USD", "name": "United States Dollar", "symbol": "$"},
        },
        "Euro": {
            "summary": "Euro",
            "value": {"code": "EUR", "name": "Euro", "symbol": "€"},
        },
        "British Pound": {
            "summary": "British Pound",
            "value": {"code": "GBP", "name": "British Pound", "symbol": "£"},
        },
        "New Taiwan Dollar": {
            "summary": "New Taiwan Dollar",
            "value": {"code": "TWD", "name": "New Taiwan Dollar", "symbol": "NT$"},
        },
    }
}


@currency_router.post("", name="Create Currency", response_model=Currency)
def create(
    *,
    session: Session = Depends(get_session),
    currency: Currency = Body(examples=EXAMPLES["create"]),
):
    session.add(currency)
    session.commit()
    session.refresh(currency)
    return currency


@currency_router.get("", name="Read Currencies", response_model=list[Currency])
def reads(*, session: Session = Depends(get_session)):
    currencies = session.exec(select(Currency)).all()
    return currencies
