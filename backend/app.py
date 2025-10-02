
print("Starting app.py") # DEBUG line to confirm this file is being run
from flask import Flask, jsonify # import Flask and jsonify
from db import get_db, close_db, init_db   # DB helpers
from teams import teams_bp
from matches import matches_bp                 

app = Flask(__name__) # create the Flask app instance 

# DB connection per request
@app.before_request  
def _open_db(): 
    get_db()

@app.teardown_appcontext # close DB connection after request
def _close_db(exception):
    close_db()

# Tests
@app.route("/")
def home():
    return "Matchup backend is running :)"

@app.get("/ping") 
def ping():
    return jsonify({"ok": True}) 

# register features
app.register_blueprint(teams_bp)  #teams CRUD

# Json errors
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(409)
@app.errorhandler(500)
def handle_error(err):
    code = getattr(err, "code", 500)
    msg = getattr(err, "description", str(err))
    return jsonify({"error": msg, "status": code}), code

app.register_blueprint(matches_bp) # register matches blueprint


if __name__ == "__main__":
    from db import init_db, DB_PATH  #initialize DB and run app if this file is run directly
    init_db()
    print ("Database initialized at:", {DB_PATH})               
    app.run(debug=True)


