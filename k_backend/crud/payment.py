from datetime import date

from sqlalchemy import func
from sqlmodel import Session, select

from ..schemas.payment import Payment


def get_payments(session: Session, payment_date: date | None) -> list[Payment]:
    scalar = select(Payment)
    if payment_date:
        scalar = scalar.where(func.date(Payment.timestamp) == payment_date)
    payments = session.exec(scalar).all()
    return payments
