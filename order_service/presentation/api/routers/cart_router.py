from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from application.dtos.requests import AddToCartRequestDTO
from application.dtos.responses import CartResponseDTO, CartItemDTO
from application.use_cases.cart_use_cases import CartUseCases
from presentation.api.dependencies import get_cart_use_cases, verify_token

router = APIRouter()

@router.get("/cart", response_model=CartResponseDTO)
def get_cart(
    use_cases: CartUseCases = Depends(get_cart_use_cases),
    username: str = Depends(verify_token)
):
    cart = use_cases.get_cart(username)
    items = [CartItemDTO(product_id=item.product_id, name=item.name, price=item.price, quantity=item.quantity) for item in cart.items]
    return CartResponseDTO(username=username, items=items, total_amount=cart.total_amount)

@router.post("/cart", response_model=CartResponseDTO)
def add_to_cart(
    request: AddToCartRequestDTO,
    use_cases: CartUseCases = Depends(get_cart_use_cases),
    username: str = Depends(verify_token)
):
    cart = use_cases.add_item(
        username=username,
        product_id=request.product_id,
        name=request.name,
        price=request.price,
        quantity=request.quantity
    )
    items = [CartItemDTO(product_id=item.product_id, name=item.name, price=item.price, quantity=item.quantity) for item in cart.items]
    return CartResponseDTO(username=username, items=items, total_amount=cart.total_amount)

@router.delete("/cart/{product_id}", response_model=CartResponseDTO)
def remove_from_cart(
    product_id: str,
    use_cases: CartUseCases = Depends(get_cart_use_cases),
    username: str = Depends(verify_token)
):
    cart = use_cases.remove_item(username=username, product_id=product_id)
    items = [CartItemDTO(product_id=item.product_id, name=item.name, price=item.price, quantity=item.quantity) for item in cart.items]
    return CartResponseDTO(username=username, items=items, total_amount=cart.total_amount)

@router.delete("/cart")
def clear_cart(
    use_cases: CartUseCases = Depends(get_cart_use_cases),
    username: str = Depends(verify_token)
):
    use_cases.clear_cart(username)
    return {"status": "success", "message": "Cart cleared"}
