import logging
from domain.entities.payment import Payment
from application.interfaces.payment_gateway import PaymentGateway
from application.interfaces.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)

class ProcessPaymentUseCase:
    def __init__(self, payment_gateway: PaymentGateway, payment_repo: PaymentRepository):
        self.payment_gateway = payment_gateway
        self.payment_repo = payment_repo

    def execute(self, username: str, order_id: str, amount: float) -> Payment:
        logger.info(f"Creating checkout session for {amount} on order {order_id} by user {username}")
        
        # Delegate to infrastructure gateway
        payment = self.payment_gateway.process_payment(
            username=username,
            order_id=order_id,
            amount=amount
        )
        
        self.payment_repo.save(payment)
        return payment
