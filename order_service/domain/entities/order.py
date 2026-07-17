from pydantic import BaseModel
from typing import List, Optional
from domain.entities.order_item import OrderItem

class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class Order(BaseModel):
    id: str
    customer_id: str
    customer_name: str = ""
    shipping_address: Optional[ShippingAddress] = None
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"
    checkout_url: Optional[str] = None
