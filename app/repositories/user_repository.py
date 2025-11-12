from .base_repository import BaseRepository
from app.models.user import User, Customer, Admin

class UserRepository(BaseRepository):
    """
    Handles CRUD for User table with error handling.
    """

    def create_table(self):
        try:
            self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT,
                address TEXT
            )""")
        except Exception as e:
            print(f"Failed to create users table: {e}")

    def add_user(self, name: str, email: str, password: str, role: str, address: str = "") -> int:
        try:
            self.execute(
                "INSERT INTO users (name, email, password, role, address) VALUES (?, ?, ?, ?, ?)",
                (name, email, password, role, address),
            )
            return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except Exception as e:
            print(f"Failed to add user {email}: {e}")
            return -1

    def get_user_by_email(self, email: str) -> User | None:
        try:
            row = self.fetch_one("SELECT * FROM users WHERE email = ?", (email,))
            if row is None:
                return None
            if row["role"] == "admin":
                return Admin(row["user_id"], row["name"], row["email"], row["password"])
            return Customer(row["user_id"], row["name"], row["email"], row["password"], row["address"])
        except Exception as e:
            print(f"Error fetching user {email}: {e}")
            return None

    def get_all_users(self):
        try:
            return self.fetch_all("SELECT * FROM users")
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
