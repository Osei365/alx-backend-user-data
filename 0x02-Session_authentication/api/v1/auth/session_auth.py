#!/usr/bin/env python3
"""session authentication."""

import uuid
from .auth import Auth


class SessionAuth(Auth):
    """session auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session."""
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
