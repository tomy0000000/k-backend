from collections.abc import Sequence
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..auth import get_client
from ..core.db import get_session
from ..schemas.account import Account, AccountBase, AccountCreate, AccountRead

TAG_NAME = "Account"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage accounts",
}

account_router = APIRouter(
    prefix="/accounts",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@account_router.post("", name="Create Account", response_model=AccountRead)
def create(
    *, session: Session = Depends(get_session), account: AccountCreate
) -> AccountBase:
    try:
        account.balance = Decimal()
        db_account = Account.model_validate(account)
        session.add(db_account)
        session.commit()
        session.refresh(db_account)
        return db_account
    except IntegrityError as err:
        raise ValueError(
            f"Currency {db_account.currency_code} is not available"
        ) from err


@account_router.get("", name="Read Accounts", response_model=list[AccountRead])
def reads(*, session: Session = Depends(get_session)) -> Sequence[AccountBase]:
    accounts = session.exec(select(Account)).all()
    return accounts


@account_router.patch("", name="Update Account", response_model=AccountRead)
def update(*, session: Session = Depends(get_session), account: Account) -> AccountBase:
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
