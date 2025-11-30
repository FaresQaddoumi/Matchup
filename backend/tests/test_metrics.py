def test_metrics_basic(client):
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.get_json()
    assert "teams_count" in data
    assert "matches_count" in data
    assert isinstance(data["teams_count"], int)
    assert isinstance(data["matches_count"], int)
