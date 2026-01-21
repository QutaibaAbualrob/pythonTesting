import os, requests, pytest
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')
@pytest.fixture
def client():
    return requests.Session()
@pytest.fixture
def base_url():
    return BASE_URL
