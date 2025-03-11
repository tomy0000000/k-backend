from decimal import Decimal
from unittest.mock import patch

import pytest
from sqlmodel import Session

from k_backend.crud.account import (
    create_account,
    read_account,
    read_accounts,
    update_account,
)
from k_backend.tests.factories import AccountFactory


def test_create_account(session: Session):
    account = AccountFactory.build(balance=0)
    db_account = create_account(session, account)

    assert db_account.id is not None
    assert db_account.name == account.name
    assert db_account.currency_code == account.currency_code
    assert db_account.balance == 0


def test_read_account(session: Session):
    account = AccountFactory()
    db_account = read_account(session, account.id)

    assert db_account.id == account.id
    assert db_account.name == account.name
    assert db_account.currency_code == account.currency_code
    assert db_account.balance == account.balance


def test_read_account_not_found(session: Session):
    assert read_account(session, 1) is None


def test_read_accounts(session: Session):
    accounts = AccountFactory.create_batch(10)
    db_accounts = read_accounts(session)

    assert len(db_accounts) == 10
    for account, db_account in zip(accounts, db_accounts, strict=True):
        assert db_account.balance == account.balance
        assert db_account.currency_code == account.currency_code
        assert db_account.id == account.id
        assert db_account.name == account.name


def test_read_accounts_by_ids(session: Session):
    accounts = AccountFactory.create_batch(10)
    interest_accounts = [accounts[index] for index in range(0, 10, 2)]
    db_accounts = read_accounts(session, [account.id for account in interest_accounts])

    assert len(db_accounts) == 5
    for account, db_account in zip(interest_accounts, db_accounts, strict=True):
        assert db_account.balance == account.balance
        assert db_account.currency_code == account.currency_code
        assert db_account.id == account.id
        assert db_account.name == account.name


def test_read_accounts_for_update(session: Session):
    AccountFactory()

    with patch.object(session, "exec", wraps=session.exec) as mock_exec:
        read_accounts(session, for_update=True)
        args = mock_exec.call_args[0]
        statement = str(args[0])
        assert "FOR UPDATE" in statement


def test_update_account(session: Session):
    account = AccountFactory()

    db_account = read_account(session, account.id)
    assert db_account.id == account.id
    assert db_account.name == account.name
    assert db_account.currency_code == account.currency_code
    assert db_account.balance == account.balance

    account.name = "New Name"
    account.balance = Decimal("100")
    new_db_account = update_account(session, account.id, account)

    assert new_db_account.id == db_account.id
    assert new_db_account.name == account.name  # Updated
    assert new_db_account.currency_code == db_account.currency_code
    assert new_db_account.balance == db_account.balance  # Not updated


def test_update_account_not_found(session: Session):
    account = AccountFactory.build()

    with pytest.raises(ValueError, match="Account with id 1 not found"):
        update_account(session, 1, account)
