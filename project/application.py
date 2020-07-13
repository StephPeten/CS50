import os
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.route("/", methods=["GET", "POST"])
def index():
    """Get Date and Show Destinations for Selected Date"""

    if request.method == "GET":
        return render_template("indexdate.html")

    else:
        tripst = request.form.get("tripst")
        tripen = request.form.get("tripen")
        people = request.form.get("people")

        db.execute("UPDATE destinations SET tripst=:tripst, tripen=:tripen, people=:people", tripst=tripst, tripen=tripen, people=people)

        return redirect("/destinations")


@app.route("/destinations")
def destinations():
    """Display all the destinations with their prices updated depending on the dates"""

    rows = db.execute("SELECT * FROM destinations")

    for row in rows:
        hotelkey = row["hotelcode"]
        chkin = row["tripst"]
        chkout = row["tripen"]
        people = row["people"]
        response = requests.get("https://data.xotelo.com/api/rates?hotel_key="+str(hotelkey)+"&chk_in="+chkin+"&chk_out="+chkout+"&adults="+str(people)+"&currency=EUR")
        response_json = response.json()
        rate = response_json["result"]["rates"][0]['rate']
        tax = response_json["result"]["rates"][0]['tax']
        hotelprice = rate + tax
        total = round((hotelprice*((100+row["hotelcom"])/100))+(row["people"]*(row["activityprice"]*((100+row["activitycom"])/100))))
        db.execute("UPDATE destinations SET hotelprice=:hotelprice, total=:total WHERE destinations=:destinations", hotelprice=hotelprice, total=total, destinations=row["destinations"])

    return render_template("homepage.html", chkin=chkin, chkout=chkout, people=people, rows=rows)


@app.route("/newdest", methods=["GET", "POST"])
@login_required
def newdest():
    """Add new destination"""

    if request.method == "GET":
        return render_template("newdest.html")

    else:
        city = request.form.get("city")
        hotelcode = request.form.get("hotelcode")
        activities = request.form.get("activities")
        imagurl = request.form.get("img")

        if not city:
            return apology("You must input a city")
        if not hotelcode:
            return apology("You must input an hotelcode")
        if not activities:
            return apology("You must input a price for the activities")
        if not imagurl:
            return apology("You must insert the URL of a picture, Google image is your friend !")

        db.execute("INSERT INTO destinations(destinations, activityprice, hotelcode, imagurl) VALUES (:destinations, :activityprice, :hotelcode, :imagurl)", destinations=city, activityprice=activities, hotelcode=hotelcode, imagurl=imagurl)

        flash("Destination Added with Success ! Go modify the dates before opening the destinations page !")
        return redirect("/")


@app.route("/rates", methods=["GET", "POST"])
@login_required
def rates():
    """Modify the commission on destinations"""

    if request.method == "GET":

        rows = db.execute("SELECT destinations, hotelcom, activitycom FROM destinations")
        dest={}

        for row in rows:
            dest[row["destinations"]] = row["hotelcom"], row["activitycom"]


        return render_template("rates.html", dest=dest)

    else:
        destinations = request.form.get("rates")
        hocom = request.form.get("hotelcom")
        accom = request.form.get("activitycom")

        if not hocom:
            return apology("You must provide an Hotel Commission")
        if not accom:
            return apology("You must provide an Activities Commission")

        db.execute("UPDATE destinations SET hotelcom=:hotelcom, activitycom=:activitycom WHERE destinations=:destinations", hotelcom=hocom, activitycom=accom, destinations=destinations)

        flash("Modified with success !")
        return redirect("/")


@app.route("/suggestion", methods=["GET", "POST"])
def suggestion():
    """Let the user give suggestion for places he would like to visit !"""

    if request.method == "GET":
        return render_template("suggestion.html")

    else:
        suggestion = request.form.get("suggestion")
        if len(suggestion) < 3:
            return apology("You must provide a 3 letters destination at least !")

        already = db.execute("SELECT demand FROM suggestions WHERE destination = :destination", destination=suggestion)

        if not already:
            db.execute("INSERT INTO suggestions(destination, demand) VALUES (:destination, :demand)", destination=suggestion, demand=1)

        else:
            dem = already[0]['demand']
            demands = dem + 1
            db.execute("UPDATE suggestions SET demand = :demand WHERE destination = :destination", destination=suggestion, demand=demands)

        flash("Thanks ! We added your suggestion to the list ! Stay tuned !")
        return redirect("/")


@app.route("/suggestions")
@login_required
def suggestions():
    """Display which destinations are the most desired by the customers"""

    suggestions = db.execute("SELECT * FROM suggestions ORDER BY demand DESC")

    return render_template("suggestions.html", suggestions=suggestions)


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
        rows = db.execute("SELECT * FROM boss WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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

    if request.method == "GET":
        return render_template("register.html")

    else:
        name = request.form.get("username")
        if not name:
            return apology("You must provide an Username.")
        elif db.execute("SELECT * FROM boss WHERE username=:username", username=name):
            return apology("Sorry, username already taken.")

        password1 = request.form.get("password")
        if not password1:
            return apology("You must provide a password.")
        elif len(password1) < 4:
            return apology("Your password must be composed of at least 4 characters")
        elif request.form.get("password")!=request.form.get("confirmation"):
            return apology("Your entered 2 different passwords.")

        password = generate_password_hash(password1)

        db.execute("INSERT INTO boss (username, hash) VALUES (:name, :password)", name=name, password=password)

    flash("Registered succesfully ! You can now Log In !")
    return redirect("/")

@app.route("/reclame")
def reclame():
    """Display my "reclame"""

    return render_template("reclame.html")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)