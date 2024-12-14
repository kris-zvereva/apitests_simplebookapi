import pytest
import requests
from faker import Faker
from config import BASE_URL


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
def create_order(auth_token, headers):
    client_name = auth_token['client_name']
    url = BASE_URL + '/orders'
    payload = {
        'bookId': fake.random_int(min=1, max=6),
        'customerName': client_name,
    }
    response = requests.post(url, headers=headers, json=payload)

    return {
        'order_id': response.json().get('orderId'),
        'book_id': payload['bookId'],
        'customer_name': payload['customerName'],
    }

