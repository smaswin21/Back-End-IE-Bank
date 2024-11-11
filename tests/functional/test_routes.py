from iebank_api import app
import pytest


def test_register(testing_client, user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password, admin, status fields are defined correctly
    """
    print(user)
    response = testing_client.post("/register",
                                   data={"username": user.username, "email": user.email, "password": "my_password", "confirm_password": "my_password"},
                                   follow_redirects=True)
    assert response.status_code == 200

def test_login(testing_client):
    """
    GIVEN a User model created in fixture
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post("/login", json={"username": "created", "password": "my_password"})
    assert response.status_code == 200



def test_get_accounts(testing_client, user):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.post("/login", json={"username": "created", "password": "my_password"})

    # Ensure login was successful
    assert response.status_code == 200

    # Extract the session cookie properly from the response headers
    session_cookie = None
    for header in response.headers.getlist("Set-Cookie"):
        if 'session=' in header:
            session_cookie = header.split(';')[0].split('=')[1]  # Extract the session value

    assert session_cookie is not None  # Ensure the session cookie was found

    # Use the extracted session cookie for the GET request (without adding a period before the session value)
    response = testing_client.get('/accounts', headers={"Cookie": f"session=.{session_cookie}"}, follow_redirects=True)
    assert response.status_code == 200


def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country' : 'Spain'})
    assert response.status_code == 200

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (PUT) with an name
    THEN check the response is valid
    """
    testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )
    response = testing_client.put("/accounts/1", json={"name": "Dev-Aswin"})
    assert response.status_code == 200

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page posted to delete (DELETE)
    THEN check the response is valid
    """

    # Create
    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )

    # Delete
    response = testing_client.delete("/accounts/1")
    assert response.status_code == 200

def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """

    # Create
    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )

    # Get by ID
    response = testing_client.get("/accounts/1")
    assert response.status_code == 200
