import os
print("Starting app.py") # debug

from flask import Flask, jsonify
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


