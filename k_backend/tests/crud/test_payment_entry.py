from sqlmodel import Session

from k_backend.crud.payment_entry import create_payment_entries
from k_backend.schemas.payment import PaymentEntry
from k_backend.tests.factories import PaymentEntryFactory


def test_create_payment_entries(session: Session):
    payment_entries = PaymentEntryFactory.build_batch(3)
    db_entries = create_payment_entries(session, payment_entries)

    assert len(db_entries) == 3

    for i, db_entry in enumerate(db_entries):
        assert db_entry.amount == payment_entries[i].amount
        assert db_entry.category_id == payment_entries[i].category_id
        assert db_entry.description == payment_entries[i].description
        assert db_entry.id is not None
        assert db_entry.payment_id == payment_entries[i].payment_id
        assert db_entry.quantity == payment_entries[i].quantity


def test_create_payment_entries_no_commit(session: Session, session_2: Session):
    entry = PaymentEntryFactory.build()

    # The entry should be created in the session
    session_entry = create_payment_entries(
        session,
        [entry],
        commit=False,
    )[0]
    assert session_entry.id is not None  # Auto int should be set
    assert session_entry.amount == entry.amount
    assert session_entry.category_id == entry.category_id
    assert session_entry.description == entry.description
    assert session_entry.payment_id == entry.payment_id
    assert session_entry.quantity == entry.quantity

    # The entry should not be visible to other sessions (yet)
    session_2_entry = session_2.get(PaymentEntry, session_entry.id)
    assert session_2_entry is None

    # Commit the entry from main session
    session.commit()

    # The entry should now be visible to other sessions
    session_2_entry = session_2.get(PaymentEntry, session_entry.id)
    assert session_2_entry is not None
    assert session_2_entry.id == entry.id
    assert session_2_entry.amount == entry.amount
    assert session_2_entry.category_id == entry.category_id
    assert session_2_entry.description == entry.description
    assert session_2_entry.payment_id == entry.payment_id
    assert session_2_entry.quantity == entry.quantity
