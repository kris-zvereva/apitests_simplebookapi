from tests.conftest import fake


def test_get_list_of_books(books_endpoint):
    """verify the endpoint returns fiction and non-fiction books without query parameters"""
    response = books_endpoint.get_books() # call the method on the instance
    books = response.json()

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert books, "The books list is empty"
    assert any(book['type'] == 'fiction' for book in books), "'fiction' books are missing" # assert that both fiction and non-fiction are present
    assert any(book['type'] == 'non-fiction' for book in books), "'non-fiction' books are missing"


def test_get_list_of_fiction_books(books_endpoint):
    """verify filtering of fiction books with the 'type=fiction' query parameter"""
    params = {
        'type': 'fiction'
    }
    response = books_endpoint.get_books(params=params)
    books = response.json()

    assert any(book['type'] == 'fiction' for book in books), "'fiction' books are missing"
    assert any(book['type'] != 'non-fiction' for book in books), "'non-fiction' books are present"


def test_get_list_of_non_fiction_books(books_endpoint):
    """verify filtering of non-fiction books with the 'type=non-fiction' query parameter"""
    params = {
        'type': 'non-fiction'
    }
    response = books_endpoint.get_books(params=params)
    books = response.json()

    assert any(book['type'] == 'non-fiction' for book in books), "'non-fiction' books are missing"
    assert any(book['type'] != 'fiction' for book in books), "'fiction' books are present"


def test_get_a_single_book(books_endpoint):
    """verify the endpoint returns the book details for a valid book ID"""
    book_id = fake.random_int(min=1, max=6)
    response = books_endpoint.get_book_by_id(book_id)
    book = response.json()

    assert book['id'] == book_id, \
        f"Expected id {book_id}, but got {book['id']}"
    assert book['name'], "Book name is missing in the response"
    assert book['author'], "Author information is missing in the response"


def test_get_a_single_book_invalid_id(books_endpoint):
    """verify error message if /books/:id endpoint got invalid book ID"""
    book_id = fake.random_int(min=21)
    response = books_endpoint.get_book_by_id(book_id)
    error_message = response.json().get('error')

    assert error_message == f'No book with id {book_id}', \
        f"Expected error message 'No book with id {book_id}', but got {error_message}"
