from pydantic import BaseModel
from typing import List, Optional

class OrderItemDTO(BaseModel):
    product_id: str
    quantity: int
    price: float

class ShippingAddressDTO(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class PlaceOrderRequestDTO(BaseModel):
    customer_name: str
    shipping_address: ShippingAddressDTO
    items: List[OrderItemDTO]

class AddToCartRequestDTO(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = 1
