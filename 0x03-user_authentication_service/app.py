#!/usr/bin/env python3
"""flask app module."""

from flask import Flask, jsonify, request, abort
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


@app.route('/sessions', methods=['POST'])
def sessionify():
    """sessionify."""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        result = jsonify({"email": email, "message": "logged in"})
        result.set_cookie('session_id', session_id)
        return result
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
