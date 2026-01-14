def test_login_valid_returns_token(client, base_url):
    client.post(f"{base_url}/register", json={"name":"Login","phone":"0599990003"})
    r = client.post(f"{base_url}/login", json={"phone":"0599990003"})
    assert r.status_code == 200
    data = r.json()
    assert ("token" in data) or ("access_token" in data)

def test_login_unregistered(client, base_url):
    r = client.post(f"{base_url}/login", json={"phone":"0599999998"})
    assert r.status_code in (401,404)

def test_login_invalid_input(client, base_url):
    r = client.post(f"{base_url}/login", json={})
    assert r.status_code in (400,422)
