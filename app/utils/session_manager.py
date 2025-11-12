# app/utils/session_manager.py
from app.models.user import User

class SessionManager:
    """
    Simple session tracker for currently logged-in user.
    Used by ConsoleUI to maintain login state.
    """

    def __init__(self):
        self._current_user: User | None = None

    def set_user(self, user: User):
        self._current_user = user

    def get_user(self) -> User | None:
        return self._current_user

    def clear_session(self):
        self._current_user = None
