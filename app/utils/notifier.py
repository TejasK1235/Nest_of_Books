# app/utils/notifier.py
class Observer:
    def update(self, order_id: int, status: str):
        raise NotImplementedError

class CustomerNotifier(Observer):
    def update(self, order_id: int, status: str):
        print(f"📢 Notification to Customer: Order #{order_id} is now {status}.")

class AdminNotifier(Observer):
    def update(self, order_id: int, status: str):
        print(f"📢 Notification to Admin: Order #{order_id} changed to {status}.")

class Notifier:
    """
    Observable — manages observers and broadcasts updates.
    Implements Observer pattern.
    """
    observers: list[Observer] = []

    @classmethod
    def register(cls, observer: Observer):
        cls.observers.append(observer)

    @classmethod
    def notify(cls, order_id: int, status: str):
        for observer in cls.observers:
            observer.update(order_id, status)
