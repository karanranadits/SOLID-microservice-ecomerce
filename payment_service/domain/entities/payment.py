from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):
    transaction_id: str
    order_id: str
    amount: float
    status: str
    checkout_url: Optional[str] = None
