import abc
from domain.entities.payment import Payment

class PaymentRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, payment: Payment) -> None:
        pass

    @abc.abstractmethod
    def get_by_id(self, transaction_id: str) -> Payment | None:
        pass
