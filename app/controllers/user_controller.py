# app/controllers/user_controller.py
from app.repositories.user_repository import UserRepository
from app.models.user import Customer, Admin, User
import re

class UserController:
    """
    Handles registration, login, logout.
    Maps to: SignUp, Login, Logout, ClearSession use cases.
    """

    def __init__(self):
        self.user_repo = UserRepository()
        self.current_user: User | None = None

    def _valid_email(self, email: str) -> bool:
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))

    def register_user(self, name, email, password, role="customer", address=""):
        try:
            # basic validations
            name = (name or "").strip()
            email = (email or "").strip()
            password = (password or "").strip()
            role = (role or "customer").strip().lower()

            if not name:
                return "Name cannot be empty."
            if not self._valid_email(email):
                return "Invalid email format."
            if not password:
                return "Password cannot be empty."
            if role not in ("admin", "customer"):
                role = "customer"

            # Restrict admin creation
            if role == "admin":
                existing_admins = [u for u in self.user_repo.get_all_users() if u["role"] == "admin"]
                if len(existing_admins) >= 2:
                    return "Admin limit reached (only 2 admins allowed)."

            existing = self.user_repo.get_user_by_email(email)
            if existing:
                return f"Email {email} already registered."

            user_id = self.user_repo.add_user(name, email, password, role, address or "")
            return f"User {name} registered successfully with ID {user_id}."
        except Exception as e:
            return f"Registration failed: {e}"

    def login(self, email: str, password: str) -> str:
        try:
            email = (email or "").strip()
            password = (password or "").strip()
            if not self._valid_email(email):
                return "Invalid email format."
            user = self.user_repo.get_user_by_email(email)
            if user is None:
                return "User not found."
            if user.login(password):
                self.current_user = user
                return f"{user.name} logged in successfully as {user.role}."
            return "Incorrect password."
        except Exception as e:
            return f"Login failed: {e}"

    def logout(self) -> str:
        try:
            if not self.current_user:
                return "No user is logged in."
            name = self.current_user.name
            self.current_user.logout()
            self.current_user = None
            return f"{name} logged out."
        except Exception as e:
            return f"Logout failed: {e}"

    def get_current_user(self) -> User | None:
        return self.current_user
