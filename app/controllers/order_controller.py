# # app/controllers/order_controller.py
# from app.repositories.order_repository import OrderRepository
# from app.repositories.book_repository import BookRepository
# from app.models.order import OrderStatus
# from app.models.payment import Payment, PaymentStatus

# class OrderController:
#     """
#     Handles checkout and order management logic.
#     Maps to: Checkout, ValidatePaymentDetails, ProcessPayment, ViewOrders.
#     """

#     def __init__(self):
#         self.order_repo = OrderRepository()
#         self.book_repo = BookRepository()

#     def checkout(self, user_id: int, cart) -> str:
#         try:
#             if cart.is_empty():
#                 return "Cannot checkout an empty cart."

#             total = cart.calculate_total()
#             if total <= 0:
#                 return "Invalid cart total."

#             order_id = self.order_repo.create_order(user_id, total, OrderStatus.PENDING)

#             print("\n--- Payment Section ---")
#             print("Available methods: Card / UPI / COD")
#             method = input("Enter payment method: ").strip().upper()  # Normalize input

#             details = {}
#             if method == "CARD":
#                 details["card_number"] = input("Enter card number (16 digits): ").strip()
#                 details["cvv"] = input("Enter CVV (3 digits): ").strip()
#                 # minimal validation
#                 if len(details["card_number"]) != 16 or not details["card_number"].isdigit():
#                     print("Invalid card number format.")
#                 if len(details["cvv"]) != 3 or not details["cvv"].isdigit():
#                     print("Invalid CVV format.")
#             elif method == "UPI":
#                 details["upi_id"] = input("Enter UPI ID (example@upi): ").strip()
#             elif method == "COD":
#                 print("Cash on Delivery selected.")
#             else:
#                 print("Invalid payment method. Defaulting to CARD.")
#                 method = "CARD"
#                 details["card_number"] = input("Enter card number (16 digits): ").strip()
#                 details["cvv"] = input("Enter CVV (3 digits): ").strip()

#             # Create Payment object (constructor validates method)
#             payment = Payment(None, order_id, method)

#             # Simulated validation rules
#             success = False
#             try:
#                 if method == "CARD" and details.get("card_number", "").startswith("4"):
#                     success = True
#                 elif method == "UPI" and "@UPI" in details.get("upi_id", "").upper():
#                     success = True
#                 elif method == "COD":
#                     success = True
#             except Exception:
#                 success = False

#             # Normalize method again before DB insert (matches schema)
#             method = method.upper()

#             # Persist result safely
#             if success:
#                 payment.status = PaymentStatus.SUCCESS
#                 self.order_repo.add_payment(order_id, method, payment.status)
#                 self.order_repo.update_order_status(order_id, OrderStatus.CONFIRMED)

#                 # Deduct stock (with bounds safety)
#                 for item in cart.items:
#                     try:
#                         new_stock = max(int(item.book.stock) - int(item.quantity), 0)
#                         self.book_repo.update_book(item.book.book_id, new_stock)
#                     except Exception:
#                         pass
#                 cart.clear_cart()

#                 print(f"\nPayment successful using {method}. Order #{order_id} confirmed!")
#             else:
#                 payment.status = PaymentStatus.FAILED
#                 self.order_repo.add_payment(order_id, method, payment.status)
#                 print(f"\nPayment failed using {method}. Order #{order_id} not confirmed.")

#             return f"Payment Status: {payment.status}"
#         except Exception as e:
#             # Ensure a generic, user-friendly failure that doesn't crash the app
#             return f"Checkout failed: {e}"

#     def view_orders(self, user_id: int):
#         try:
#             orders = self.order_repo.get_orders_by_user(user_id)
#             if not orders:
#                 return "No orders found."
#             lines = ["\nOrder History:"]
#             for order in orders:
#                 lines.append(f"Order #{order.order_id} — ₹{order.total_amount} — {order.status}")
#             return "\n".join(lines)
#         except Exception as e:
#             return f"Failed to fetch orders: {e}"



