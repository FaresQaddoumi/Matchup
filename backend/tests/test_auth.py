def test_auth_signup_login_me_logout(client):
    # signup
    r = client.post("/auth/signup", json={"email": "user@example.com", "password": "secret123"})
    assert r.status_code == 201
    data = r.get_json()
    token = data["token"]
    assert data["email"] == "user@example.com"

    # The token
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.get_json()["email"] == "user@example.com"

    # login existing user
    r = client.post("/auth/login", json={"email": "user@example.com", "password": "secret123"})
    assert r.status_code == 200
    token2 = r.get_json()["token"]
    assert token2

    # logout token2
    r = client.post("/auth/logout", headers={"Authorization": f"Bearer {token2}"})
    assert r.status_code == 200

    # token2 no longer valid after logging out
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert r.status_code == 401
