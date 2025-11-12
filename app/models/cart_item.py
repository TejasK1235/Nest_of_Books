# app/models/cart_item.py
from __future__ import annotations
from .book import Book

class CartItem:
    """
    UML: CartItem
    +quantity: int
    +updateQuantity()
    Aggregation: references Book (1)
    """
    def __init__(self, book: Book, quantity: int):
        if quantity <= 0:
            raise ValueError("quantity must be > 0")
        self.book = book
        self.quantity = int(quantity)
        self.subtotal = self.book.price * self.quantity

    def update_quantity(self, new_qty: int) -> None:
        if new_qty <= 0:
            raise ValueError("new_qty must be > 0")
        self.quantity = int(new_qty)
        self.subtotal = self.book.price * self.quantity

    def __repr__(self) -> str:
        return f"<CartItem book_id={self.book.book_id} qty={self.quantity} subtotal={self.subtotal:.2f}>"
