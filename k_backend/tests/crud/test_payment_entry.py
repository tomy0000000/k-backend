from sqlmodel import Session

from k_backend.crud.payment_entry import create_payment_entries
from k_backend.tests.factories import PaymentEntryFactory, PaymentFactory


def test_create_payment_entries(session: Session):
    payment = PaymentFactory()
    payment_entries = PaymentEntryFactory.build_batch(3, payment=payment)
    db_entries = create_payment_entries(session, payment_entries, payment.id)

    assert len(db_entries) == 3

    for i, db_entry in enumerate(db_entries):
        assert db_entry.amount == payment_entries[i].amount
        assert db_entry.category_id == payment_entries[i].category_id
        assert db_entry.description == payment_entries[i].description
        assert db_entry.id is not None
        assert db_entry.payment_id == payment.id
        assert db_entry.quantity == payment_entries[i].quantity
