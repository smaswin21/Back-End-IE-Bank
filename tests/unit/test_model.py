from iebank_api.models import User, Account, Transaction, TransactionType
from iebank_api import db


def test_create_user(new_user):
    """
    Test creating a new user instance.
    """
    assert new_user.username == "test_user"
    assert new_user.email == "test_user@example.com"
    assert new_user.password == "hashed_password"
    assert new_user.status == "Active"
    assert new_user.admin is False


def test_create_account(new_account):
    """
    Test creating a new account instance.
    """
    assert new_account.name == "Test Account"
    assert new_account.currency == "USD"
    assert new_account.country == "USA"
    assert new_account.balance == 1000.0
    assert new_account.status == "Active"


def test_transaction_model(test_client, new_user, new_account):
    """
    Test creating and associating a transaction with a user and account.
    """
    with test_client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

        account = Account(
            name="Savings Account",
            currency="USD",
            country="USA",
            user_id=new_user.id,
            balance=500.0
        )
        db.session.add(account)
        db.session.commit()

        transaction = Transaction(
            amount=100.0,
            currency="USD",
            account_id=account.id,
            transaction_type=TransactionType.DEPOSIT,
            user_id=new_user.id
        )
        db.session.add(transaction)
        db.session.commit()

        assert transaction.amount == 100.0
        assert transaction.currency == "USD"
        assert transaction.account_id == account.id
        assert transaction.transaction_type == TransactionType.DEPOSIT
        assert transaction.user_id == new_user.id


def test_user_deactivation(new_user):
    """
    Test user deactivation method.
    """
    new_user.deactivate()
    assert new_user.status == "Inactive"


def test_account_deactivation(new_account):
    """
    Test account deactivation method.
    """
    new_account.deactivate()
    assert new_account.status == "Inactive"


def test_simple_transaction(new_user, new_account):
    """
    Test that a basic transaction can be created and properties are set correctly.
    """
    transaction = Transaction(
        amount=200.0,
        currency="USD",
        account_id=new_account.id,
        transaction_type=TransactionType.WITHDRAW,
        user_id=new_user.id,
        description="Test Transaction"
    )

    assert transaction.amount == 200.0
    assert transaction.currency == "USD"
    assert transaction.account_id == new_account.id
    assert transaction.transaction_type == TransactionType.WITHDRAW
    assert transaction.user_id == new_user.id
    assert transaction.description == "Test Transaction"

def test_account_number_generation(new_account):
    """
    Test that a unique account number is generated for a new account.
    """
    # Check that the account number is a string of the correct length (20 digits)
    assert isinstance(new_account.account_number, str)
    assert len(new_account.account_number) == 20
    assert new_account.account_number.isdigit()
