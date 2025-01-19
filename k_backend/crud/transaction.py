from sqlmodel import Session, select

from ..schemas.payment import Transaction


def get_transactions(
    session: Session, account_id: int | None = None
) -> list[Transaction]:
    scalar = select(Transaction)
    if account_id:
        scalar = scalar.where(Transaction.account_id == account_id)
    txns = session.exec(scalar).all()
    return txns
