from .base_repository import BaseRepository
from app.models.order import Order
from app.models.payment import Payment, PaymentStatus

class OrderRepository(BaseRepository):
    """
    Handles persistence for orders and payments with error handling.
    """

    def create_tables(self):
        try:
            self.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL,
                status TEXT
            )""")
            self.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                method TEXT CHECK(method IN ('Card','UPI','COD')),
                status TEXT
            )""")
        except Exception as e:
            print(f"❌ Failed to create order/payment tables: {e}")

    def create_order(self, user_id: int, total_amount: float, status: str = "Pending") -> int:
        try:
            self.execute(
                "INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)",
                (user_id, total_amount, status),
            )
            return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except Exception as e:
            print(f"❌ Failed to create order for user {user_id}: {e}")
            return -1

    def get_orders_by_user(self, user_id: int):
        try:
            rows = self.fetch_all("SELECT * FROM orders WHERE user_id = ?", (user_id,))
            return [Order(r["order_id"], r["user_id"], r["total_amount"], r["status"]) for r in rows]
        except Exception as e:
            print(f"❌ Error fetching orders for user {user_id}: {e}")
            return []

    def update_order_status(self, order_id: int, new_status: str):
        try:
            self.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
        except Exception as e:
            print(f"❌ Failed to update order {order_id}: {e}")

    # --- Payment Methods ---
    def add_payment(self, order_id: int, method: str, status: str = PaymentStatus.PENDING) -> int:
        try:
            self.execute(
                "INSERT INTO payments (order_id, method, status) VALUES (?, ?, ?)",
                (order_id, method, status),
            )
            return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except Exception as e:
            print(f"❌ Failed to add payment for order {order_id}: {e}")
            return -1

    def update_payment_status(self, payment_id: int, new_status: str):
        try:
            self.execute("UPDATE payments SET status = ? WHERE payment_id = ?", (new_status, payment_id))
        except Exception as e:
            print(f"❌ Failed to update payment {payment_id}: {e}")

    def get_payment_by_order(self, order_id: int) -> Payment | None:
        try:
            row = self.fetch_one("SELECT * FROM payments WHERE order_id = ?", (order_id,))
            if not row:
                return None
            return Payment(row["payment_id"], row["order_id"], row["method"], row["status"])
        except Exception as e:
            print(f"❌ Error fetching payment for order {order_id}: {e}")
            return None
