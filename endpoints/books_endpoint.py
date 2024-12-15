import requests


class BooksEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_books(self, params=None):  # None default value helps in situations where the parameter is optional, and its presence is conditional
        url = f'{self.base_url}/books'
        return requests.get(url, params=params)

    def get_book_by_id(self, book_id):
        url = f'{self.base_url}/books/{book_id}'
        return requests.get(url)
