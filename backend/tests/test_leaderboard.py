def test_leaderboard_scoring_and_sort(client):
    # Teams
    alpha = client.post("/teams", json={"name": "Alpha"}).get_json()
    beta  = client.post("/teams", json={"name": "Beta"}).get_json()
    gamma = client.post("/teams", json={"name": "Gamma"}).get_json()

  
    m1 = client.post("/matches", json={"home_team_id": alpha["id"], "away_team_id": beta["id"]}).get_json()
    m2 = client.post("/matches", json={"home_team_id": beta["id"],  "away_team_id": gamma["id"]}).get_json()
    m3 = client.post("/matches", json={"home_team_id": gamma["id"], "away_team_id": alpha["id"]}).get_json()

    # Results:
    
    client.put(f"/matches/{m1['id']}/result", json={"home_score": 2, "away_score": 0})
    
    client.put(f"/matches/{m2['id']}/result", json={"home_score": 1, "away_score": 1})
    
    client.put(f"/matches/{m3['id']}/result", json={"home_score": 3, "away_score": 1})


    r = client.get("/leaderboard")
    assert r.status_code == 200
    table = r.get_json()
    pts = {row["team"]: row["points"] for row in table}
    assert pts["Alpha"] == 3
    assert pts["Beta"]  == 1
    assert pts["Gamma"] == 4

    # Gamma should be first, then Alpha,and lastly Beta
    assert table[0]["team"] == "Gamma"
