import factory
from factory.alchemy import SQLAlchemyModelFactory

from k_backend.schemas import PaymentEntry


class PaymentEntryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PaymentEntry
        sqlalchemy_session_persistence = "commit"

    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    category = factory.SubFactory("k_backend.tests.factories.category.CategoryFactory")
    category_id = factory.SelfAttribute("category.id")
    description = factory.Faker("sentence")
    index = factory.Sequence(lambda n: n)
    payment = factory.SubFactory("k_backend.tests.factories.payment.PaymentFactory")
    payment_id = factory.SelfAttribute("payment.id")
    quantity = factory.Faker("random_int", min=1, max=10)
    currency = factory.SubFactory("k_backend.tests.factories.currency.CurrencyFactory")
    currency_code = factory.SelfAttribute("currency.code")
