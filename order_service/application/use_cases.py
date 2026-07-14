import logging
import uuid
from typing import List
from domain.models import Order, OrderItem, PaymentDetails
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

    def execute(self, customer_id: str, items: List[OrderItem], payment_details: PaymentDetails) -> Order:
        # 1. Calculate total
        raw_total = sum(item.price * item.quantity for item in items)
        
        # 2. Apply OCP discount strategy
        final_total = self.discount_strategy.apply_discount(raw_total)

        # 3. Create Order Entity (Saga Step 1: Pending Order)
        order = Order(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            items=items,
            total_amount=final_total,
            status="pending"
        )
        
        # Save initially as pending
        self.order_writer.save(order)
        
        # 4. Process Payment (Saga Step 2: External Call)
        logger.info(f"Saga: Executing payment for order {order.id}")
        payment_success = self.payment_gateway.process_payment(order.id, order.total_amount, payment_details)
        
        # 5. Saga Compensation or Completion
        if payment_success:
            logger.info(f"Saga: Payment succeeded for order {order.id}")
            order.status = "paid"
        else:
            logger.error(f"Saga: Payment failed for order {order.id}. Executing compensation.")
            order.status = "payment_failed"

        # Update Order
        self.order_writer.save(order)
        
        return order
