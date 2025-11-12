# app/controllers/cart_controller.py
from app.repositories.book_repository import BookRepository
from app.models.cart import Cart

class CartController:
    """
    Handles Cart operations for logged-in users.
    Maps to: AddToCart, RemoveFromCart, UpdateQuantity, ViewCart.
    """

    def __init__(self):
        self.book_repo = BookRepository()
        self.cart_sessions: dict[int, Cart] = {}  # user_id → Cart

    def _get_cart(self, user_id: int) -> Cart:
        """
        Get an existing cart for a user or load one from the DB if present.
        """
        if user_id not in self.cart_sessions:
            try:
                saved_cart = self.book_repo.load_cart(user_id)
                if saved_cart and not saved_cart.is_empty():
                    self.cart_sessions[user_id] = saved_cart
                else:
                    self.cart_sessions[user_id] = Cart(user_id)
            except Exception:
                # fallback to empty cart if DB read fails
                self.cart_sessions[user_id] = Cart(user_id)
        return self.cart_sessions[user_id]

    def add_to_cart(self, user_id: int, book_id: int, qty: int) -> str:
        try:
            if qty is None or qty <= 0:
                return "❌ Quantity must be a positive integer."
            book = self.book_repo.get_book_by_id(book_id)
            if not book:
                return "❌ Book not found."
            if book.stock < qty:
                return "❌ Not enough stock available."
            cart = self._get_cart(user_id)
            cart.add_item(book, qty)
            self.book_repo.save_cart(user_id, cart)
            return f"✅ Added {qty} × '{book.title}' to cart."
        except Exception as e:
            return f"❌ Failed to add to cart: {e}"

    def remove_from_cart(self, user_id: int, book_id: int) -> str:
        try:
            cart = self._get_cart(user_id)
            cart.remove_item(book_id)
            self.book_repo.save_cart(user_id, cart)
            return f"🗑️ Removed book ID {book_id} from cart."
        except Exception as e:
            return f"❌ Failed to remove item: {e}"

    def update_cart(self, user_id: int, book_id: int, new_qty: int) -> str:
        try:
            if new_qty is None or new_qty <= 0:
                return "❌ Quantity must be a positive integer."
            cart = self._get_cart(user_id)
            cart.update_quantity(book_id, new_qty)
            self.book_repo.save_cart(user_id, cart)
            return f"🔁 Updated book ID {book_id} to quantity {new_qty}."
        except Exception as e:
            return f"❌ Failed to update cart: {e}"

    def view_cart(self, user_id: int) -> str:
        try:
            cart = self._get_cart(user_id)
            if cart.is_empty():
                return "🛒 Your cart is empty."
            lines = ["\n🛒 Cart contents:"]
            for item in cart.items:
                lines.append(
                    f"  [ID:{item.book.book_id}] {item.book.title} — Qty: {item.quantity} — ₹{item.subtotal}"
                )
            lines.append(f"Total: ₹{cart.calculate_total()}")
            return "\n".join(lines)
        except Exception as e:
            return f"❌ Could not load cart: {e}"

    def clear_cart(self, user_id: int) -> str:
        try:
            cart = self._get_cart(user_id)
            cart.clear_cart()
            self.book_repo.save_cart(user_id, cart)
            return "🧹 Cart cleared."
        except Exception as e:
            return f"❌ Failed to clear cart: {e}"
