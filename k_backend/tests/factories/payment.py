import factory
from factory.alchemy import SQLAlchemyModelFactory

from k_backend.schemas import Payment
from k_backend.schemas.api_models import PaymentCreateDetailed
from k_backend.schemas.payment import PaymentType


class PaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Payment
        sqlalchemy_session_persistence = "commit"

    description = factory.Faker("sentence")
    timestamp = factory.Faker("date_time")
    timezone = "UTC"
    total = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    type = factory.Faker("random_element", elements=list(PaymentType))

    @classmethod
    def build_details(cls, type=PaymentType.Expense, entry_num=1, transaction_num=1):
        from .payment_entry import PaymentEntryFactory
        from .transaction import TransactionFactory

        # Create entries and transactions
        entries = PaymentEntryFactory.build_batch(entry_num)
        transactions = TransactionFactory.build_batch(transaction_num)

        # Calculate totals
        total = factory.Faker("pydecimal", left_digits=5, right_digits=2)
        entries_total = sum([entry.amount * entry.quantity for entry in entries])
        transactions_total = sum([transaction.amount for transaction in transactions])

        if type is PaymentType.Expense:
            # Update last transaction amount to match the total
            # entries_total == -transactions_total
            transactions[-1].amount -= entries_total + transactions_total
            total = entries_total

        if type is PaymentType.Income:
            # Update last transaction amount to match the total
            # entries_total == transactions_total
            transactions[-1].amount -= transactions_total - entries_total
            total = entries_total

        # Create payment
        payment = cls.build(
            type=type,
            total=total,
            entries=entries,
            transactions=transactions,
        )

        return PaymentCreateDetailed(
            payment=payment, entries=entries, transactions=transactions
        )
