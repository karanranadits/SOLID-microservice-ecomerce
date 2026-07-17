from fastapi import HTTPException, Header
import jwt
from application.use_cases.process_payment import ProcessPaymentUseCase

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

from infrastructure.stripe_gateway import StripeGateway
from infrastructure.repositories.sqlite_payment_repository import SQLitePaymentRepository

payment_gateway = StripeGateway()
payment_repo = SQLitePaymentRepository()

def get_process_payment_use_case() -> ProcessPaymentUseCase:
    return ProcessPaymentUseCase(
        payment_gateway=payment_gateway,
        payment_repo=payment_repo
    )
