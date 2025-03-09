from sqlmodel import Session

from ..schemas.payment import PaymentEntry, PaymentEntryCreate


def create_payment_entries(
    session: Session, entries: list[PaymentEntryCreate], payment_id: int
) -> list[PaymentEntry]:
    db_entries = []
    for entry in entries:
        entry.payment_id = payment_id  # Add payment_id to the entry
        db_entries.append(PaymentEntry.model_validate(entry))
    session.add_all(db_entries)
    session.commit()
    return db_entries
