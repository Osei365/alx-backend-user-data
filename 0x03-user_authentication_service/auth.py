#!/usr/bin/env python3
"""auth module."""

import bcrypt
import uuid
from typing import Union
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

    def valid_login(self, email: str, password: str) -> bool:
        """validates login."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except Exception:
            return False
        return False

    def create_session(self, email: str) -> str:
        """creates a session."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """gets user based on session."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroys a session."""
        self._db.update_user(user_id, session_id=None)


def _hash_password(password: str) -> bytes:
    """hases a password."""
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(byte, salt)
    return hashed_pswd


def _generate_uuid() -> str:
    """returns a uuid."""
    return str(uuid.uuid4())
