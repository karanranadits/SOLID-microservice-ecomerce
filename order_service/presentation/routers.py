from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from pydantic import BaseModel
import jwt

from domain.models import Order, OrderItem, PaymentDetails
from application.use_cases import PlaceOrderUseCase
from application.strategies import PercentageDiscount
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import StripePaymentGateway

router = APIRouter()

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

order_repo = InMemoryOrderRepository()
payment_gateway = StripePaymentGateway()

def get_place_order_use_case() -> PlaceOrderUseCase:
    discount_strategy = PercentageDiscount(10.0)
    return PlaceOrderUseCase(
        order_writer=order_repo,
        payment_gateway=payment_gateway,
        discount_strategy=discount_strategy
    )

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

class OrderRequest(BaseModel):
    items: List[OrderItem]
    payment_details: PaymentDetails

@router.post("/orders", response_model=Order, status_code=201)
def create_order(
    request: OrderRequest, 
    use_case: PlaceOrderUseCase = Depends(get_place_order_use_case),
    username: str = Depends(verify_token),
    authorization: str = Header(None)
):
    try:
        # Pass the auth token down to the gateway to forward it to payment_service
        payment_gateway.set_token(authorization)
        order = use_case.execute(
            customer_id=username, 
            items=request.items,
            payment_details=request.payment_details
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders", response_model=List[Order])
def list_orders(username: str = Depends(verify_token)):
    # simple listing from mock db filtering by customer_id
    orders = [o for o in order_repo._db.values() if o.customer_id == username]
    return orders
