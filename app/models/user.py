# app/models/user.py
from __future__ import annotations
from typing import Optional
from .cart import Cart

class User:
    """
    UML: User
    +userId: int
    +name: string
    +email: string
    +password: string
    ——————————————————————————
    Responsibilities:
    - Hold identity & auth data for any user (Admin/Customer).
    - No persistence/DB logic here.
    """
    def __init__(self, user_id: Optional[int], name: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._password = password    # plain compare for console demo
        self.role = role             # 'customer' | 'admin'
        self._logged_in = False

    # --- Operations ---
    def check_password(self, password: str) -> bool:
        return self._password == password

    def login(self, password: str) -> bool:
        if self.check_password(password):
            self._logged_in = True
            return True
        return False

    def logout(self) -> None:
        self._logged_in = False

    @property
    def is_logged_in(self) -> bool:
        return self._logged_in

    def __repr__(self) -> str:
        return f"<User id={self.user_id} name={self.name!r} role={self.role}>"

class Customer(User):
    """
    UML: Customer extends User
    +address: string
    +phone: string (optional, skipped in minimal)
    +browseBooks()
    +addToCart()
    +placeOrder()
    Composition: owns Cart (1:1)
    """
    def __init__(self, user_id: Optional[int], name: str, email: str, password: str, address: str = ""):
        super().__init__(user_id, name, email, password, role="customer")
        self.address = address
        self.cart: Cart = Cart(user_id=self.user_id)

    # Thin convenience wrappers around Cart (domain-level, no repositories here)
    def add_to_cart(self, book, quantity: int) -> None:
        self.cart.add_item(book, quantity)

    def remove_from_cart(self, book_id: int) -> None:
        self.cart.remove_item(book_id)

    def update_cart_quantity(self, book_id: int, new_qty: int) -> None:
        self.cart.update_quantity(book_id, new_qty)

    def clear_cart(self) -> None:
        self.cart.clear_cart()

class Admin(User):
    """
    UML: Admin extends User
    +addBook()
    +updateBook()
    +removeBook()
    +manageUsers()
    (Actual persistence is done in controllers/repositories.)
    """
    def __init__(self, user_id: Optional[int], name: str, email: str, password: str):
        super().__init__(user_id, name, email, password, role="admin")
