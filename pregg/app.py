import sqlite3
import os

from flask import Flask, jsonify, render_template, request, session, flash, redirect
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

from config import Config

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.from_object(Config)


# DATABASE

# Connect database (create a Connection object that represents the database)
con = sqlite3.connect('app.db')

# Create datatables
# https://docs.python.org/3/library/sqlite3.html
con.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, hash TEXT, PRIMARY KEY(id))''')

# Initialize cursor 
# cur = con.cursor()

# Save (commit) the changes
con.commit()


@app.route("/", methods=["GET", 'POST'])
def home():
    """
    Home page route
    """
    if request.method == 'POST':
        message = request.form['message']
        return jsonify(your_message=message)
    return render_template("index.html")

@app.route("/hello", methods=["GET"])
def hello():
    """
    Hello route
    """
    return 'hello'

@app.route('/message', methods=['POST'])
def message():
    """
    Message route
    """
    message = request.json.get("message")
    return jsonify(your_message=message)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return
            # return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return
            # return apology("must provide password", 403)

        # Query database for username
        rows = con.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return
            # return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST": 

        # Ensure user submitted a username (If field is left blank, render apology)
        if not request.form.get("username"):
            return
            # return apology("must provide username", 400)

        # Ensure user submitted both password and confirmation (Render an apology if password or confirmation left blank) 
        if not request.form.get("password") or not request.form.get("confirmation"):
            return
            # return apology("must provide both password and confirmation", 400)

        # Query database for username
        rows = con.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure user submitted a username that does not already exist
        if len(rows) == 1:
            return
            # return apology("must provide username that doesn't already exist", 400)

        # Render an apology if passwords do not match
        if request.form.get("password") != request.form.get("confirmation"):
            return
            # return apology("password and confirmation must match", 400)

        # Get data (username and password) that user inputted into registration form 
        username = request.form.get("username")
        passwordhash = generate_password_hash(request.form.get("password"))

        # Insert user input into database
        con.execute("INSERT into users (username, hash) VALUES (?, ?)", username, passwordhash)

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET 
    else:
        return render_template("register.html")

@app.route("/journal")
@login_required
def journal():
    """Journal page for users"""
    return render_template("journal.html")

@app.route("/quiz")
@login_required
def quiz():
    """Quiz"""
    return render_template("quiz.html")

@app.route("/ppd")
@login_required
def ppd():
    """Info on postpartum depression"""
    return render_template("ppd.html")

@app.route("/tracking")
@login_required
def tracking():
    """Allow users to track their pregnancy (prenatal development of the baby)"""
    return render_template("tracking.html")

@app.route("/about")
@login_required
def about():
    """About us"""
    return render_template("about.html")