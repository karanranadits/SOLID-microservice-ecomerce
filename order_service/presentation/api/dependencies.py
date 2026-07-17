from fastapi import HTTPException, Header
import jwt
from application.use_cases import PlaceOrderUseCase
from application.use_cases.cart_use_cases import CartUseCases
from application.strategies import PercentageDiscount
from infrastructure.sqlite_order_repository import SQLiteOrderRepository
from infrastructure.sqlite_cart_repository import SQLiteCartRepository
from infrastructure.gateways import StripePaymentGateway

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

order_repo = SQLiteOrderRepository()
cart_repo = SQLiteCartRepository()
payment_gateway = StripePaymentGateway()

def get_place_order_use_case() -> PlaceOrderUseCase:
    discount_strategy = PercentageDiscount(10.0)
    return PlaceOrderUseCase(
        order_writer=order_repo,
        payment_gateway=payment_gateway,
        discount_strategy=discount_strategy
    )

def get_cart_use_cases() -> CartUseCases:
    return CartUseCases(cart_repo=cart_repo)

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
