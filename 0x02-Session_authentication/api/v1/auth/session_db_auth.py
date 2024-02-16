#!/usr/bin/env python3
"""session database module."""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """session database class."""
    def create_session(self, user_id=None):
        """creates a session id."""
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            new_user = UserSession(user_id=user_id, session_id=session_id)
            new_user.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """retrieves user id."""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """destroys a session."""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
