#!/usr/bin/env python3
"""session view."""

import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_login():
    """auth session login."""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    user_dict = jsonify(users[0].to_json())
    user_dict.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return user_dict


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_logout():
    """auth session logout."""
    from api.v1.app import auth
    val = auth.destroy_session(request)
    if val is False:
        abort(404)
    return jsonify({}), 200
