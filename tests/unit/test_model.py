from iebank_api.models import Account, User
import pytest

# Fixtures are used:
"""
account : basic account object
user : a simple user object (username, user@iebank.com, my_password, admin=False)
admin : a simple admin object (admin1, admin@iebank.com, my_password1, admin=True)
"""

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', "Spain")
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == "Spain"
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_deactivate_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the status is set to Inactive
    """
    account = Account('John Doe', '€', "Spain")
    account.deactivate()
    assert account.status == 'Inactive'

# testing user object
def test_user_object(user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password, admin, status fields are defined correctly
    """
    assert user.username == 'username'
    assert user.email == 'user@iebank.com'
