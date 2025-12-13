from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database needs to exist prior to running this script
db_name = "users.db"

@app.route('/signup/v1', methods=['GET', 'POST'])
def signup_v1():
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    if request.method == 'GET':
        return render_template("signup.html")
    try:
        c.execute(
            "INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
            (request.form['username'], request.form['password'])
        )
        db_conn.commit()
        return "Signup success\n"

    except sqlite3.IntegrityError:
        return "Username already exists\n"

    finally:
        db_conn.close()

app.run()
