# Add to this file for the Microweb app lab
from flask import Flask
from flask import request
from flask import render_template

microweb_app = Flask(__name__)

@microweb_app.route("/")
def main():
    return render_template("index.html")

if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5050)
