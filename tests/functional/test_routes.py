from iebank_api.models import User
from iebank_api import app


def test_home_route(test_client):
    """
    Test the home route for a successful response.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Update this based on your index.html content


def test_register_route(test_client):
    """
    Test user registration functionality.
    """
    response = test_client.post(
        "/register",
        data={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "initial_balance": "1000.0",
        },
    )
    assert response.status_code == 302  # Expecting a redirect after registration

    # Verify user exists in the database
    with app.app_context():
        user = User.query.filter_by(email="new_user@example.com").first()
        assert user is not None
        assert user.username == "new_user"