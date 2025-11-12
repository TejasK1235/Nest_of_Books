# app/models/book.py
from __future__ import annotations
from typing import Optional

class Book:
    """
    UML: Book
    +bookId: int
    +title: string
    +author: string
    +price: double
    +stock: int
    +displayDetails()
    +updateStock()
    """
    def __init__(self, book_id: Optional[int], title: str, author: str, price: float, stock: int):
        # OCL-like invariant: price >= 0 and stock >= 0
        assert price >= 0, "price must be non-negative"
        assert stock >= 0, "stock must be non-negative"

        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = float(price)
        self.stock = int(stock)

    def update_stock(self, new_stock: int) -> None:
        if new_stock < 0:
            raise ValueError("new_stock cannot be negative")
        self.stock = int(new_stock)

    def decrement_stock(self, qty: int) -> None:
        if qty < 0:
            raise ValueError("qty cannot be negative")
        if qty > self.stock:
            raise ValueError("insufficient stock")
        self.stock -= qty

    def display_details(self) -> str:
        return f"[{self.book_id}] {self.title} by {self.author} — ₹{self.price:.2f} (stock: {self.stock})"

    def __repr__(self) -> str:
        return f"<Book id={self.book_id} title={self.title!r} price={self.price} stock={self.stock}>"
