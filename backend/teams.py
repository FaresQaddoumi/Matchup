
from flask import Blueprint, request, jsonify 
from sqlite3 import IntegrityError 
from backend.db import query_all, query_one, execute 

teams_bp = Blueprint("teams", __name__, url_prefix="/teams") # Blueprint for teams routes

def team_to_dict(row): # convert DB row to dict
    return {
        "id": row["id"], 
        "name": row["name"],
        "city": row["city"],
        "created_at": row["created_at"],
    }

@teams_bp.get("") 
def list_teams():
    rows = query_all("SELECT id, name, city, created_at FROM teams ORDER BY name ASC")
    return jsonify([team_to_dict(r) for r in rows]), 200

@teams_bp.get("/<int:team_id>") # get a specific team by ID
def get_team(team_id: int):
    row = query_one("SELECT id, name, city, created_at FROM teams WHERE id = ?", (team_id,))
    if not row:
        return jsonify({"error": f"team {team_id} not found"}), 404
    return jsonify(team_to_dict(row)), 200

@teams_bp.post("") # create a new team
def create_team():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    city = (data.get("city") or "").strip() or None

    if not name:
        return jsonify({"error": "name is required"}), 400 

    try:
        team_id = execute("INSERT INTO teams(name, city) VALUES(?, ?)", (name, city)) 
        row = query_one("SELECT id, name, city, created_at FROM teams WHERE id = ?", (team_id,)) 
        return jsonify(team_to_dict(row)), 201 
    except IntegrityError:
        return jsonify({"error": f"name '{name}' already exists"}), 409 

@teams_bp.put("/<int:team_id>") # update an existing team
def update_team(team_id: int):
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "nothing to update"}), 400 

    current = query_one("SELECT id, name, city FROM teams WHERE id = ?", (team_id,)) 
    if not current:
        return jsonify({"error": f"team {team_id} not found"}), 404 

    new_name = data.get("name", current["name"])
    new_city = data.get("city", current["city"])

    if new_name is None or str(new_name).strip() == "":
        return jsonify({"error": "name cannot be empty"}), 400

    try: 
        execute(
            "UPDATE teams SET name = ?, city = ? WHERE id = ?",
            (str(new_name).strip(), (new_city or None), team_id), 
        )
        row = query_one("SELECT id, name, city, created_at FROM teams WHERE id = ?", (team_id,))
        return jsonify(team_to_dict(row)), 200
    except IntegrityError:
        return jsonify({"error": f"name '{new_name}' already exists"}), 409

@teams_bp.delete("/<int:team_id>") # delete a team
def delete_team(team_id: int):
    row = query_one("SELECT id FROM teams WHERE id = ?", (team_id,))
    if not row:
        return jsonify({"error": f"team {team_id} not found"}), 404
    execute("DELETE FROM teams WHERE id = ?", (team_id,))
    return jsonify({"ok": True, "deleted_id": team_id}), 200
