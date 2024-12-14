import pytest
import requests
from config import BASE_URL

def test_api_status():
    url = BASE_URL + '/status'
    response = requests.get(url)

    assert response.status_code == 200

