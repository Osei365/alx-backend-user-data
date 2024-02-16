#!/usr/bin/env python3
"""User module.
"""
from models.base import Base


class UserSession(Base):
    """user session model."""

    def __init__(self, *args: list, **kwargs: dict):
        """initiliazes instance based on kwargs and args."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
