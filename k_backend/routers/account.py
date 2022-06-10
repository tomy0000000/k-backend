from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.account import Account, AccountCreate, AccountRead

TAG_NAME = "Account"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage accounts",
}

account_router = APIRouter(
    prefix="/account",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@account_router.post("", response_model=AccountRead)
def create_account(*, session: Session = Depends(get_session), account: AccountCreate):
    try:
        account.balance = 0
        db_account = Account.from_orm(account)
        session.add(db_account)
        session.commit()
        session.refresh(db_account)
        return db_account
    except IntegrityError:
        raise ValueError(f"Currency {db_account.currency_code} is not available")


@account_router.get("", response_model=list[AccountRead])
def read_accounts(*, session: Session = Depends(get_session)):
    accounts = session.exec(select(Account)).all()
    return accounts


@account_router.patch("", response_model=AccountRead)
def update_account(*, session: Session = Depends(get_session), account: Account):
    session.merge(account)
    session.commit()
    session.refresh(account)
    return account


# TODO: Think about how this should work
# @account_router.delete("/{id}")
# def delete_account(*, session: Session = Depends(get_session), id: int):
#     account = session.query(Account).get(id)
#     if account is None:
#         raise HTTPException(status_code=404, detail="Account not found")
#     session.delete(account)
#     session.commit()
