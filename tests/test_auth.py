import requests
from tests.conftest import fake
from config import BASE_URL


def test_create_user_get_auth_token():
    """verify auth token is generated for valid name and email"""
    url = BASE_URL + "/api-clients/"
    payload = {
            "clientName": fake.name(),
            "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)

    assert response.json().get("accessToken"), "Authentication token was not returned in the response."
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"


def test_create_same_user_twice():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)

    print(response.json())
    url = BASE_URL + "/api-clients/"

    response = requests.post(url, json=payload)
    print(response.json())
    error_message = response.json().get('error')
    assert error_message == 'API client already registered. Try a different email.', f"Unexpected error message: {error_message}"
    assert response.status_code == 409


def test_create_user_same_client_name():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)
    client_name = response.json().get('clientName')
    print(response.json())
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": client_name,
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)
    print(response.json())
    error_message = response.json().get('error')
    assert error_message == 'Invalid or missing client name.', f"Unexpected error message: {error_message}"
    assert response.status_code == 400


def test_create_user_same_email():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)
    client_email = response.json().get('clientEmail')
    print(response.json())
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
        "clientEmail": client_email,
    }
    response = requests.post(url, json=payload)
    print(response.json())
    error_message = response.json().get('error')
    assert error_message == 'Invalid or missing client email.', f"Unexpected error message: {error_message}"
    assert response.status_code == 400

def test_create_user_no_client_name():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)
    print(response.json())
    error_message = response.json().get('error')
    assert error_message == 'Invalid or missing client name.', f"Unexpected error message: {error_message}"
    assert response.status_code == 400

def test_create_user_no_email():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
    }
    response = requests.post(url, json=payload)
    print(response.json())
    error_message = response.json().get('error')
    assert error_message == 'Invalid or missing client email.', f"Unexpected error message: {error_message}"
    assert response.status_code == 400
