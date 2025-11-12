# app/cli/console_ui.py
from app.controllers.user_controller import UserController
from app.controllers.cart_controller import CartController
from app.controllers.order_controller import OrderController
from app.controllers.admin_controller import AdminController
from app.utils.session_manager import SessionManager
import getpass

class ConsoleUI:
    """
    Text-based user interface for console operation.
    Handles both Admin and Customer flows.
    """

    def __init__(self):
        self.user_ctrl = UserController()
        self.cart_ctrl = CartController()
        self.order_ctrl = OrderController()
        self.admin_ctrl = AdminController()
        self.session = SessionManager()

    # ---------- Safe input helpers ----------
    def _prompt_choice(self, prompt: str, choices: list[str]):
        """Returns a validated choice (string) from choices (case-insensitive)."""
        while True:
            try:
                val = input(prompt).strip()
                if not val:
                    print("⚠️ Please enter a value.")
                    continue
                # allow raw number choices or text
                if val.lower() in [c.lower() for c in choices]:
                    return val
                if val in choices:
                    return val
                # allow 1..n direct matches if provided as numbers
                if val.isdigit() and int(val) >= 1 and int(val) <= len(choices):
                    return val
                print(f"❌ Invalid choice. Allowed: {', '.join(choices)}")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Input interrupted.")
                return None

    def _prompt_int(self, prompt: str, min_val: int | None = None, allow_blank: bool = False):
        while True:
            try:
                val = input(prompt).strip()
                if allow_blank and val == "":
                    return None
                num = int(val)
                if min_val is not None and num < min_val:
                    print(f"⚠️ Enter a number ≥ {min_val}.")
                    continue
                return num
            except ValueError:
                print("❌ Please enter a valid integer.")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Input interrupted.")
                return None

    def _prompt_float(self, prompt: str, min_val: float | None = None, allow_blank: bool = False):
        while True:
            try:
                val = input(prompt).strip()
                if allow_blank and val == "":
                    return None
                num = float(val)
                if min_val is not None and num < min_val:
                    print(f"⚠️ Enter an amount ≥ {min_val}.")
                    continue
                return num
            except ValueError:
                print("❌ Please enter a valid number.")
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Input interrupted.")
                return None

    # ---------- Menus ----------
    def main_menu(self):
        while True:
            print("\n====== 📚 Nest of Books ======")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = self._prompt_choice("Enter choice: ", ["1", "2", "3"])
            if choice == "1":
                self.handle_registration()
            elif choice == "2":
                self.handle_login()
            elif choice == "3":
                print("👋 Exiting system. Goodbye!")
                break
            else:
                print("❌ Invalid choice.")

    # --- User Registration / Login ---
    def handle_registration(self):
        try:
            print("\n=== 📝 User Registration ===")
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ").strip()
            role = input("Role (admin/customer): ").strip().lower()
            if role not in ("admin", "customer"):
                print("⚠️ Role must be 'admin' or 'customer'. Defaulting to 'customer'.")
                role = "customer"
            address = input("Address (for customers): ").strip() if role == "customer" else ""
            msg = self.user_ctrl.register_user(name, email, password, role, address)
            print(msg)
        except Exception as e:
            print(f"❌ Registration failed: {e}")

    def handle_login(self):
        try:
            print("\n=== 🔐 Login ===")
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ").strip()
            msg = self.user_ctrl.login(email, password)
            print(msg)

            user = self.user_ctrl.get_current_user()
            if user and user.is_logged_in:
                self.session.set_user(user)
                if user.role == "admin":
                    self.admin_menu()
                else:
                    self.customer_menu()
                self.user_ctrl.logout()
                self.session.clear_session()
        except Exception as e:
            print(f"❌ Login failed: {e}")

    # --- Admin Flow ---
    def admin_menu(self):
        while True:
            print("\n=== 🧑‍💼 Admin Dashboard ===")
            print("1. Add Book")
            print("2. Update Book Stock")
            print("3. View All Books")
            print("4. View Users")
            print("5. Logout")
            choice = self._prompt_choice("Enter choice: ", ["1", "2", "3", "4", "5"])
            if choice == "1":
                try:
                    title = input("Title: ").strip()
                    author = input("Author: ").strip()
                    price = self._prompt_float("Price: ", min_val=0)
                    stock = self._prompt_int("Stock: ", min_val=0)
                    if price is None or stock is None:
                        print("⚠️ Operation cancelled.")
                        continue
                    print(self.admin_ctrl.add_book(title, author, price, stock))
                except Exception as e:
                    print(f"❌ Could not add book: {e}")
            elif choice == "2":
                try:
                    book_id = self._prompt_int("Book ID: ", min_val=1)
                    stock = self._prompt_int("New Stock: ", min_val=0)
                    if book_id is None or stock is None:
                        print("⚠️ Operation cancelled.")
                        continue
                    print(self.admin_ctrl.update_book_stock(book_id, stock))
                except Exception as e:
                    print(f"❌ Could not update stock: {e}")
            elif choice == "3":
                try:
                    print(self.admin_ctrl.view_all_books())
                except Exception as e:
                    print(f"❌ Could not load books: {e}")
            elif choice == "4":
                try:
                    print(self.admin_ctrl.view_all_users())
                except Exception as e:
                    print(f"❌ Could not load users: {e}")
            elif choice == "5":
                print("👋 Logging out admin...")
                break
            else:
                print("❌ Invalid choice.")

    # --- Customer Flow ---
    def customer_menu(self):
        user = self.session.get_user()
        while True:
            print("\n=== 🧍 Customer Menu ===")
            print("1. Browse Books")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Update Quantity")
            print("5. Remove from Cart")
            print("6. Checkout")
            print("7. View Orders")
            print("8. Logout")
            choice = self._prompt_choice("Enter choice: ", ["1","2","3","4","5","6","7","8"])

            if choice == "1":
                try:
                    print(self.admin_ctrl.view_all_books())
                except Exception as e:
                    print(f"❌ Could not fetch books: {e}")
            elif choice == "2":
                try:
                    book_id = self._prompt_int("Book ID to add: ", min_val=1)
                    qty = self._prompt_int("Quantity: ", min_val=1)
                    if book_id is None or qty is None:
                        print("⚠️ Operation cancelled.")
                        continue
                    print(self.cart_ctrl.add_to_cart(user.user_id, book_id, qty))
                except Exception as e:
                    print(f"❌ Could not add to cart: {e}")
            elif choice == "3":
                try:
                    print(self.cart_ctrl.view_cart(user.user_id))
                except Exception as e:
                    print(f"❌ Could not show cart: {e}")
            elif choice == "4":
                try:
                    book_id = self._prompt_int("Book ID to update: ", min_val=1)
                    qty = self._prompt_int("New Quantity: ", min_val=1)
                    if book_id is None or qty is None:
                        print("⚠️ Operation cancelled.")
                        continue
                    print(self.cart_ctrl.update_cart(user.user_id, book_id, qty))
                except Exception as e:
                    print(f"❌ Could not update cart: {e}")
            elif choice == "5":
                try:
                    book_id = self._prompt_int("Book ID to remove: ", min_val=1)
                    if book_id is None:
                        print("⚠️ Operation cancelled.")
                        continue
                    print(self.cart_ctrl.remove_from_cart(user.user_id, book_id))
                except Exception as e:
                    print(f"❌ Could not remove item: {e}")
            elif choice == "6":
                try:
                    cart = self.cart_ctrl._get_cart(user.user_id)
                    print(self.order_ctrl.checkout(user.user_id, cart))
                except Exception as e:
                    print(f"❌ Checkout failed: {e}")
            elif choice == "7":
                try:
                    print(self.order_ctrl.view_orders(user.user_id))
                except Exception as e:
                    print(f"❌ Could not fetch orders: {e}")
            elif choice == "8":
                print("👋 Logging out...")
                break
            else:
                print("❌ Invalid choice.")
