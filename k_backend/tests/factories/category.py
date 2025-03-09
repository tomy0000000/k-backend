import factory
from factory.alchemy import SQLAlchemyModelFactory

from k_backend.schemas import Category


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name")
    description = factory.Faker("sentence")
