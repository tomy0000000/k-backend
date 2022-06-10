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


@currency_router.post(
    "",
    response_model=Currency,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "United States Dollar": {
                            "summary": "United States Dollar",
                            "value": {
                                "code": "USD",
                                "name": "United States Dollar",
                                "symbol": "$",
                            },
                        },
                        "Euro": {
                            "summary": "Euro",
                            "value": {"code": "EUR", "name": "Euro", "symbol": "€"},
                        },
                        "British Pound": {
                            "summary": "British Pound",
                            "value": {
                                "code": "GBP",
                                "name": "British Pound",
                                "symbol": "£",
                            },
                        },
                        "New Taiwan Dollar": {
                            "summary": "New Taiwan Dollar",
                            "value": {
                                "code": "TWD",
                                "name": "New Taiwan Dollar",
                                "symbol": "NT$",
                            },
                        },
                    }
                }
            }
        }
    },
)
def create_currency(*, session: Session = Depends(get_session), currency: Currency):
    session.add(currency)
    session.commit()
    session.refresh(currency)
    return currency


@currency_router.get("", response_model=Currency)
def read_currencies(*, session: Session = Depends(get_session)):
    currencys = session.exec(select(Currency)).all()
    return currencys
