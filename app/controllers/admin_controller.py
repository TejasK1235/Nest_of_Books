# app/controllers/admin_controller.py
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository

class AdminController:
    """
    Handles Admin operations.
    Maps to: ManageBooks, ModifyInventory, ViewUsers.
    """

    def __init__(self):
        self.book_repo = BookRepository()
        self.user_repo = UserRepository()

    def add_book(self, title: str, author: str, price: float, stock: int) -> str:
        try:
            title = (title or "").strip()
            author = (author or "").strip()
            if not title or not author:
                return "Title and Author are required."
            if price is None or price < 0:
                return "Price must be ≥ 0."
            if stock is None or stock < 0:
                return "Stock must be ≥ 0."
            book_id = self.book_repo.add_book(title, author, float(price), int(stock))
            return f"Added '{title}' (ID: {book_id}) successfully."
        except Exception as e:
            return f"Failed to add book: {e}"

    def update_book_stock(self, book_id: int, new_stock: int) -> str:
        try:
            if not isinstance(book_id, int) or book_id <= 0:
                return "Invalid Book ID."
            if new_stock is None or new_stock < 0:
                return "Stock must be ≥ 0."
            book = self.book_repo.get_book_by_id(book_id)
            if not book:
                return f"Book ID {book_id} not found."
            self.book_repo.update_book(book_id, int(new_stock))
            return f"Stock for '{book.title}' updated to {new_stock}."
        except Exception as e:
            return f"Failed to update stock: {e}"

    def remove_book(self, book_id: int) -> str:
        try:
            if not isinstance(book_id, int) or book_id <= 0:
                return "Invalid Book ID."
            book = self.book_repo.get_book_by_id(book_id)
            if not book:
                return f"Book ID {book_id} not found."
            self.book_repo.delete_book(book_id)
            return f"Removed '{book.title}' from catalog."
        except Exception as e:
            return f"Failed to remove book: {e}"

    def view_all_books(self) -> str:
        try:
            books = self.book_repo.get_all_books()
            if not books:
                return "No books in inventory."
            lines = ["\nBook Inventory:"]
            for b in books:
                lines.append(f"[{b.book_id}] {b.title} — ₹{b.price} — Stock: {b.stock}")
            return "\n".join(lines)
        except Exception as e:
            return f"Failed to fetch books: {e}"

    def view_all_users(self) -> str:
        try:
            users = self.user_repo.get_all_users()
            if not users:
                return "No users found."
            lines = ["\nRegistered Users:"]
            for u in users:
                lines.append(f"{u['user_id']} — {u['name']} ({u['role']}) — {u['email']}")
            return "\n".join(lines)
        except Exception as e:
            return f"Failed to fetch users: {e}"
