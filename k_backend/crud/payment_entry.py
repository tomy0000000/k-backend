from collections.abc import Sequence

from sqlmodel import Session

from ..schemas.payment import PaymentEntryBase, PaymentEntryCreate


def create_payment_entries(
    session: Session,
    entries: list[PaymentEntryCreate],
    commit: bool = True,
) -> Sequence[PaymentEntryBase]:
    session.add_all(entries)
    if commit:
        session.commit()
        for entry in entries:
            session.refresh(entry)
    else:
        session.flush()
    return entries
