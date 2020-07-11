import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute("SELECT * FROM ind WHERE user_id=:user", user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"]

    stocks = []
    total = cash

    for row in rows:
        stodata = lookup(row["stock"])
        value = round(row["shares"] * stodata["price"], 2)
        total += value

        stocks.append(list((stodata["symbol"], stodata["name"], row["shares"], stodata["price"], value)))

    return render_template("index.html", stocks=stocks, cash=round(cash, 2), total = round(total, 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:
        stock = lookup(request.form.get("symbol"))["symbol"]
        shares = int(request.form.get("shares"))

        if not lookup(stock):
            return apology("Invalid Symbol Bro.")

        price = lookup(stock)["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"]
        remaincash = cash - price * float(shares)
        if remaincash < 0:
            return apology("You don't have enough money Bro.")

        already = db.execute("SELECT shares FROM ind WHERE user_id = :id AND stock = :stock", id=session["user_id"], stock=stock)

        if not already:
            db.execute("INSERT INTO ind(user_id, stock, shares) VALUES (:id, :stock, :shares)", id=session["user_id"], stock=stock, shares=shares)

        else:
            shares += already[0]['shares']
            db.execute("UPDATE ind SET shares = :shares WHERE user_id = :id AND stock = :stock", id=session["user_id"], stock=stock, shares=shares)

        db.execute("INSERT INTO history(user_id, stock, shares, price, transactions) VALUES (:id, :stock, :shares, :price, :transactions)", id=session["user_id"], stock=stock, shares=shares, price=round(price*float(shares), 2), transactions="+ BOUGHT +")

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=remaincash, id=session["user_id"])

        flash("Bought ! Welcome to the Road to the Billion Bro!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM history WHERE user_id=:id", id=session["user_id"])

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Invalid Stock Bro.")

        return render_template("quoted.html", stock=stock)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        name = request.form.get("username")
        if not name:
            return apology("You must provide an Username Bro.")
        elif db.execute("SELECT * FROM users WHERE username=:username", username=name):
            return apology("Sorry, username already taken Bro.")

        password = generate_password_hash(request.form.get("password"))
        if not password:
            return apology("You must provide a password Bro.")
        elif request.form.get("password")!=request.form.get("confirmation"):
            return apology("Your entered 2 different passwords Bro.")

        db.execute("INSERT INTO users (username, hash) VALUES (:name, :password)", name=name, password=password)

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":

        rows = db.execute("SELECT stock, shares FROM ind WHERE user_id=:id", id=session["user_id"])
        stock={}

        for row in rows:
            stock[row["stock"]] = row["shares"]

        return render_template("sell.html", stock=stock)

    else:
        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        price = lookup(stock)["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"]

        nbshares = db.execute("SELECT shares FROM ind WHERE user_id=:id AND stock=:stock", id=session["user_id"], stock=stock)[0]["shares"]
        newshares = nbshares - shares

        if newshares == 0:
            db.execute("DELETE FROM ind WHERE user_id=:id AND stock=:stock", id=session["user_id"], stock=stock)

        elif newshares < 0:
            return apology("Don't try to sell what you don't have Bro.")

        else:
            db.execute("UPDATE ind SET shares=:shares WHERE user_id=:id AND stock=:stock", shares=newshares, id=session["user_id"], stock=stock)

        newcash = round(cash + float(shares) * price, 2)
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=newcash, id=session["user_id"])

        db.execute("INSERT INTO history(user_id, stock, price, shares, transactions) VALUES(:id, :stock, :price, :shares, :transactions)", id=session["user_id"], stock=stock, price=price, shares=shares, transactions="- SOLD -")

        flash("Sold Bro, High Five !")
        return redirect("/")

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add more cash for free because we are gentlemans"""

    if request.method == "GET":
        return render_template("addcash.html")

    else:
        monopoly = int(request.form.get("monopoly"))
        if monopoly > 3000:
            return apology("Hold on cow-boy, it's 3000 max. Take it easy Bro.")

        db.execute("UPDATE users SET cash= cash + :cash WHERE id=:id", cash=monopoly, id=session["user_id"])
        db.execute("INSERT INTO history(user_id, stock, price, shares, transactions) VALUES(:id, :stock, :price, :shares, :transactions)", id=session["user_id"], stock="MAGIC", price=monopoly, shares="1", transactions="+ MONOPOLY +")

    flash("Well done Bro, that's how you play da game.")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)