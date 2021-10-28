from flask import Flask
from flask import request
from flask import render_template
import sqlite3
import hashlib

microweb_app = Flask(__name__)

db_name = 'login.db'

#### RE-INTIALIZING DATABASE => deleting all records from test database
@microweb_app.route('/delete/all', methods=['POST', 'DELETE'])
def delete_all():
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    sql_statement = "DELETE FROM USER_PLAIN ; "
    c.execute(sql_statement)
    sql_statement = "DELETE FROM USER_HASH ; "
    c.execute(sql_statement)
    db_conn.commit()
    db_conn.close()
    return "Test records deleted\n"

#### CLEAR TEXT PASSWORDS, INSECURE => signup, verify, login
@microweb_app.route('/signup/v1', methods=['POST'])
def signup_v1():
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    sql_statement = "CREATE TABLE IF NOT EXISTS USER_PLAIN (USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL); "
    c.execute(sql_statement)
    db_conn.commit()
    try:
        sql_statement = "INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES ('{0}' , '{1}')".format(request.form['username'] , request.form['password'])
        c.execute(sql_statement)
        db_conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered, but is insecure\n"
    return "Signup success, but insecure\n"

def verify_plain(username, password):
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    sql_query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = '{0}'".format(username)
    c.execute(sql_query)
    records = c.fetchone()
    db_conn.close()
    if not records:
        return False
    return records[0] == password

@microweb_app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    error = None
    if request.method == 'POST':
        if verify_plain(request.form['username'], request.form['password']):
            error = 'Login success, but insecure\n'
        else:
            error = 'Invalid username/password\n'
    else:   
        error = 'Invalid Method\n'
    return error

#### PASSWORD HASHING => signup, verify, login
@microweb_app.route('/signup/v2', methods=['POST'])
def signup_v2():
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    sql_statement = "CREATE TABLE IF NOT EXISTS USER_HASH (USERNAME TEXT PRIMARY KEY NOT NULL, HASH TEXT NOT NULL); "
    c.execute(sql_statement)
    db_conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        sql_statement = "INSERT INTO USER_HASH VALUES ('{0}' , '{1}' ) ".format(request.form['username'], hash_value)
        c.execute(sql_statement)
        db_conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered\n"
    print('username: ' , request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Secure signup succeeded\n"

def verify_hash(username, password):
    db_conn = sqlite3.connect(db_name)
    c = db_conn.cursor()
    sql_query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(sql_query)
    records = c.fetchone()
    db_conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@microweb_app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'Login sucess, using hash\n'
        else:
            error = 'Invalid username/password\n' 
    else:
        error = 'Invalid method\n'
    return error

#### HOME
@microweb_app.route('/')
def main():
    return render_template("index.html")

#### MAIN
if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5555, ssl_context='adhoc')
