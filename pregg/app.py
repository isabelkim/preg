import sqlite3
import os
import datetime
from datetime import date

from cs50 import SQL
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
# con = sqlite3.connect('app.db')

# Database using CS50
db = SQL("sqlite:///app.db")

# Create datatables
# https://docs.python.org/3/library/sqlite3.html
# con.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, hash TEXT, PRIMARY KEY(id))''')
# db.execute("DROP TABLE date")
# db.execute("DROP TABLE date")
# db.execute("DROP TABLE users")
db.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, hash TEXT, PRIMARY KEY(id))''')
db.execute('''CREATE TABLE IF NOT EXISTS date (id INTEGER, user_id INTEGER, month INT, day INT, year INT, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id))''')

# Initialize cursor 
# cur = con.cursor()

# Save (commit) the changes
# con.commit()


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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        # rows = con.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Check that user hasn't logged in before then initialize conception date
        rows2 = db.execute("SELECT * FROM date WHERE user_id = ?", session["user_id"])
        if len(rows2) == 0:
            db.execute("INSERT INTO date (user_id, month, day, year) VALUES (?, ?, ?, ?)", session["user_id"], 0, 0, 0)

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
            return apology("must provide username", 400)

        # Ensure user submitted both password and confirmation (Render an apology if password or confirmation left blank) 
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide both password and confirmation", 400)

        # Query database for username
        # rows = con.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure user submitted a username that does not already exist
        if len(rows) == 1:
            return apology("must provide username that doesn't already exist", 400)
            # return apology("must provide username that doesn't already exist", 400)

        # Render an apology if passwords do not match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)

        # Get data (username and password) that user inputted into registration form 
        username = request.form.get("username")
        passwordhash = generate_password_hash(request.form.get("password"))

        # Insert user input into database
        # con.execute("INSERT into users (username, hash) VALUES (?, ?)", username, passwordhash)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passwordhash)

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET 
    else:
        return render_template("register.html")

@app.route("/submitentry", methods=["GET", "POST"])
@login_required
def submitentry():
    """Submit a journal entry"""
    if request.method == "POST":
        # db.execute('''DROP TABLE journal''')
        db.execute('''CREATE TABLE IF NOT EXISTS journal (id INTEGER, user_id INTEGER, title TEXT, mood TEXT, entry TEXT, timestamp DATETIME default(CURRENT_TIMESTAMP), PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id))''')

        # Make sure entry is not blank
        if not request.form.get("entry"):
            return apology("entry cannot be blank", 400)
        
        title = request.form.get("title")
        entry = request.form.get("entry")
        mood = request.form.get("mood")
        
        # Insert user input into database
        db.execute("INSERT INTO journal (user_id, title, entry, mood) VALUES (?, ?, ?, ?)", session["user_id"], title, entry, mood)

        # Redirect user to home page
        return redirect("/journal")
    
    # User reached route via GET 
    else:
        return render_template("submitentry.html")

@app.route("/journal")
@login_required
def journal():
    """Show journal entries"""
    # Select all of the entries of a user
    entries = db.execute("SELECT * FROM journal WHERE user_id = ?", session["user_id"])

    return render_template("journal.html", entries=entries)

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

@app.route("/conception", methods=["GET", "POST"])
@login_required
def conception():
    """Conception date"""
    if request.method == "POST":
        # Make sure month and day are not blank
        if not request.form.get("month"):
            return apology("entry cannot be blank", 400)
        if not request.form.get("day"):
            return apology("entry cannot be blank", 400)
        if not request.form.get("year"):
            return apology("entry cannot be blank", 400)
        
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        year = int(request.form.get("year"))
        
        # Insert user input into database
        db.execute("UPDATE date SET month = ?, day = ?, year = ? WHERE user_id = ?", month, day, year, session["user_id"])

        # Redirect user to home page
        return redirect("/tracking")
    
    # User reached route via GET 
    else:
        return render_template("conception.html")

@app.route("/tracking")
@login_required
def tracking():
    """Allow users to track their pregnancy (prenatal development of the baby)"""
    dt = datetime.datetime.today()
    today_month = dt.month
    today_day = dt.day
    today_year = dt.year
    month = db.execute("SELECT month FROM date WHERE user_id = ?", session["user_id"])[0]["month"]
    day = db.execute("SELECT day FROM date WHERE user_id = ?", session["user_id"])[0]["day"]
    year = db.execute("SELECT year FROM date WHERE user_id = ?", session["user_id"])[0]["year"]
    today = date(today_year, today_month, today_day)
    conception = date(year, month, day)
    difference = today - conception
    weeks = difference.days / 7
    return render_template("tracking.html", weeks=weeks)

@app.route("/about")
@login_required
def about():
    """About us"""
    return render_template("about.html")