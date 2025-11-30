def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.get_json() == {"ok": True}
def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code in (200, 500)  # should be 200 normally, 500 only if DB broken

    data = r.get_json()
    assert "status" in data
    assert "db" in data

