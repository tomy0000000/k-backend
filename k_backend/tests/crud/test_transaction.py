from sqlmodel import Session

from k_backend.crud.transaction import get_transactions
from k_backend.tests.factories import AccountFactory, TransactionFactory


def test_get_transactions_all(session: Session):
    for _ in range(10):
        TransactionFactory()

    assert len(get_transactions(session)) == 10


def test_get_transactions_by_account(session: Session):
    account_1 = AccountFactory()
    account_2 = AccountFactory()
    TransactionFactory(account=account_1)
    TransactionFactory(account=account_2)

    assert len(get_transactions(session, account_id=account_1.id)) == 1
    assert len(get_transactions(session, account_id=account_2.id)) == 1
