import pytest
from iebank_api import app, db
from iebank_api.models import User, Account
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    """
    Fixture to set up the Flask test client with an in-memory SQLite database.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture
def new_user():
    """
    Fixture to create and persist a new user in the database.
    """
    with app.app_context():
        user = User(
            username="test_user",
            email="test_user@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def new_account(new_user):
    """
    Fixture to create and persist a new account for the test user in the database.
    """
    with app.app_context():
        account = Account(
            name="Test Account",
            currency="USD",
            country="USA",
            user_id=new_user.id,
            balance=1000.0
        )
        db.session.add(account)
        db.session.commit()
        return account


@pytest.fixture
def admin_user():
    """
    Fixture to create and persist an admin user in the database.
    """
    with app.app_context():
        admin = User(
            username="admin_user",
            email="admin_user@example.com",
            password=generate_password_hash("admin123"),
            admin=True
        )
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def login_user(test_client, new_user):
    """
    Log in the user and set session.
    """
    with test_client:
        test_client.post('/login', data={
            'username': new_user.username,
            'password': 'password123'  # Ensure this matches the test user's password
        })

@pytest.fixture
def new_user():
    """
    Create and persist a new test user.
    """
    with app.app_context():
        user = User(
            username="test_user",
            email="test_user@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
        return user
