from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)
DB_NAME = "user.db"

# --------------------------------------------------
# HTML PAGES IN TEMPLATES FOLDER
# --------------------------------------------------

# --------------------------------------------------
# login_v1.html login_v2.html signup_v1.html signup_v1.html
# (pages must call the correct function)
# --------------------------------------------------
def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    """
    Initialize database and tables if they do not exist.
    This makes the application robust for first run,
    Docker containers, CI/CD pipelines, etc.
    """
    db = get_db()
    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_PLAIN (
            USERNAME TEXT PRIMARY KEY,
            PASSWORD TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_HASH (
            USERNAME TEXT PRIMARY KEY,
            HASH TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()

# --------------------------------------------------
# RESET DATABASE (TEST ONLY)
# --------------------------------------------------
@app.route("/delete/all", methods=["GET" , "POST", "DELETE"])
# A browser that opens a URL manually always sends an HTTP GET request. 
# Using GET for destructive actions is not RESTful and is insecure, 
# but it is deliberately allowed here for testing purposes.

def delete_all():
    db = get_db()
    c = db.cursor()

    c.execute("DELETE FROM USER_PLAIN")
    c.execute("DELETE FROM USER_HASH")

    db.commit()
    db.close()
    return "All test records deleted\n"

# ==================================================
# V1 — PLAINTEXT PASSWORDS (INSECURE, EDUCATIONAL)
# ==================================================

@app.route("/signup/v1", methods=["GET", "POST"])
def signup_v1():
    if request.method == "GET":
        return render_template("signup_v1.html")

    db = get_db()
    c = db.cursor()

    try:
        c.execute(
            "INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
            (request.form["username"], request.form["password"])
        )
        db.commit()
        return "V1 signup successful (plaintext password)\n"

    except sqlite3.IntegrityError:
        return "Username already exists\n"

    finally:
        db.close()

def verify_plain(username, password):
    db = get_db()
    c = db.cursor()

    c.execute(
        "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?",
        (username,)
    )
    record = c.fetchone()
    db.close()

    return record is not None and record[0] == password

@app.route("/login/v1", methods=["GET", "POST"])
def login_v1():
    if request.method == "GET":
        return render_template("login_v1.html")

    if verify_plain(request.form["username"], request.form["password"]):
        return "V1 login successful (insecure)\n"

    return "Invalid username or password\n"

# ==================================================
# V2 — HASHED PASSWORDS (SECURE)
# ==================================================

@app.route("/signup/v2", methods=["GET", "POST"])
def signup_v2():
    if request.method == "GET":
        return render_template("signup_v2.html")

    db = get_db()
    c = db.cursor()

    try:
        password_hash = hashlib.sha256(
            request.form["password"].encode()
        ).hexdigest()

        c.execute(
            "INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)",
            (request.form["username"], password_hash)
        )
        db.commit()
        return "V2 signup successful (hashed password)\n"

    except sqlite3.IntegrityError:
        return "Username already exists\n"

    finally:
        db.close()

def verify_hash(username, password):
    db = get_db()
    c = db.cursor()

    c.execute(
        "SELECT HASH FROM USER_HASH WHERE USERNAME = ?",
        (username,)
    )
    record = c.fetchone()
    db.close()

    if not record:
        return False

    return record[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route("/login/v2", methods=["GET", "POST"])
def login_v2():
    if request.method == "GET":
        return render_template("login_v2.html")

    if verify_hash(request.form["username"], request.form["password"]):
        return "V2 login successful (secure)\n"

    return "Invalid username or password\n"


# --------------------------------------------------
# HOME
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    init_db()  # <-- CRUCIAL CHANGE
    app.run(host="0.0.0.0", port=5555, ssl_context="adhoc")
