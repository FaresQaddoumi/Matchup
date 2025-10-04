

from flask import Blueprint, jsonify
from backend.db import query_all


leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

@leaderboard_bp.get("")
def leaderboard():
    
    # Win = 3, Draw = 1, Loss = 0. Tiebreakers: points, goal diff, goals for, and the name
    rows = query_all(
        """
        SELECT m.id,
               m.home_team_id, th.name AS home_name,
               m.away_team_id, ta.name AS away_name,
               m.home_score, m.away_score
        FROM matches m
        JOIN teams th ON th.id = m.home_team_id
        JOIN teams ta ON ta.id = m.away_team_id
        WHERE m.home_score IS NOT NULL AND m.away_score IS NOT NULL
        """
    )

    stats = {}  # Team stats

    def ensure(team_id, name):
        
        if team_id not in stats:
            stats[team_id] = {
                "team_id": team_id,
                "team": name,
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_diff": 0,
                "points": 0,
            }
        return stats[team_id]

    for r in rows:
        h = ensure(r["home_team_id"], r["home_name"])

        a = ensure(r["away_team_id"], r["away_name"])
        hs, as_ = int(r["home_score"]), int(r["away_score"])

        # updates stats for both teams
        h["played"] += 1; a["played"] += 1
        h["goals_for"] += hs; h["goals_against"] += as_
        a["goals_for"] += as_; a["goals_against"] += hs

        
        if hs > as_:
            h["wins"] += 1; a["losses"] += 1
            h["points"] += 3
        elif hs < as_:
            a["wins"] += 1; h["losses"] += 1
            a["points"] += 3
        else:
            h["draws"] += 1; a["draws"] += 1
            h["points"] += 1; a["points"] += 1

    #goal diff
    for t in stats.values():
        t["goal_diff"] = t["goals_for"] - t["goals_against"]

    table = sorted(
        stats.values(),
        key=lambda t: (-t["points"], -t["goal_diff"], -t["goals_for"], t["team"].lower())
    )

    return jsonify(table), 200
