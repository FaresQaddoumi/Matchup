def test_matches_flow(client):
    #creating the teams
    a = client.post("/teams", json={"name": "Team A"}).get_json()
    b = client.post("/teams", json={"name": "Team B"}).get_json()

    # schedule a match
    r = client.post("/matches", json={
        "home_team_id": a["id"],
        "away_team_id": b["id"],
        "scheduled_at": "2026-05-20 18:00"
    })
    assert r.status_code == 201
    match = r.get_json()
    mid = match["id"]

    # list upcoming
    r = client.get("/matches?upcoming=1")
    assert r.status_code == 200
    assert any(x["id"] == mid for x in r.get_json())

    # set result
    r = client.put(f"/matches/{mid}/result", json={"home_score": 2, "away_score": 1})
    assert r.status_code == 200
    m2 = r.get_json()
    assert (m2["home_score"], m2["away_score"]) == (2, 1)

    # list played
    r = client.get("/matches?played=1")
    assert r.status_code == 200
    assert any(x["id"] == mid for x in r.get_json())
