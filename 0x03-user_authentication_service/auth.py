#!/usr/bin/env python3
"""auth module."""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email=email, hashed_password=hashed_password)
        return user


def _hash_password(password: str) -> bytes:
    """hases a password."""
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(byte, salt)
    return hashed_pswd
