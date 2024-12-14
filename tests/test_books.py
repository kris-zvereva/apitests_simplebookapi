import requests
from config import BASE_URL
from tests.conftest import fake


def test_get_list_of_books():
    """verify the endpoint returns fiction and non-fiction books without query parameters"""
    url = BASE_URL + "/books"
    response = requests.get(url)
    books = response.json()

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert books, "The books list is empty"
    assert any(book['type'] == 'fiction' for book in books), "'fiction' books are missing" # assert that both fiction and non-fiction are present
    assert any(book['type'] == 'non-fiction' for book in books), "'non-fiction' books are missing"


def test_get_list_of_fiction_books():
    """verify filtering of fiction books with the 'type=fiction' query parameter"""
    url = BASE_URL + '/books'
    params = {
        'type': 'fiction'
    }
    response = requests.get(url, params)  # params arg in requests.get() automatically converts the dict into the correct URL-encoded format for query parameters.
    books = response.json()

    assert any(book['type'] == 'fiction' for book in books), "'fiction' books are missing"
    assert any(book['type'] != 'non-fiction' for book in books), "'non-fiction' books are present"


def test_get_list_of_non_fiction_books():
    """verify filtering of non-fiction books with the 'type=non-fiction' query parameter"""
    url = BASE_URL + '/books'
    params = {
        'type': 'non-fiction'
    }
    response = requests.get(url, params)
    books = response.json()

    assert any(book['type'] == 'non-fiction' for book in books), "'non-fiction' books are missing"
    assert any(book['type'] != 'fiction' for book in books), "'fiction' books are present"


def test_get_a_single_book():
    """verify the endpoint returns the book details for a valid book ID"""
    book_id = fake.random_int(min=1, max=6)
    url = BASE_URL + f'/books/{book_id}'
    response = requests.get(url)
    book = response.json()

    assert book['id'] == book_id, \
        f"Expected id {book_id}, but got {book['id']}"
    assert book['name'], "Book name is missing in the response"
    assert book['author'], "Author information is missing in the response"


def test_get_a_single_book_invalid_id():
    """verify error message if /books/:id endpoint got invalid book ID"""
    book_id = fake.random_int(min=21)
    url = BASE_URL + f'/books/{book_id}'
    response = requests.get(url)
    error_message = response.json().get('error')

    assert error_message == f'No book with id {book_id}', \
        f"Expected error message 'No book with id {book_id}', but got {error_message}"
