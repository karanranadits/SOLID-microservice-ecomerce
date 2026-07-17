import abc
from domain.entities.cart import Cart

class CartRepository(abc.ABC):
    @abc.abstractmethod
    def get_cart(self, username: str) -> Cart:
        pass

    @abc.abstractmethod
    def save_cart(self, cart: Cart) -> None:
        pass

    @abc.abstractmethod
    def clear_cart(self, username: str) -> None:
        pass
