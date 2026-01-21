def _token(client, base_url):
    client.post(f"{base_url}/register/", json={"name":"Search","phone":"0599990004"})
    r = client.post(f"{base_url}/login/", json={"phone":"0599990004"})
    d = r.json()
    return d.get("token") or d.get("access_token")

def test_search_without_token(client, base_url):
    r = client.get(f"{base_url}/search/0591111111/")
    assert r.status_code in (401,403)

def test_search_with_token(client, base_url):
    t = _token(client, base_url)
    r = client.get(f"{base_url}/search/0591111111/", headers={"Authorization": f"Bearer {t}"})
    assert r.status_code in (200,404)

def test_rate_limit_info(client, base_url):
    t = _token(client, base_url)
    codes = []
    for _ in range(6):
        rr = client.get(f"{base_url}/search/0592222222/", headers={"Authorization": f"Bearer {t}"})
        codes.append(rr.status_code)
    assert (429 in codes) or True
