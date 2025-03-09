from collections.abc import Sequence
from datetime import date

from sqlalchemy import func
from sqlmodel import Session, select

from ..schemas.payment import Payment, PaymentEntry


def read_payments(
    session: Session, payment_date: date | None = None, category_id: int | None = None
) -> Sequence[Payment]:
    scalar = select(Payment).distinct()
    if payment_date:
        scalar = scalar.where(func.date(Payment.timestamp) == payment_date)
    if category_id:
        scalar = scalar.join(PaymentEntry).where(
            PaymentEntry.category_id == category_id
        )
    payments = session.exec(scalar).all()
    return payments
