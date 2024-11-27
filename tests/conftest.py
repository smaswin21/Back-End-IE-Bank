import pytest
from iebank_api import app, db
from iebank_api.models import User, Account, Transaction, TransactionType
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def test_client():
    """
    Set up a Flask test client with an in-memory SQLite database.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def clear_database():
    """
    Clears the database before each test to avoid duplicate entries.
    """
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def new_user():
    """
    Create and return a new test user in the database.
    """
    with app.app_context():
        user = User(
            username="test_user",
            email="test_user@example.com",
            password=generate_password_hash("password123"),
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def new_account(new_user):
    """
    Create and return a new test account linked to the test user.
    """
    with app.app_context():
        account = Account(
            name="Test Account",
            currency="USD",
            country="USA",
            user_id=new_user.id,
            balance=500.0,
        )
        db.session.add(account)
        db.session.commit()
        return account


@pytest.fixture
def new_transaction(new_account):
    """
    Create and return a test transaction associated with the test account.
    """
    with app.app_context():
        transaction = Transaction(
            amount=100.0,
            currency="USD",
            account_id=new_account.id,
            transaction_type=TransactionType.DEPOSIT,
            user_id=new_account.user_id,
            description="Test deposit transaction",
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
