from __future__ import annotations
from typing import Optional

class PaymentStatus:
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED  = "Failed"

    @classmethod
    def allowed(cls):
        return [cls.PENDING, cls.SUCCESS, cls.FAILED]

class Payment:
    """
    UML: Payment
    +paymentId: int
    +orderId: int
    +paymentType: string
    +status: string
    +validatePayment()
    +processPayment()
    Association: belongs to Order (1:1)
    """
    # All uppercase to match normalization
    VALID_METHODS = {"CARD", "UPI", "COD"}

    def __init__(self, payment_id: Optional[int], order_id: int, method: str,
                 status: str = PaymentStatus.PENDING):
        # Normalize method
        method = method.strip().upper()

        if method not in Payment.VALID_METHODS:
            raise ValueError(f"Unsupported payment method: {method}")
        if status not in PaymentStatus.allowed():
            raise ValueError("invalid payment status")

        self.payment_id = payment_id
        self.order_id = order_id
        self.method = method
        self.status = status

    # --- Operations ---
    def validate_payment(self, amount: float) -> bool:
        """
        Simple validation for console demo:
        - amount > 0
        - method is one of VALID_METHODS
        """
        return amount > 0 and self.method in Payment.VALID_METHODS

    def process_payment(self, amount: float) -> bool:
        """
        Simulated processing:
        - If validate passes, mark Success; else Failed.
        - Controllers/Repos handle persistence.
        """
        if self.validate_payment(amount):
            self.status = PaymentStatus.SUCCESS
            return True
        self.status = PaymentStatus.FAILED
        return False

    def __repr__(self) -> str:
        return (f"<Payment id={self.payment_id} order={self.order_id} "
                f"method={self.method} status={self.status}>")
