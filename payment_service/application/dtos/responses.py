from pydantic import BaseModel
from typing import Optional

class ProcessPaymentResponseDTO(BaseModel):
    status: str
    transaction_id: str
    user: str
    checkout_url: Optional[str] = None
