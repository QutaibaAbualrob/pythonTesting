
import requests
BASE_URL = "http://localhost:5000"

def test_spam_report(auth_token):
    headers={"Authorization":f"Bearer {auth_token}"}
    r = requests.post(f"{BASE_URL}/spam", headers=headers,
        json={"phone":"0591234567","category":"Scam","comment":"Auto"})
    assert r.status_code in [200,409]
