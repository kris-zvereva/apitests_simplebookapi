import pytest
import requests
from faker import Faker
from config import BASE_URL
from endpoints.books_endpoint import BooksEndpoint
from endpoints.orders_endpoint import OrdersEndpoint

fake = Faker() #to instantiate the Faker class


@pytest.fixture
def auth_token():
    url = BASE_URL + "/api-clients/"
    payload = {
        "clientName": fake.name(),
        "clientEmail": fake.email(),
    }
    response = requests.post(url, json=payload)
    return {
        'client_name': payload.get('clientName'),
        'client_email': payload.get('clientEmail'),
        'token': response.json().get('accessToken')
        }


@pytest.fixture
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token['token']}"}


@pytest.fixture
def books_endpoint():
    """fixture to create a BooksEndpoint instance"""
    return BooksEndpoint(BASE_URL)


@pytest.fixture
def orders_endpoint():
    """fixture to create an OrdersEndpoint instance"""
    return OrdersEndpoint(BASE_URL)

