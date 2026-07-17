from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class Cart(BaseModel):
    username: str
    items: List[CartItem] = []

    @property
    def total_amount(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
