from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlmodel import Session

from k_backend.auth import get_client
from k_backend.core.db import get_session
from k_backend.crud.transaction import get_transactions
from k_backend.schemas.transaction import TransactionBase, TransactionRead

TAG_NAME = "Transaction"
tag = {
    "name": TAG_NAME,
    "description": "Query and manage transactions",
}

txn_router = APIRouter(
    prefix="/transactions",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@txn_router.get("", name="Read Transactions", response_model=list[TransactionRead])
def reads(
    *, session: Session = Depends(get_session), account_id: int | None = None
) -> Sequence[TransactionBase]:
    return get_transactions(session, account_id)
