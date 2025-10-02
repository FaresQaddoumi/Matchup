
from flask import Blueprint, request, jsonify
from sqlite3 import IntegrityError
from db import query_all, query_one, execute
from datetime import datetime

matches_bp = Blueprint("matches", __name__, url_prefix="/matches")

def parse_iso_when_present(value):
    if not value:
        return None
    s = value.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).isoformat(timespec="minutes")
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s).isoformat(timespec="minutes")
    except ValueError:
        return None

def match_to_dict(row):
    return {
        "id": row["id"],
        "home_team_id": row["home_team_id"],
        "home_team_name": row["home_team_name"],
        "away_team_id": row["away_team_id"],
        "away_team_name": row["away_team_name"],
        "scheduled_at": row["scheduled_at"],
        "home_score": row["home_score"],
        "away_score": row["away_score"],
        "created_at": row["created_at"],
    }

def single_match_by_id(match_id):
    return query_one(
        """
        SELECT m.id, m.home_team_id, m.away_team_id, m.scheduled_at,
               m.home_score, m.away_score, m.created_at,
               th.name AS home_team_name, ta.name AS away_team_name
        FROM matches m
        JOIN teams th ON th.id = m.home_team_id
        JOIN teams ta ON ta.id = m.away_team_id
        WHERE m.id = ?
        """,
        (match_id,),
    )

# --- routes ---


@matches_bp.post("")
def create_match():
    data = request.get_json(silent=True) or {}
    home_id = data.get("home_team_id")
    away_id = data.get("away_team_id")
    when_in = data.get("scheduled_at")
    if home_id is None or away_id is None:
        return jsonify({"error": "home_team_id and away_team_id are required"}), 400
    if str(home_id) == str(away_id):
        return jsonify({"error": "home_team_id and away_team_id must be different"}), 400
    if not query_one("SELECT id FROM teams WHERE id = ?", (home_id,)):
        return jsonify({"error": f"home team {home_id} not found"}), 404
    if not query_one("SELECT id FROM teams WHERE id = ?", (away_id,)):
        return jsonify({"error": f"away team {away_id} not found"}), 404
    when_iso = parse_iso_when_present(when_in)
    if when_in and not when_iso:
        return jsonify({"error": "scheduled_at must be ISO-like (YYYY-MM-DD or YYYY-MM-DD HH:MM)"}), 400
    try:
        match_id = execute(
            "INSERT INTO matches(home_team_id, away_team_id, scheduled_at) VALUES(?, ?, ?)",
            (home_id, away_id, when_iso),
        )
        row = single_match_by_id(match_id)
        return jsonify(match_to_dict(row)), 201
    except IntegrityError as e:
        return jsonify({"error": f"db error: {str(e)}"}), 409


@matches_bp.get("")
def list_matches():
    played = request.args.get("played")
    upcoming = request.args.get("upcoming")
    base_sql = """
        SELECT m.id, m.home_team_id, m.away_team_id, m.scheduled_at,
               m.home_score, m.away_score, m.created_at,
               th.name AS home_team_name, ta.name AS away_team_name
        FROM matches m
        JOIN teams th ON th.id = m.home_team_id
        JOIN teams ta ON ta.id = m.away_team_id
    """
    where = []
    params = []
    if played == "1":
        where.append("m.home_score IS NOT NULL AND m.away_score IS NOT NULL")
    if upcoming == "1":
        where.append("m.home_score IS NULL AND m.away_score IS NULL")
    if where:
        base_sql += " WHERE " + " AND ".join(where)
    base_sql += " ORDER BY COALESCE(m.scheduled_at, m.created_at) ASC, m.id ASC"
    rows = query_all(base_sql, tuple(params))
    return jsonify([match_to_dict(r) for r in rows]), 200


@matches_bp.put("/<int:match_id>/result")
def set_result(match_id):
    data = request.get_json(silent=True) or {}
    if "home_score" not in data or "away_score" not in data:
        return jsonify({"error": "home_score and away_score are required"}), 400
    try:
        hs = int(data["home_score"])
        as_ = int(data["away_score"])
    except (TypeError, ValueError):
        return jsonify({"error": "scores must be integers"}), 400
    if hs < 0 or as_ < 0:
        return jsonify({"error": "scores must be >= 0"}), 400
    exists = query_one("SELECT id FROM matches WHERE id = ?", (match_id,))
    if not exists:
        return jsonify({"error": f"match {match_id} not found"}), 404
    execute("UPDATE matches SET home_score = ?, away_score = ? WHERE id = ?", (hs, as_, match_id))
    row = single_match_by_id(match_id)
    return jsonify(match_to_dict(row)), 200
