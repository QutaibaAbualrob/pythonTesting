def test_register_valid(client, base_url):
    r = client.post(f"{base_url}/register", json={"name":"Test","phone":"0599990001"})
    assert r.status_code in (200,201)

def test_register_duplicate(client, base_url):
    client.post(f"{base_url}/register", json={"name":"A","phone":"0599990002"})
    r = client.post(f"{base_url}/register", json={"name":"B","phone":"0599990002"})
    assert r.status_code in (400,409)

def test_register_empty_phone(client, base_url):
    r = client.post(f"{base_url}/register", json={"name":"C","phone":""})
    assert r.status_code in (400,422)
