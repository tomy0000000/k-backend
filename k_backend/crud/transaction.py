from collections.abc import Sequence

from sqlmodel import Session, select

from ..schemas.transaction import Transaction, TransactionBase, TransactionCreate


def create_transactions(
    session: Session,
    txns: Sequence[TransactionCreate],
    commit: bool = True,
) -> Sequence[TransactionBase]:
    session.add_all(txns)
    if commit:
        session.commit()
        for txn in txns:
            session.refresh(txn)
    else:
        session.flush()
    return txns


def get_transactions(
    session: Session, account_id: int | None = None
) -> Sequence[Transaction]:
    scalar = select(Transaction)
    if account_id:
        scalar = scalar.where(Transaction.account_id == account_id)
    txns = session.exec(scalar).all()
    return txns
