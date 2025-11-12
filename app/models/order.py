# app/models/order.py
from __future__ import annotations
from typing import Optional, List, Dict
from datetime import datetime

class OrderStatus:
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

    @classmethod
    def allowed(cls) -> List[str]:
        return [cls.PENDING, cls.CONFIRMED, cls.CANCELLED]

class Order:
    """
    UML: Order
    +orderId: int
    +orderDate: date
    +totalAmount: double
    +status: string
    +updateStatus()
    +generateInvoice()
    Association: 1..1 Payment
    """
    def __init__(self, order_id: Optional[int], user_id: int, total_amount: float,
                 status: str = OrderStatus.PENDING, order_date: Optional[datetime] = None):
        if total_amount < 0:
            raise ValueError("total_amount must be >= 0")
        if status not in OrderStatus.allowed():
            raise ValueError("invalid order status")

        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = round(float(total_amount), 2)
        self.status = status
        self.order_date = order_date or datetime.now()

    # --- Operations ---
    def update_status(self, new_status: str) -> None:
        if new_status not in OrderStatus.allowed():
            raise ValueError("invalid order status")
        # Simple state machine: Pending -> Confirmed/Cancelled; Confirmed -> (no change)
        if self.status == OrderStatus.CONFIRMED and new_status != OrderStatus.CONFIRMED:
            raise ValueError("confirmed orders cannot change status")
        self.status = new_status

    def confirm(self) -> None:
        self.update_status(OrderStatus.CONFIRMED)

    def cancel(self) -> None:
        if self.status == OrderStatus.CONFIRMED:
            raise ValueError("cannot cancel confirmed order")
        self.update_status(OrderStatus.CANCELLED)

    def generate_invoice(self) -> Dict[str, str]:
        """
        Returns a lightweight invoice representation (used by CLI / demo).
        """
        return {
            "order_id": str(self.order_id),
            "user_id": str(self.user_id),
            "date": self.order_date.strftime("%Y-%m-%d %H:%M"),
            "total": f"{self.total_amount:.2f}",
            "status": self.status,
        }

    def __repr__(self) -> str:
        return f"<Order id={self.order_id} user={self.user_id} total={self.total_amount} status={self.status}>"
