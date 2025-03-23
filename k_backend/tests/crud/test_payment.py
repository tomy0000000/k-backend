from datetime import datetime

from sqlmodel import Session

from k_backend.crud.payment import create_payment, read_payment, read_payments
from k_backend.tests.factories import (
    CategoryFactory,
    PaymentEntryFactory,
    PaymentFactory,
)


def test_create_payment(session: Session, session_2: Session):
    payment = PaymentFactory.build()
    create_payment(session, payment)
    db_payment = read_payment(session_2, payment.id)

    assert db_payment.id is not None
    assert db_payment.description == payment.description
    assert db_payment.timestamp == payment.timestamp
    assert db_payment.timezone == payment.timezone
    assert db_payment.total == payment.total
    assert db_payment.type == payment.type


def test_create_payment_no_commit(session: Session, session_2: Session):
    payment = PaymentFactory.build()

    # The payment should be created in the session
    session_payment = create_payment(session, payment, commit=False)
    assert session_payment.id is not None  # Auto int should be set
    assert session_payment.description == payment.description
    assert session_payment.timestamp == payment.timestamp
    assert session_payment.timezone == payment.timezone
    assert session_payment.total == payment.total
    assert session_payment.type == payment.type

    # The payment should not be visible to other sessions (yet)
    session_2_payment = read_payment(session_2, payment.id)
    assert session_2_payment is None

    # Commit the payment from main session
    session.commit()

    # The payment should now be visible to other sessions
    session_2_payment = read_payment(session_2, payment.id)
    assert session_2_payment is not None
    assert session_2_payment.id == payment.id
    assert session_2_payment.description == payment.description
    assert session_2_payment.timestamp == payment.timestamp
    assert session_2_payment.timezone == payment.timezone
    assert session_2_payment.total == payment.total
    assert session_2_payment.type == payment.type


def test_read_payment(session: Session):
    payment = PaymentFactory()
    assert read_payment(session, payment.id) == payment


def test_read_payments_all(session: Session):
    for _ in range(10):
        PaymentFactory()

    assert len(read_payments(session)) == 10


def test_read_payments_by_date(session: Session):
    PaymentFactory(timestamp=datetime(2025, 1, 1))
    PaymentFactory(timestamp=datetime(2025, 1, 2))

    assert len(read_payments(session, payment_date="2025-01-01")) == 1
    assert len(read_payments(session, payment_date="2025-01-02")) == 1


def test_read_payments_by_category(session: Session):
    category_1 = CategoryFactory()
    category_2 = CategoryFactory()
    category_3 = CategoryFactory()
    payment_1 = PaymentFactory(
        entries=[
            PaymentEntryFactory(category=category_1),
            PaymentEntryFactory(category=category_2),
        ]
    )
    payment_2 = PaymentFactory(
        entries=[
            PaymentEntryFactory(category=category_1),
            PaymentEntryFactory(category=category_3),
        ]
    )

    payments = read_payments(session, category_id=category_1.id)
    payment_ids = {payment.id for payment in payments}
    assert len(payments) == 2
    assert payment_1.id in payment_ids
    assert payment_2.id in payment_ids

    payments = read_payments(session, category_id=category_2.id)
    assert len(payments) == 1
    assert payments[0].id == payment_1.id

    payments = read_payments(session, category_id=category_3.id)
    assert len(payments) == 1
    assert payments[0].id == payment_2.id
