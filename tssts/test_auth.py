
import requests
BASE_URL = "http://localhost:5000"

def test_register_user():
    r = requests.post(f"{BASE_URL}/register", json={"name":"Test","phone":"0599999999"})
    assert r.status_code in [201,409]

def test_login_user():
    r = requests.post(f"{BASE_URL}/login", json={"phone":"0599999999"})
    assert r.status_code == 200
