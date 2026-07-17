from pydantic import BaseModel

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float
