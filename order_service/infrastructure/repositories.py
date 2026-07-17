from typing import Optional, Dict
from domain.entities.order import Order
from application.interfaces import OrderWriter, OrderReader

# LISKOV SUBSTITUTION PRINCIPLE (LSP)
# These implementations can substitute the OrderWriter and OrderReader abstractions 
# without breaking the application logic.

class InMemoryOrderRepository(OrderWriter, OrderReader):
    def __init__(self):
        self._db: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._db[order.id] = order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._db.get(order_id)
