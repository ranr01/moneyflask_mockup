from flask import Flask, render_template, request, redirect, url_for

from auth_bp import auth_bp_factory, login_required, role_required

from data import users, accounts, transactions


def get_user_from_user_id(id):
    user = [u for u in users if u["id"] == id]
    if len(user) > 0:
        return user[0]
    return None


def get_user_from_username(username):
    user = [u for u in users if u["username"] == username]
    if len(user) > 0:
        return user[0]
    return None


class State:
    pass


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")

app.register_blueprint(
    auth_bp_factory(
        get_user_from_username, get_user_from_user_id, "index", "auth.login"
    )
)


@app.route("/")
@login_required
def index():
    return render_template("index.html", accounts=accounts)


@app.route("/<int:account_id>/new-transaction", methods=["GET"])
@login_required
@role_required("admin")
def new_transaction(account_id):
    state = State()
    state.name_is_active = False

    return render_template(
        "new_transaction.html",
        account=accounts[account_id - 1],
        state=state,
    )


@app.route("/<int:account_id>/new-transaction", methods=["POST"])
@login_required
@role_required("admin")
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
@login_required
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
@login_required
@role_required("admin")
def settings(account_id):
    state = State()
    state.name_is_active = False

    return render_template(
        "account_settings.html",
        account=accounts[account_id - 1],
        state=state,
    )


@app.route("/<int:account_id>/settings", methods=["POST"])
@login_required
@role_required("admin")
def post_settings(account_id):
    return redirect(url_for("index"))