# app/controllers/order_controller.py
from app.repositories.order_repository import OrderRepository
from app.repositories.book_repository import BookRepository
from app.models.order import OrderStatus
from app.models.payment import Payment, PaymentStatus

class OrderController:
    """
    Handles checkout and order management logic.
    Maps to: Checkout, ValidatePaymentDetails, ProcessPayment, ViewOrders.
    """

    def __init__(self):
        self.order_repo = OrderRepository()
        self.book_repo = BookRepository()

    def checkout(self, user_id: int, cart) -> str:
        try:
            # --- Validate cart ---
            if cart.is_empty():
                return "Cannot checkout an empty cart."

            total = cart.calculate_total()
            if total <= 0:
                return "Invalid cart total."

            # --- Create new order ---
            order_id = self.order_repo.create_order(user_id, total, OrderStatus.PENDING)

            print("\n--- Payment Section ---")
            print("Available methods: Card / UPI / COD")
            method = input("Enter payment method: ").strip().upper()  # normalize user input

            # --- Collect payment details ---
            details = {}
            if method == "CARD":
                details["card_number"] = input("Enter card number (16 digits): ").strip()
                details["cvv"] = input("Enter CVV (3 digits): ").strip()

                # Minimal format validation
                if len(details["card_number"]) != 16 or not details["card_number"].isdigit():
                    print("Invalid card number format.")
                if len(details["cvv"]) != 3 or not details["cvv"].isdigit():
                    print("Invalid CVV format.")

            elif method == "UPI":
                details["upi_id"] = input("Enter UPI ID (example@upi): ").strip()

            elif method == "COD":
                print("Cash on Delivery selected.")

            else:
                print("Invalid payment method. Defaulting to CARD.")
                method = "CARD"
                details["card_number"] = input("Enter card number (16 digits): ").strip()
                details["cvv"] = input("Enter CVV (3 digits): ").strip()

            # --- Create Payment object ---
            payment = Payment(None, order_id, method)

            # --- Simulate payment validation ---
            success = False
            try:
                if method == "CARD" and details.get("card_number", "").startswith("4"):
                    success = True
                elif method == "UPI" and "@UPI" in details.get("upi_id", "").upper():
                    success = True
                elif method == "COD":
                    success = True
            except Exception:
                success = False

            # --- Normalize for DB constraint (critical fix) ---
            # Database CHECK constraint expects: 'Card', 'UPI', 'COD'
            db_method_map = {"CARD": "Card", "UPI": "UPI", "COD": "COD"}
            db_method = db_method_map.get(method.strip().upper(), "Card")  # Default to 'Card'

            # --- Persist payment and update order ---
            if success:
                payment.status = PaymentStatus.SUCCESS
                self.order_repo.add_payment(order_id, db_method, payment.status)
                self.order_repo.update_order_status(order_id, OrderStatus.CONFIRMED)

                # Deduct stock safely
                for item in cart.items:
                    try:
                        new_stock = max(int(item.book.stock) - int(item.quantity), 0)
                        self.book_repo.update_book(item.book.book_id, new_stock)
                    except Exception:
                        pass

                cart.clear_cart()
                print(f"\nPayment successful using {db_method}. Order #{order_id} confirmed!")

            else:
                payment.status = PaymentStatus.FAILED
                self.order_repo.add_payment(order_id, db_method, payment.status)
                print(f"\nPayment failed using {db_method}. Order #{order_id} not confirmed.")

            return f"Payment Status: {payment.status}"

        except Exception as e:
            # Generic safe fallback for any unforeseen issue
            return f"Checkout failed: {e}"

    def view_orders(self, user_id: int):
        try:
            orders = self.order_repo.get_orders_by_user(user_id)
            if not orders:
                return "No orders found."
            lines = ["\nOrder History:"]
            for order in orders:
                lines.append(f"Order #{order.order_id} — ₹{order.total_amount} — {order.status}")
            return "\n".join(lines)
        except Exception as e:
            return f"Failed to fetch orders: {e}"
