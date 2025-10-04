
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import query_one, execute, query_all
import secrets

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _new_token() -> str:
    return secrets.token_hex(24)  # this gives us 48 hexidecimal chars

def _create_session(user_id: int) -> str:
    token = _new_token()
    execute("INSERT INTO sessions(id, user_id) VALUES(?, ?)", (token, user_id))
    return token

def current_user_from_header():
    """Read Authorization: Bearer <token> and return user row or None."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1].strip()
    row = query_one(
        """
        SELECT u.id, u.email
        FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.id = ?
        """,
        (token,),
    )
    return row


@auth_bp.post("/signup")
def signup():
    """
    Body: { "email": "...", "password": "..." }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if query_one("SELECT id FROM users WHERE email = ?", (email,)):
        return jsonify({"error": "email already registered"}), 409

    pw_hash = generate_password_hash(password)
    user_id = execute("INSERT INTO users(email, password_hash) VALUES(?, ?)", (email, pw_hash))

    token = _create_session(user_id)
    return jsonify({"user_id": user_id, "email": email, "token": token}), 201

@auth_bp.post("/login")
def login():
    """
    Body: { "email": "...", "password": "..." }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = query_one("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "invalid credentials"}), 401

    token = _create_session(user["id"])
    return jsonify({"user_id": user["id"], "email": user["email"], "token": token}), 200

@auth_bp.get("/me")
def me():
    """Return current user using Authorization: Bearer <token> header."""
    user = current_user_from_header()
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"user_id": user["id"], "email": user["email"]}), 200

@auth_bp.post("/logout")
def logout():
    """Invalidate the current token."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"ok": True}) 
    token = auth.split(" ", 1)[1].strip()
    # delete the session if present
    execute("DELETE FROM sessions WHERE id = ?", (token,))
    return jsonify({"ok": True}), 200
