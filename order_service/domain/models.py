from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class PaymentDetails(BaseModel):
    card_number: str
    expiry: str
    cvv: str

class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"
