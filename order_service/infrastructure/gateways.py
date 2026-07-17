import logging
import requests
import time
from typing import Optional
from application.interfaces import PaymentGateway
from domain.entities.payment_details import PaymentDetails

logger = logging.getLogger(__name__)

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                logger.info("Circuit Breaker transitioning to HALF-OPEN")
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit Breaker is OPEN. Request rejected.")

        try:
            result = func(*args, **kwargs)
            self._reset()
            return result
        except Exception as e:
            self._record_failure()
            raise e

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.warning(f"Circuit Breaker failure count: {self.failure_count}")
        if self.failure_count >= self.failure_threshold:
            logger.error("Circuit Breaker threshold reached. Transitioning to OPEN.")
            self.state = "OPEN"

    def _reset(self):
        if self.state != "CLOSED":
            logger.info("Circuit Breaker transitioning to CLOSED")
            self.state = "CLOSED"
        self.failure_count = 0


class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        self.auth_token = None
        self.payment_service_url = "http://payment_service:8003/pay"
        self.circuit_breaker = CircuitBreaker()

    def set_token(self, token: str):
        self.auth_token = token

    def process_payment(self, order_id: str, amount: float) -> Optional[str]:
        logger.info(f"Calling Payment Service for ${amount} on order {order_id} via Circuit Breaker...")
        headers = {}
        if self.auth_token:
            headers["Authorization"] = self.auth_token
            
        payload = {
            "order_id": order_id, 
            "amount": amount
        }

        def _make_request():
            response = requests.post(
                self.payment_service_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("checkout_url")

        try:
            return self.circuit_breaker.call(_make_request)
        except CircuitBreakerOpenException:
            logger.error("Payment failed because Circuit Breaker is OPEN.")
            return None
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            return None
