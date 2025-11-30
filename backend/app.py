import os
print("Starting app.py") # debug

from flask import Flask, jsonify, Response
from backend.db import get_db, close_db, init_db
from backend.teams import teams_bp
from backend.matches import matches_bp
from backend.leaderboard import leaderboard_bp
from backend.auth import auth_bp

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})



@app.before_request
def _open_db():
    get_db()  # open db


@app.teardown_appcontext
def _close_db(exception):
    close_db()  # close db


@app.route("/")
def home():
    return "Matchup backend is running :)"

@app.route("/health", methods=["GET"])
def health():
    try:
        db = get_db()
        
        db.execute("SELECT 1")
        return jsonify({
            "status": "ok",
            "db": "ok"
        }), 200
    except Exception as e:
       
        return jsonify({
            "status": "error",
            "db": "error",
            "details": str(e)
        }), 500
    
@app.route("/metrics", methods=["GET"])
def metrics():
    db = get_db()
    # Adjust table names if yours are different, but they’re very likely "teams" and "matches"
    teams_count = db.execute("SELECT COUNT(*) FROM teams").fetchone()[0]
    matches_count = db.execute("SELECT COUNT(*) FROM matches").fetchone()[0]

    return jsonify({
        "teams_count": teams_count,
        "matches_count": matches_count,
    }), 200

@app.route("/metrics_prom", methods=["GET"])
def metrics_prom():
    db = get_db()
    teams_count = db.execute("SELECT COUNT(*) FROM teams").fetchone()[0]
    matches_count = db.execute("SELECT COUNT(*) FROM matches").fetchone()[0]

    lines = [
        "# HELP matchup_teams_count Number of teams registered in Matchup.",
        "# TYPE matchup_teams_count gauge",
        f"matchup_teams_count {teams_count}",
        "# HELP matchup_matches_count Number of matches stored in Matchup.",
        "# TYPE matchup_matches_count gauge",
        f"matchup_matches_count {matches_count}",
    ]
    body = "\n".join(lines) + "\n"

    return Response(body, mimetype="text/plain; version=0.0.4; charset=utf-8")





@app.get("/ping")
def ping():
    return jsonify({"ok": True})


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(409)
@app.errorhandler(500)
def handle_error(err):
    code = getattr(err, "code", 500)
    msg = getattr(err, "description", str(err))
    return jsonify({"error": msg, "status": code}), code



app.register_blueprint(teams_bp)
app.register_blueprint(auth_bp)  
app.register_blueprint(matches_bp)
app.register_blueprint(leaderboard_bp) 



if __name__ == "__main__":
    from backend.db import init_db, DB_PATH
    init_db()
    print("db at:", DB_PATH)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


