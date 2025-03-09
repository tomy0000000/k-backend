from decimal import Decimal

from ..schemas.api_models import PaymentCreateDetailed
from ..schemas.payment import PaymentType


def validate_total(details: PaymentCreateDetailed) -> None:
    if details.payment.type in (PaymentType.Expense, PaymentType.Income):
        entries_total = Decimal(
            sum([entry.amount * entry.quantity for entry in details.entries])
        )
        transactions_total = Decimal(
            sum([transaction.amount for transaction in details.transactions])
        )
        if entries_total != -transactions_total:
            raise ValueError(
                f"Entries total ({entries_total}) and "
                f"transactions total ({-transactions_total}) do not match"
            )
        if details.payment.total is None:
            details.payment.total = entries_total
        elif entries_total != details.payment.total:
            raise ValueError(
                f"Entries total ({entries_total}) and "
                f"payment total ({details.payment.total}) do not match"
            )

    if details.payment.type in (PaymentType.Transfer, PaymentType.Exchange):
        if details.payment.total is None:
            raise ValueError("Transfer or Exchange payment must have a total")
