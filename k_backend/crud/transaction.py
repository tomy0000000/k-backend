from collections.abc import Sequence

from sqlmodel import Session, select

from ..schemas.transaction import Transaction, TransactionBase, TransactionCreate


def create_transaction(session: Session, txn: TransactionCreate) -> TransactionBase:
    session.add(txn)
    session.commit()
    session.refresh(txn)
    return txn


def get_transactions(
    session: Session, account_id: int | None = None
) -> Sequence[Transaction]:
    scalar = select(Transaction)
    if account_id:
        scalar = scalar.where(Transaction.account_id == account_id)
    txns = session.exec(scalar).all()
    return txns
