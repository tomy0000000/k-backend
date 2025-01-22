from datetime import datetime

from sqlmodel import Session

from k_backend.crud.payment import get_payments
from k_backend.tests.factories import (
    CategoryFactory,
    PaymentEntryFactory,
    PaymentFactory,
)


def test_get_all_payments(session: Session):
    for _ in range(10):
        PaymentFactory()

    assert len(get_payments(session)) == 10


def test_get_payment_by_date(session: Session):
    PaymentFactory(timestamp=datetime(2025, 1, 1))
    PaymentFactory(timestamp=datetime(2025, 1, 2))

    assert len(get_payments(session, payment_date="2025-01-01")) == 1
    assert len(get_payments(session, payment_date="2025-01-02")) == 1


def test_get_payment_by_category(session: Session):
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

    payments = get_payments(session, category_id=category_1.id)
    payment_ids = {payment.id for payment in payments}
    assert len(payments) == 2
    assert payment_1.id in payment_ids
    assert payment_2.id in payment_ids

    payments = get_payments(session, category_id=category_2.id)
    assert len(payments) == 1
    assert payments[0].id == payment_1.id

    payments = get_payments(session, category_id=category_3.id)
    assert len(payments) == 1
    assert payments[0].id == payment_2.id
