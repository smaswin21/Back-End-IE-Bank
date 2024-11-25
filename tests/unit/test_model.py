from iebank_api.models import User, Account, Transaction, TransactionType
from iebank_api import app, db

from iebank_api.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import pytest
from iebank_api import db
from iebank_api.models import User, Account, Transaction, TransactionType
from datetime import datetime, timezone


def test_unique_username(test_client):
    """
    Ensure that `username` must be unique.
    """
    with app.app_context():
        user1 = User(username="unique_user", email="unique1@example.com", password="password1")
        user2 = User(username="unique_user", email="unique2@example.com", password="password2")  # Duplicate username

        db.session.add(user1)
        db.session.commit()

        db.session.add(user2)
        with pytest.raises(Exception):  # Adding a duplicate username should raise an exception
            db.session.commit()


def test_unique_email(test_client):
    """
    Ensure that `email` must be unique.
    """
    with app.app_context():
        user1 = User(username="user1", email="duplicate@example.com", password="password1")
        user2 = User(username="user2", email="duplicate@example.com", password="password2")  # Duplicate email

        db.session.add(user1)
        db.session.commit()

        db.session.add(user2)
        with pytest.raises(Exception):  # Adding a duplicate email should raise an exception
            db.session.commit()


def test_password_hashing(test_client):
    """
    Ensure that passwords are stored securely as hashes.
    """
    with app.app_context():
        plain_password = "securepassword"
        hashed_password = generate_password_hash(plain_password)

        user = User(username="secure_user", email="secure_user@example.com", password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Retrieve user and verify the hashed password
        retrieved_user = User.query.filter_by(username="secure_user").first()
        assert check_password_hash(retrieved_user.password, plain_password)  # Password matches


def test_default_status(test_client):
    """
    Ensure that the `status` field defaults to "Active".
    """
    with app.app_context():
        user = User(username="status_user", email="status_user@example.com", password="password123")
        db.session.add(user)
        db.session.commit()

        # Retrieve user and verify default status
        retrieved_user = User.query.filter_by(username="status_user").first()
        assert retrieved_user.status == "Active"  # Default is "Active"
