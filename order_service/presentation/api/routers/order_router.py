from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from application.dtos.requests import PlaceOrderRequestDTO
from application.dtos.responses import OrderResponseDTO, OrderItemResponseDTO
from application.use_cases import PlaceOrderUseCase
from domain.entities.order_item import OrderItem
from presentation.api.dependencies import get_place_order_use_case, verify_token, payment_gateway, order_repo

router = APIRouter()

@router.post("/orders", response_model=OrderResponseDTO, status_code=201)
def create_order(
    request: PlaceOrderRequestDTO, 
    use_case: PlaceOrderUseCase = Depends(get_place_order_use_case),
    username: str = Depends(verify_token),
    authorization: str = Header(None)
):
    try:
        # Pass the auth token down to the gateway to forward it to payment_service
        payment_gateway.set_token(authorization)
        
        # Map DTO to Entity
        items = [OrderItem(product_id=item.product_id, quantity=item.quantity, price=item.price) for item in request.items]

        shipping_address = None
        if request.shipping_address:
            shipping_address = {
                "street": request.shipping_address.street,
                "city": request.shipping_address.city,
                "state": request.shipping_address.state,
                "zip_code": request.shipping_address.zip_code,
                "country": request.shipping_address.country
            }

        order = use_case.execute(
            customer_id=username, 
            customer_name=request.customer_name,
            shipping_address=shipping_address,
            items=items
        )
        
        # Map Entity to Response DTO
        response_items = [OrderItemResponseDTO(product_id=item.product_id, quantity=item.quantity, price=item.price) for item in order.items]
        return OrderResponseDTO(
            id=order.id,
            customer_id=order.customer_id,
            items=response_items,
            total_amount=order.total_amount,
            status=order.status,
            checkout_url=order.checkout_url
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}/confirm", response_model=OrderResponseDTO)
def confirm_order(order_id: str, username: str = Depends(verify_token)):
    order = order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.customer_id != username:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    order.status = "paid"
    order_repo.save(order)
    
    response_items = [OrderItemResponseDTO(product_id=item.product_id, quantity=item.quantity, price=item.price) for item in order.items]
    return OrderResponseDTO(
        id=order.id,
        customer_id=order.customer_id,
        items=response_items,
        total_amount=order.total_amount,
        status=order.status,
        checkout_url=order.checkout_url
    )

@router.get("/orders", response_model=List[OrderResponseDTO])
def list_orders(username: str = Depends(verify_token)):
    # simple listing from mock db filtering by customer_id
    orders = [o for o in order_repo._db.values() if o.customer_id == username]
    
    result = []
    for order in orders:
        response_items = [OrderItemResponseDTO(product_id=item.product_id, quantity=item.quantity, price=item.price) for item in order.items]
        result.append(OrderResponseDTO(
            id=order.id,
            customer_id=order.customer_id,
            items=response_items,
            total_amount=order.total_amount,
            status=order.status
        ))
    return result
