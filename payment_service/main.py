from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import logging

app = FastAPI(title="SOLID Payment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PaymentDetails(BaseModel):
    card_number: str
    expiry: str
    cvv: str

class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    payment_details: PaymentDetails

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/pay")
def process_payment(request: PaymentRequest, authorization: str = Header(None)):
    username = verify_token(authorization)
    logger.info(f"Processing payment of {request.amount} for order {request.order_id} by user {username}")
    
    # Mock Validation
    if len(request.payment_details.card_number) != 16:
        logger.error("Invalid card number length.")
        raise HTTPException(status_code=400, detail="Invalid card number. Must be 16 digits.")
        
    # Simulating successful payment logic
    return {"status": "success", "transaction_id": "tx_12345", "user": username}

@app.get("/")
def root():
    return {"message": "Payment Service running"}
