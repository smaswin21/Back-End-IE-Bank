import pytest
from iebank_api import app, db
from iebank_api.models import User, Account


@pytest.fixture(scope='module')
def test_client():
    # Configure Flask app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  # Create tables
        yield testing_client

        # Clean up
        with app.app_context():
            db.drop_all()


@pytest.fixture
def new_user():
    """
    Fixture to create a new user instance.
    """
    user = User(username="test_user", email="test_user@example.com", password="hashed_password")
    return user


@pytest.fixture
def new_account(new_user):
    """
    Fixture to create a new account instance for the test user.
    """
    account = Account(name="Test Account", currency="USD", country="USA", user_id=new_user.id, balance=1000.0)
    return account
