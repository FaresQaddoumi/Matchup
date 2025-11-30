def test_metrics_prometheus_format(client):
    response = client.get("/metrics_prom")
    assert response.status_code == 200

    body = response.data.decode("utf-8")
    assert "matchup_teams_count" in body
    assert "matchup_matches_count" in body
    #Prometheus format
    assert "# HELP matchup_teams_count" in body
    assert "# TYPE matchup_teams_count gauge" in body
