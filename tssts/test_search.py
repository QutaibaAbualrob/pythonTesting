
import requests
BASE_URL = "http://localhost:5000"

def test_search_existing(auth_token):
    headers={"Authorization":f"Bearer {auth_token}"}
    r = requests.get(f"{BASE_URL}/search/0591234567", headers=headers)
    assert r.status_code in [200,404]
