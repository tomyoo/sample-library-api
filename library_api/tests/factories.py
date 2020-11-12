"""
Test Factories
"""

import factory
from faker import Factory as FakerFactory

from library_api.extensions import db
from library_api.models.models import User, Book, BookRequest

faker = FakerFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    """User factory"""

    email = factory.LazyAttribute(lambda x: faker.email())

    class Meta:
        model = User


class BookFactory(BaseFactory):
    """Book factory"""

    title = factory.LazyAttribute(lambda x: faker.sentence())

    class Meta:
        model = Book


class BookRequestFactory(BaseFactory):
    """BookRequest factory"""

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BookRequest
