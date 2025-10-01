

import os, sqlite3
from flask import g
from dotenv import load_dotenv # load environment variables

load_dotenv()
# Always use absolute path for DB file, based on this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DATABASE", os.path.join(BASE_DIR, "matchup.db"))

def get_db(): # get DB connection, create if needed
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        g.db = conn
    return g.db 

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    print(f"[init_db] Using DB_PATH: {DB_PATH}")
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    print(f"[init_db] Using schema: {schema_path}")
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()
            print(f"[init_db] First 200 chars of schema.sql:\n{sql[:200]}")
        with sqlite3.connect(DB_PATH) as conn:
            conn.executescript(sql)
            print("[init_db] Schema executed.")
    except Exception as e:
        print(f"[init_db] ERROR: {e}")

def query_one(sql, params=()):
    cur = get_db().execute(sql, params)
    row = cur.fetchone(); cur.close()
    return row

def query_all(sql, params=()):
    cur = get_db().execute(sql, params)
    rows = cur.fetchall(); cur.close()
    return rows

def execute(sql, params=()):
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    last = cur.lastrowid
    cur.close()
    return last
