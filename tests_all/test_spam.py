def _token(client, base_url):
    client.post(f"{base_url}/register/", json={"name":"Spam","phone":"0599990005"})
    r = client.post(f"{base_url}/login/", json={"phone":"0599990005"})
    d = r.json()
    return d.get("token") or d.get("access_token")

def test_spam_without_auth(client, base_url):
    r = client.post(f"{base_url}/spam/", json={"phone":"0593333334","category":"Sales","comment":"x"})
    assert r.status_code in (401,403)

def test_spam_with_auth(client, base_url):
    t = _token(client, base_url)
    r = client.post(
        f"{base_url}/spam/",
        json={"phone":"0593333333","category":"Scam","comment":"Automated"},
        headers={"Authorization": f"Bearer {t}"}
    )
    assert r.status_code in (200,201)

def test_spam_missing_fields(client, base_url):
    t = _token(client, base_url)
    r = client.post(f"{base_url}/spam/", json={"phone":""}, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code in (400,422)
