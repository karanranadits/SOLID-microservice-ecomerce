from pydantic import BaseModel

class ProcessPaymentRequestDTO(BaseModel):
    order_id: str
    amount: float
