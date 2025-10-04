def test_teams_crud(client):
    # create two teams
    r = client.post("/teams", json={"name": "Real Madrid", "city": "Madrid"})
    assert r.status_code == 201
    t1 = r.get_json()

    r = client.post("/teams", json={"name": "FC Barcelona", "city": "Barcelona"})
    assert r.status_code == 201
    t2 = r.get_json()

    
    r = client.post("/teams", json={"name": "Real Madrid"})
    assert r.status_code == 409

    # list
    r = client.get("/teams")
    assert r.status_code == 200
    teams = r.get_json()
    assert any(x["id"] == t1["id"] for x in teams)
    assert any(x["id"] == t2["id"] for x in teams)

   
    r = client.get(f"/teams/{t1['id']}")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Real Madrid"

    # update
    r = client.put(f"/teams/{t1['id']}", json={"city": "Madrid City"})
    assert r.status_code == 200
    assert r.get_json()["city"] == "Madrid City"

    # delete
    r = client.delete(f"/teams/{t2['id']}")
    assert r.status_code == 200

    # 404 on deleted team
    r = client.get(f"/teams/{t2['id']}")
    assert r.status_code == 404
