from flask import Flask, render_template, request
import sqlite3
# Check SQL injection vurnerability

app = Flask(__name__)

# Database needs to exist prior to running this script
db_name = "user.db"

@app.route('/signup/v1', methods=['GET', 'POST'])
def signup_v1():
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        try:
            username_entered = request.form.get('username')
            password_entered = request.form.get('password')
            if not username_entered or not password_entered:
                return "Missing username or password", 400
            c.execute(
                "INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
                 (username_entered, password_entered)
                )
            db_conn.commit()
        return "Signup success\n"
        
    except sqlite3.IntegrityError:
        return "Username already exists\n"

    finally:
        db_conn.close()

app.run()
