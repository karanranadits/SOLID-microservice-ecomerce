import logging
import uuid
from typing import List
from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from application.interfaces import OrderWriter, PaymentGateway
from application.strategies import DiscountStrategy

logger = logging.getLogger(__name__)

# SAGA ORCHESTRATOR & SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# This class acts as a Saga Orchestrator for the Order Creation process.
# Step 1: Save Pending Order (Local Transaction)
# Step 2: Call PaymentGateway (External Call)
# Step 3: Compensate if payment fails.

class PlaceOrderUseCase:
    def __init__(
        self, 
        order_writer: OrderWriter, 
        payment_gateway: PaymentGateway,
        discount_strategy: DiscountStrategy
    ):
        self.order_writer = order_writer
        self.payment_gateway = payment_gateway
        self.discount_strategy = discount_strategy

    def execute(self, customer_id: str, customer_name: str, shipping_address: dict, items: List[OrderItem]) -> Order:
        # 1. Calculate total
        raw_total = sum(item.price * item.quantity for item in items)
        
        # 2. Apply OCP discount strategy
        final_total = self.discount_strategy.apply_discount(raw_total)

        # 3. Create Order Entity (Saga Step 1: Pending Order)
        from domain.entities.order import ShippingAddress
        
        address_obj = ShippingAddress(**shipping_address) if shipping_address else None

        order = Order(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            customer_name=customer_name,
            shipping_address=address_obj,
            items=items,
            total_amount=final_total,
            status="pending"
        )
        
        # Save initially as pending
        self.order_writer.save(order)
        
        # 4. Request Checkout Session (Saga Step 2: External Call)
        logger.info(f"Saga: Requesting checkout session for order {order.id}")
        checkout_url = self.payment_gateway.process_payment(order.id, order.total_amount)
        
        # 5. Saga Completion Wait
        if checkout_url:
            logger.info(f"Saga: Checkout session created for order {order.id}")
            order.checkout_url = checkout_url
            # Order stays 'pending' until webhook/confirmation
        else:
            logger.error(f"Saga: Payment gateway failed to create session for order {order.id}.")
            order.status = "payment_failed"

        # Update Order
        self.order_writer.save(order)
        
        return order
