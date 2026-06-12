from flask import Flask, request, redirect, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# In-memory database
accounts = {}


# ---------------- HTML TEMPLATES ----------------
home_page = """
<h1>🏦 ATM SYSTEM</h1>

{% if not session.get('user') %}
    <a href="/login">Login</a> | <a href="/create">Create Account</a>
{% else %}
    <p>Welcome {{session['user']}}</p>
    <a href="/dashboard">Go to Dashboard</a><br><br>
    <a href="/logout">Logout</a>
{% endif %}
"""

login_page = """
<h2>Login</h2>
<form method="POST">
    Account: <input name="acc"><br>
    PIN: <input name="pin" type="password"><br>
    <button type="submit">Login</button>
</form>
<p style="color:red">{{error}}</p>
<a href="/">Home</a>
"""

create_page = """
<h2>Create Account</h2>
<form method="POST">
    Account: <input name="acc"><br>
    PIN: <input name="pin" type="password"><br>
    Initial Balance: <input name="bal" type="number"><br>
    <button type="submit">Create</button>
</form>
<p style="color:green">{{msg}}</p>
<a href="/">Home</a>
"""

dashboard_page = """
<h2>Dashboard - {{acc}}</h2>

<p>Balance: ₹{{balance}}</p>

<h3>Deposit</h3>
<form method="POST" action="/deposit">
    <input name="amount" type="number">
    <button>Deposit</button>
</form>

<h3>Withdraw</h3>
<form method="POST" action="/withdraw">
    <input name="amount" type="number">
    <button>Withdraw</button>
</form>

<h3>Transactions</h3>
<ul>
{% for t in transactions %}
    <li>{{t}}</li>
{% endfor %}
</ul>

<br>
<a href="/logout">Logout</a>
"""


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template_string(home_page)


@app.route("/create", methods=["GET", "POST"])
def create():
    msg = ""
    if request.method == "POST":
        acc = request.form["acc"]
        pin = request.form["pin"]
        bal = float(request.form["bal"])

        if acc in accounts:
            msg = "Account already exists!"
        else:
            accounts[acc] = {
                "pin": generate_password_hash(pin),
                "balance": bal,
                "transactions": []
            }
            msg = "Account created successfully!"

    return render_template_string(create_page, msg=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        acc = request.form["acc"]
        pin = request.form["pin"]

        if acc in accounts and check_password_hash(accounts[acc]["pin"], pin):
            session["user"] = acc
            return redirect("/dashboard")
        else:
            error = "Invalid credentials"

    return render_template_string(login_page, error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    acc = session["user"]
    data = accounts[acc]

    return render_template_string(
        dashboard_page,
        acc=acc,
        balance=data["balance"],
        transactions=reversed(data["transactions"])
    )


@app.route("/deposit", methods=["POST"])
def deposit():
    acc = session["user"]
    amount = float(request.form["amount"])

    accounts[acc]["balance"] += amount
    accounts[acc]["transactions"].append(f"Deposited ₹{amount}")

    return redirect("/dashboard")


@app.route("/withdraw", methods=["POST"])
def withdraw():
    acc = session["user"]
    amount = float(request.form["amount"])

    if amount > accounts[acc]["balance"]:
        accounts[acc]["transactions"].append("Failed withdrawal (Insufficient balance)")
    else:
        accounts[acc]["balance"] -= amount
        accounts[acc]["transactions"].append(f"Withdrawn ₹{amount}")

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run()
