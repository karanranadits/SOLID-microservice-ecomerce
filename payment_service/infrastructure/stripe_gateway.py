import stripe
import logging
import os
from application.interfaces.payment_gateway import PaymentGateway
from domain.entities.payment import PaymentDetails, Payment

logger = logging.getLogger(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_mock")

class StripeGateway(PaymentGateway):
    def process_payment(self, username: str, order_id: str, amount: float) -> Payment:
        logger.info(f"Creating checkout session for order {order_id}")
        
        if stripe.api_key == "sk_test_mock":
            logger.info("Using Mock Stripe Gateway (no real API key provided)")
            return Payment(
                transaction_id="tx_mock_stripe_123",
                order_id=order_id,
                amount=amount,
                status="pending",
                checkout_url=f"http://localhost:5173/?success=true&order_id={order_id}"
            )
            
        try:
            # We convert amount to cents for Stripe
            amount_in_cents = int(amount * 100)
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order {order_id}',
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://localhost:5173/?success=true&order_id={order_id}',
                cancel_url='http://localhost:5173/?canceled=true',
                client_reference_id=order_id,
                customer_email=f"{username}@example.com" # Just a placeholder
            )
            
            return Payment(
                transaction_id=session.id,
                order_id=order_id,
                amount=amount,
                status="pending",
                checkout_url=session.url
            )
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e.user_message}")
            raise ValueError(f"Checkout failed: {e.user_message}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError("Checkout processing failed due to unexpected error")
