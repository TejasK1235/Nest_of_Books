# app/models/cart.py
from __future__ import annotations
from typing import List, Optional
from .book import Book
from .cart_item import CartItem

class Cart:
    """
    UML: Cart
    +cartId: (not persisted at model level; identified by userId)
    +totalAmount: double (derived)
    +calculateTotal()
    +clearCart()
    Composition: has many CartItem (1..*)
    """
    def __init__(self, user_id: Optional[int]):
        self.user_id = user_id
        self.items: List[CartItem] = []

    # --- Operations matching use cases ---
    def add_item(self, book: Book, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")

        # If book already in cart → update quantity
        for ci in self.items:
            if ci.book.book_id == book.book_id:
                ci.update_quantity(ci.quantity + qty)
                return
        self.items.append(CartItem(book, qty))

    def remove_item(self, book_id: int) -> None:
        self.items = [ci for ci in self.items if ci.book.book_id != book_id]

    def update_quantity(self, book_id: int, new_qty: int) -> None:
        found = False
        for ci in self.items:
            if ci.book.book_id == book_id:
                ci.update_quantity(new_qty)
                found = True
                break
        if not found:
            raise ValueError("book not present in cart")

    def calculate_total(self) -> float:
        # OCL-like invariant: total == sum(item.subtotal)
        return round(sum(ci.subtotal for ci in self.items), 2)

    def clear_cart(self) -> None:
        self.items.clear()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def __repr__(self) -> str:
        return f"<Cart user_id={self.user_id} items={len(self.items)} total={self.calculate_total():.2f}>"
