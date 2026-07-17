import abc
from domain.entities.payment import Payment

class PaymentGateway(abc.ABC):
    @abc.abstractmethod
    def process_payment(self, username: str, order_id: str, amount: float) -> Payment:
        pass
