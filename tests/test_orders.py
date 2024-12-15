from tests.conftest import fake, auth_token


def test_create_order(auth_token, headers, orders_endpoint):
    """verify a new order is created"""
    client_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6),
    response = orders_endpoint.create_order(book_id, customer_name=client_name, headers=headers)

    assert response.json().get('created'), f"Expected 'created' to be True, but got {response.json().get('created')}"
    assert response.json().get('orderId'), "Expected 'orderId' to be non-empty"


def test_create_order_no_auth(orders_endpoint):
    """verify the endpoint returns 401 when no auth token is provided"""
    book_id = fake.random_int(min=1, max=6),
    customer_name = fake.name()
    response = orders_endpoint.create_order(book_id, customer_name=customer_name)
    error_message = response.json().get('error')

    assert error_message == 'Missing Authorization header.', f"Unexpected error message: {error_message}"
    assert response.status_code == 401


def test_create_order_old_auth(orders_endpoint):
    """verify the endpoint returns 401 when no auth token is provided"""
    book_id = fake.random_int(min=1, max=6),
    customer_name = fake.name()
    headers = {
        "Authorization": f"Bearer {fake.sha256()}"
    }
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    error_message = response.json().get('error')

    assert error_message == 'Invalid bearer token.', f"Unexpected error message: {error_message}"
    assert response.status_code == 401


def test_check_order_in_list_of_orders(auth_token, headers, orders_endpoint):
    """verify when an order is created it exists in the list of orders"""
    customer_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6)
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    created_order = response.json()
    order_id = created_order['orderId']

    response = orders_endpoint.get_list_of_orders(headers=headers)
    orders = response.json()
    matching_order = None
    for order in orders:
        if order.get('id') == order_id:
            matching_order = order
            break

    assert matching_order, f"Order with ID {order_id} not found in the list of orders"
    assert matching_order.get('bookId') == book_id, (
        f"Expected bookId {book_id}, got {matching_order.get('bookId')}"
    )
    assert matching_order.get('customerName') == customer_name, (
        f"Expected customerName {customer_name}, got {matching_order.get('customerName')}"
    )


def test_get_order_by_id(auth_token, orders_endpoint, headers):
    """verify the endpoint gets order details for a valid order ID"""
    customer_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6)
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    created_order = response.json()
    order_id = created_order['orderId']

    response = orders_endpoint.get_order_by_id(order_id, headers=headers)
    response_data = response.json()

    assert response_data.get('bookId') == book_id
    assert response_data.get('customerName') == customer_name, f"Expected customerName equals {customer_name}, got {response_data.get('customerName')}"
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}"


def test_get_order_invalid_id(headers, orders_endpoint):
    """verify the endpoint returns 404 when accessing an order with an invalid ID"""
    order_id = fake.uuid4().replace('-', '')[:21]
    response = orders_endpoint.get_order_by_id(order_id, headers=headers)

    assert response.json().get('error') == f'No order with id {order_id}.'
    assert response.status_code == 404


def test_update_order(auth_token, headers, orders_endpoint):
    """verify the endpoint allows updating order's customer name"""
    customer_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6)
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    created_order = response.json()
    order_id = created_order['orderId']
    updated_name = fake.name()
    response = orders_endpoint.update_order(order_id, updated_name, headers=headers)

    assert response.status_code == 204

    response = orders_endpoint.get_order_by_id(order_id, headers=headers)
    print(response.json())
    assert response.json().get('customerName') == updated_name, \
        f"Expected customerName equals {updated_name}, got {response.json().get('customerName')}"


def test_delete_order(auth_token, headers, orders_endpoint):
    """verify the endpoint supports deleting an order"""
    customer_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6)
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    created_order = response.json()
    order_id = created_order['orderId']
    response = orders_endpoint.delete_order(order_id, headers=headers)

    assert response.status_code == 204

def test_get_deleted_order(auth_token, headers, orders_endpoint):
    """verify accessing a deleted order returns a 404 with the error message"""
    customer_name = auth_token['client_name']
    book_id = fake.random_int(min=1, max=6)
    response = orders_endpoint.create_order(book_id, customer_name=customer_name, headers=headers)
    created_order = response.json()
    order_id = created_order['orderId']
    orders_endpoint.delete_order(order_id, headers=headers)
    response = orders_endpoint.get_order_by_id(order_id, headers=headers)

    assert response.json().get('error') == f'No order with id {order_id}.'
    assert response.status_code == 404
