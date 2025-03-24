from sqlmodel import Session

from k_backend.crud.transaction import create_transactions, get_transactions
from k_backend.schemas.transaction import Transaction
from k_backend.tests.factories import AccountFactory, TransactionFactory


def test_create_transactions_1_txn(session: Session):
    txn = TransactionFactory.build()
    db_txn = create_transactions(session, [txn])[0]

    assert db_txn.account_id == txn.account_id
    assert db_txn.amount == txn.amount
    assert db_txn.description == txn.description
    assert db_txn.payment_id == txn.payment_id
    assert db_txn.psp_id == txn.psp_id
    assert db_txn.psp_reconcile == txn.psp_reconcile
    assert db_txn.reconcile == txn.reconcile
    assert db_txn.timestamp == txn.timestamp
    assert db_txn.timezone == txn.timezone


def test_create_transactions_n_txn(session: Session):
    txns = TransactionFactory.build_batch(10)
    db_txns = create_transactions(session, txns)

    assert len(db_txns) == 10
    for db_txn, txn in zip(db_txns, txns, strict=False):
        assert db_txn.account_id == txn.account_id
        assert db_txn.amount == txn.amount
        assert db_txn.description == txn.description
        assert db_txn.payment_id == txn.payment_id
        assert db_txn.psp_id == txn.psp_id
        assert db_txn.psp_reconcile == txn.psp_reconcile
        assert db_txn.reconcile == txn.reconcile
        assert db_txn.timestamp == txn.timestamp
        assert db_txn.timezone == txn.timezone


def test_create_transactions_no_commit(session: Session, session_2: Session):
    txn = TransactionFactory.build()

    # The txn should be created in the session
    session_txn = create_transactions(session, [txn], commit=False)[0]
    assert session_txn.account_id == txn.account_id
    assert session_txn.amount == txn.amount
    assert session_txn.description == txn.description
    assert session_txn.payment_id == txn.payment_id
    assert session_txn.psp_id == txn.psp_id
    assert session_txn.psp_reconcile == txn.psp_reconcile
    assert session_txn.reconcile == txn.reconcile
    assert session_txn.timestamp == txn.timestamp
    assert session_txn.timezone == txn.timezone

    # The txn should not be visible to other sessions (yet)
    session_2_txn = session_2.get(Transaction, (txn.account_id, txn.payment_id))
    assert session_2_txn is None

    # Commit the txn from main session
    session.commit()

    # The txn should now be visible to other sessions
    session_2_txn = session_2.get(Transaction, (txn.account_id, txn.payment_id))
    assert session_2_txn is not None
    assert session_2_txn.account_id == txn.account_id
    assert session_2_txn.amount == txn.amount
    assert session_2_txn.description == txn.description
    assert session_2_txn.payment_id == txn.payment_id
    assert session_2_txn.psp_id == txn.psp_id
    assert session_2_txn.psp_reconcile == txn.psp_reconcile
    assert session_2_txn.reconcile == txn.reconcile
    assert session_2_txn.timestamp == txn.timestamp
    assert session_2_txn.timezone == txn.timezone


def test_get_transactions_all(session: Session):
    TransactionFactory.create_batch(10)

    assert len(get_transactions(session)) == 10


def test_get_transactions_by_account(session: Session):
    account_1 = AccountFactory()
    account_2 = AccountFactory()
    TransactionFactory(account=account_1)
    TransactionFactory(account=account_2)

    assert len(get_transactions(session, account_id=account_1.id)) == 1
    assert len(get_transactions(session, account_id=account_2.id)) == 1
