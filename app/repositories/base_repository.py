import sqlite3
from typing import Any

class BaseRepository:
    """
    Implements Singleton pattern for shared DB connection.
    Adds robust error handling for all queries.
    """
    _instance = None
    _connection = None

    def __new__(cls, db_name: str = "bookstore.db"):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._connection = sqlite3.connect(db_name, check_same_thread=False)
                cls._connection.row_factory = sqlite3.Row  # fetch as dict-like
            except sqlite3.Error as e:
                print(f"Failed to connect to database '{db_name}': {e}")
                raise
        return cls._instance

    @property
    def conn(self):
        if self._connection is None:
            raise ConnectionError("Database connection not initialized.")
        return self._connection

    # --- Safe Execution Methods ---
    def execute(self, query: str, params: tuple = ()) -> Any:
        """Execute a write operation with error handling and commit."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"DB Execute Error: {e}\nQuery: {query}\nParams: {params}")
            raise

    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Fetch multiple rows safely."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"DB FetchAll Error: {e}\nQuery: {query}\nParams: {params}")
            return []

    def fetch_one(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        """Fetch a single row safely."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"DB FetchOne Error: {e}\nQuery: {query}\nParams: {params}")
            return None

    def close_connection(self):
        """Safely close the shared database connection."""
        try:
            if self._connection:
                self._connection.commit()
                self._connection.close()
                self._connection = None
                print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")
