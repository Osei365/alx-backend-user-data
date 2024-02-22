#!/usr/bin/env python3
"""auth module."""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hases a password."""
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(byte, salt)
    return hashed_pswd
