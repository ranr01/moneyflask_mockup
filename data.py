from werkzeug.security import generate_password_hash

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
    {"id": 1, "name": "Ofer", "owner": 1, "balance": 1115.55},
    {"id": 2, "name": "Maya", "owner": 2, "balance": -456.00},
    {"id": 3, "name": "Ofer (Savings)", "owner": 1, "balance": 18000.0},
    {"id": 4, "name": "Maya (Savings)", "owner": 2, "balance": 10000.0},
]

users = [
    {
        "id": 0,
        "username": "ranr",
        "password": generate_password_hash("250402"),
        "role": "admin",
    },
    {
        "id": 1,
        "username": "ofer",
        "password": generate_password_hash("2504"),
        "role": "user",
    },
    {
        "id": 2,
        "username": "maya",
        "password": generate_password_hash("2504"),
        "role": "user",
    },
]
