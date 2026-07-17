from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.order import Order
from domain.entities.payment_details import PaymentDetails

# INTERFACE SEGREGATION PRINCIPLE (ISP)
# Instead of one large IOrderRepository, we split into smaller, more specific interfaces.
# Clients (Use Cases) only depend on the interfaces they actually need.

class OrderReader(ABC):
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

class OrderWriter(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, order_id: str, amount: float) -> Optional[str]:
        pass
