from sqlmodel import Session

from k_backend.crud.transaction import create_transaction, get_transactions
from k_backend.tests.factories import AccountFactory, TransactionFactory


def test_create_transaction(session: Session):
    txn = TransactionFactory.build()
    db_txn = create_transaction(session, txn)

    assert db_txn.account_id == txn.account_id
    assert db_txn.amount == txn.amount
    assert db_txn.description == txn.description
    assert db_txn.payment_id == txn.payment_id
    assert db_txn.psp_id == txn.psp_id
    assert db_txn.psp_reconcile == txn.psp_reconcile
    assert db_txn.reconcile == txn.reconcile
    assert db_txn.timestamp == txn.timestamp
    assert db_txn.timezone == txn.timezone


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
