from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

transactions = [
    {
        "date": "12/12/22",
        "id": 1,
        "description": "Initial balance",
        "amount": 1100.55,
    },
    {
        "date": "12/12/22",
        "id": 1,
        "description": "Allowance",
        "amount": 15,
    },
    {
        "date": "12/12/22",
        "id": 2,
        "description": "Initial balance",
        "amount": -456.00,
    },
]
accounts = [
    {"id": 1, "name": "Ofer", "balance": 1115.55},
    {"id": 2, "name": "Maya", "balance": -456.00},
    {"id": 3, "name": "Ofer (Savings)", "balance": 18000.0},
    {"id": 4, "name": "Maya (Savings)", "balance": 10000.0},
]

class State:
    pass


@app.route("/")
def index():
    return render_template("index.html", accounts=accounts)


@app.route("/<int:account_id>/new-transaction", methods=["GET"])
def new_transaction(account_id):
    state = State()
    state.name_is_active = False

    return render_template(
        "new_transaction.html",
        account=accounts[account_id - 1],
        state=state,
    )


@app.route("/<int:account_id>/new-transaction", methods=["POST"])
def post_new_transaction(account_id):
    transactions.append(
        {
            "date": "12/12/22",
            "id": account_id,
            "description": request.form["description"],
            "amount": float(request.form["amount"]),
        }
    )
    accounts[account_id - 1]["balance"] += float(request.form["amount"])
    return redirect(url_for("index"))


@app.route("/<int:account_id>/transactions", methods=["GET"])
def get_transactions(account_id):
    state = State()
    state.name_is_active = True

    return render_template(
        "transaction_table.html",
        account=accounts[account_id - 1],
        transactions=[t for t in transactions if t["id"] == account_id],
        state=state,
    )


@app.route("/<int:account_id>/settings", methods=["GET"])
def settings(account_id):
    state = State()
    state.name_is_active = False

    return render_template(
        "account_settings.html",
        account=accounts[account_id - 1],
        state=state,
    )


@app.route("/<int:account_id>/settings", methods=["POST"])
def post_settings(account_id):
    return redirect(url_for("index"))
