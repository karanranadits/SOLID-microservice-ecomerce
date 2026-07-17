from abc import ABC, abstractmethod
from domain.entities.order import Order

# OPEN/CLOSED PRINCIPLE (OCP)
# Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.
# We can add new discount strategies without modifying the PricingService or existing strategies.

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply_discount(self, amount: float) -> float:
        return amount - (amount * (self.percentage / 100))

class FlatRateDiscount(DiscountStrategy):
    def __init__(self, flat_rate: float):
        self.flat_rate = flat_rate

    def apply_discount(self, amount: float) -> float:
        return max(0.0, amount - self.flat_rate)
