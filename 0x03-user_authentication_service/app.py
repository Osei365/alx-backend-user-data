#!/usr/bin/env python3
"""flask app module."""

from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def payload():
    """returns payload."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    result = None
    try:
        AUTH.register_user(email, password)
        result = jsonify({"email": "{}".format(email),
                          "message": "user created"})
    except Exception:
        result = jsonify({"message": "email already registered"}), 400
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
