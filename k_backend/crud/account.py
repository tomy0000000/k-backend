from collections.abc import Sequence

from sqlmodel import Session, select

from ..schemas.account import Account, AccountBase, AccountCreate, AccountUpdate


def create_account(session: Session, account: AccountCreate) -> AccountBase:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def read_account(session: Session, account_id: int) -> Account | None:
    return session.get(Account, account_id)


def read_accounts(session: Session) -> Sequence[Account]:
    return session.exec(select(Account)).all()


def update_account(
    session: Session, account_id: int, account: AccountUpdate
) -> Account:
    db_account = session.get(Account, account_id)
    if not db_account:
        raise ValueError(f"Account with id {account_id} not found")
    account_data = account.model_dump(exclude_unset=True)
    db_account.sqlmodel_update(account_data)

    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account
