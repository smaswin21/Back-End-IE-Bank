from iebank_api.models import User, Account, Transaction
import pytest


def test_home_route(test_client):
    """
    Test the home route.
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust if 'Welcome' is present in index.html
