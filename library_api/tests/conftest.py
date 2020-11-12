import pytest

from pytest_factoryboy import register

from ..api import create_app
from ..extensions import db

from .factories import UserFactory, BookFactory, BookRequestFactory

TEST_SETTINGS = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}


@pytest.fixture
def app():
    app = create_app(settings_override=TEST_SETTINGS)
    with app.app_context():
        db.create_all()
    return app


# Register FactoryBoy factories
register(UserFactory)
register(BookFactory)
register(BookRequestFactory)
