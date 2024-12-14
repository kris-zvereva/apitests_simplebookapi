import requests
from config import BASE_URL
from tests.conftest import fake


def test_create_order(auth_token, headers):
    """verify a new order is created"""
    client_name = auth_token['client_name']
    url = BASE_URL + '/orders'
    payload = {
        'bookId': 1,
        'customerName': client_name,
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

    assert response.json().get('created'), f"Expected 'created' to be True, but got {response.json().get('created')}"
    assert response.json().get('orderId'), "Expected 'orderId' to be non-empty"


def test_create_order_no_auth():
    """verify the endpoint returns 401 when no auth token is provided"""
    url = BASE_URL + "/orders"
    payload = {
            "bookId": fake.random_int(min=1, max=6),
            "customerName": fake.name()
    }
    response = requests.post(url, json=payload)

    error_message = response.json().get('error')
    assert error_message == 'Missing Authorization header.', f"Unexpected error message: {error_message}"
    assert response.status_code == 401


def test_get_order(create_order, headers):
    """verify the endpoint gets order details for a valid order ID"""

    order_id = create_order['order_id']
    book_id = create_order['book_id']
    customer_name = create_order['customer_name']

    url = BASE_URL + f'/orders/{order_id}'
    response = requests.get(url, headers=headers)
    response_data = response.json()

    assert response_data.get('bookId') == book_id
    assert response_data.get('customerName') == customer_name, f"Expected customerName equals {customer_name}, got {response_data.get('customerName')}"
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}"


def test_get_order_invalid_id(headers):
    """verify the endpoint returns 404 when accessing an order with an invalid ID"""
    order_id = fake.uuid4().replace('-', '')[:21]
    url = BASE_URL + f'/orders/{order_id}'
    response = requests.get(url, headers=headers)

    assert response.json().get('error') == f'No order with id {order_id}.'
    assert response.status_code == 404


def test_update_order(create_order, headers):
    order_id = create_order['order_id']
    url = BASE_URL + f'/orders/{order_id}'
    payload = {
        'customerName': fake.name()
    }
    updated_name = payload['customerName']
    response = requests.patch(url, headers=headers, json=payload)
    assert response.status_code == 204

    url = BASE_URL + f'/orders/{order_id}'
    response = requests.get(url, headers=headers)

    assert response.json().get('customerName') == updated_name, \
        f"Expected customerName equals {updated_name}, got {response.json().get('customerName')}"


def test_delete_order(create_order, headers):
    order_id = create_order['order_id']
    url = BASE_URL + f'/orders/{order_id}'
    response = requests.delete(url, headers=headers)

    assert response.status_code == 204

    url = BASE_URL + f'/orders/{order_id}'
    response = requests.get(url, headers=headers)

    assert response.json().get('error') == f'No order with id {order_id}.'
    assert response.status_code == 404

