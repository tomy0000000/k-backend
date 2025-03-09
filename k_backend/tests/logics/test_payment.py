import pytest

from k_backend.logics.payment import validate_total
from k_backend.schemas.payment import PaymentType
from k_backend.tests.factories import PaymentFactory


def test_validate_total_expense_no_total():
    """Total is not set and entries total is used"""
    details = PaymentFactory.build_details(
        type=PaymentType.Expense, entry_num=3, transaction_num=5
    )
    details.payment.total = None
    validate_total(details)


def test_validate_total_expense_explicit_total():
    """Total is explicitly set and matches the entries total"""
    details = PaymentFactory.build_details(
        type=PaymentType.Expense, entry_num=3, transaction_num=5
    )
    validate_total(details)


def test_validate_total_expense_explicit_total_mismatch():
    """Contains a total that does not match the sum of entries"""
    details = PaymentFactory.build_details(
        type=PaymentType.Expense, entry_num=3, transaction_num=5
    )
    details.payment.total += 1
    with pytest.raises(ValueError, match="payment (.*) not match"):
        validate_total(details)


def test_validate_total_expense_entries_transactions_mismatch():
    """Entries and transactions totals do not match"""
    details = PaymentFactory.build_details(
        type=PaymentType.Expense, entry_num=3, transaction_num=5
    )
    details.transactions[-1].amount += 1
    with pytest.raises(ValueError, match="transactions (.*) not match"):
        validate_total(details)


def test_validate_total_transfer_with_total():
    """Total is not set and entries total is used"""
    details = PaymentFactory.build_details(
        type=PaymentType.Transfer, entry_num=3, transaction_num=5
    )
    validate_total(details)


def test_validate_total_transfer_without_total():
    """Total is explicitly set and matches the entries total"""
    details = PaymentFactory.build_details(
        type=PaymentType.Transfer, entry_num=3, transaction_num=5
    )
    details.payment.total = None
    with pytest.raises(ValueError, match="must have a total"):
        validate_total(details)
