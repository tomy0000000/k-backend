import factory
from factory.alchemy import SQLAlchemyModelFactory

from k_backend.schemas import (
    Account,
    Category,
    Currency,
    Payment,
    PaymentEntry,
    Transaction,
)


class CurrencyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Currency
        sqlalchemy_session_persistence = "commit"

    code = factory.Sequence(lambda n: f"CUR{n:03d}")
    name = factory.Faker("currency_name")
    symbol = factory.Faker("currency_symbol")


class AccountFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Account
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    currency = factory.SubFactory(CurrencyFactory)
    balance = factory.Faker("pydecimal", left_digits=5, right_digits=2)


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    description = factory.Faker("sentence")


class PaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Payment
        sqlalchemy_session_persistence = "commit"

    type = "Expense"
    timestamp = factory.Faker("date_time")
    timezone = "UTC"
    description = factory.Faker("sentence")
    total = factory.Faker("pydecimal", left_digits=5, right_digits=2)


# Expense of one transaction + one entry
class PaymentSimpleExpenseFactory(PaymentFactory):
    transactions = factory.RelatedFactoryList(
        "k_backend.tests.factories.TransactionFactory", "payment", size=1
    )
    entries = factory.RelatedFactoryList(
        "k_backend.tests.factories.PaymentEntryFactory", "payment", size=1
    )


class PaymentEntryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PaymentEntry
        sqlalchemy_session_persistence = "commit"

    payment = factory.SubFactory(PaymentFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    quantity = factory.Faker("random_int", min=1, max=10)
    description = factory.Faker("sentence")


class TransactionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Transaction
        sqlalchemy_session_persistence = "commit"

    account = factory.SubFactory(AccountFactory)
    payment = factory.SubFactory(PaymentFactory)
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    timestamp = factory.Faker("date_time")
    timezone = "UTC"
    description = factory.Faker("sentence")
    reconcile = factory.Faker("boolean")
