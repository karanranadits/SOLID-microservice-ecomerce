from pydantic import BaseModel

class PaymentDetails(BaseModel):
    card_number: str
    expiry: str
    cvv: str
