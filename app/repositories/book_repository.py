from .base_repository import BaseRepository
from app.models.book import Book

class BookRepository(BaseRepository):
    """
    CRUD for Book table with error handling.
    """

    def create_table(self):
        try:
            self.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                price REAL,
                stock INTEGER
            )""")
        except Exception as e:
            print(f"Failed to create books table: {e}")

    def add_book(self, title: str, author: str, price: float, stock: int) -> int:
        try:
            self.execute(
                "INSERT INTO books (title, author, price, stock) VALUES (?, ?, ?, ?)",
                (title, author, price, stock),
            )
            return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except Exception as e:
            print(f"Failed to add book: {e}")
            return -1

    def get_book_by_id(self, book_id: int) -> Book | None:
        try:
            row = self.fetch_one("SELECT * FROM books WHERE book_id = ?", (book_id,))
            if not row:
                return None
            return Book(row["book_id"], row["title"], row["author"], row["price"], row["stock"])
        except Exception as e:
            print(f"Error fetching book {book_id}: {e}")
            return None

    def get_all_books(self):
        try:
            rows = self.fetch_all("SELECT * FROM books")
            return [Book(r["book_id"], r["title"], r["author"], r["price"], r["stock"]) for r in rows]
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []

    def update_book(self, book_id: int, new_stock: int):
        try:
            self.execute("UPDATE books SET stock = ? WHERE book_id = ?", (new_stock, book_id))
        except Exception as e:
            print(f"Failed to update stock for book {book_id}: {e}")

    def delete_book(self, book_id: int):
        try:
            self.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        except Exception as e:
            print(f"Failed to delete book {book_id}: {e}")

    # --- Cart Persistence Helpers ---
    def save_cart(self, user_id: int, cart):
        try:
            self.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
            for item in cart.items:
                self.execute(
                    "INSERT INTO cart_items (user_id, book_id, quantity) VALUES (?, ?, ?)",
                    (user_id, item.book.book_id, item.quantity),
                )
        except Exception as e:
            print(f"Failed to save cart for user {user_id}: {e}")

    def load_cart(self, user_id: int):
        try:
            rows = self.fetch_all("SELECT * FROM cart_items WHERE user_id = ?", (user_id,))
            from app.models.cart import Cart
            from app.models.book import Book
            cart = Cart(user_id)
            for r in rows:
                book = self.get_book_by_id(r["book_id"])
                if book:
                    cart.add_item(book, r["quantity"])
            return cart
        except Exception as e:
            print(f"Failed to load cart for user {user_id}: {e}")
            from app.models.cart import Cart
            return Cart(user_id)
