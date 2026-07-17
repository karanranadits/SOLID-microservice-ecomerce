from pydantic import BaseModel
from typing import List, Optional

class OrderItemResponseDTO(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderResponseDTO(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItemResponseDTO]
    total_amount: float
    status: str
    checkout_url: Optional[str] = None

class CartItemDTO(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class CartResponseDTO(BaseModel):
    username: str
    items: List[CartItemDTO]
    total_amount: float
