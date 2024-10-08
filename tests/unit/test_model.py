from iebank_api.models import Account
import pytest

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
    account.__deactivate__()
    assert account.status == 'Inactive'

def test_update_account_status():
    """
    GIVEN a Account model
    WHEN the status is updated
    THEN check the status is updated correctly
    """
    account = Account('John Doe', '€', "Spain")
    account.status = 'Inactive'
    assert account.status == 'Inactive'
