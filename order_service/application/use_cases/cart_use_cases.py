from application.interfaces.cart_repository import CartRepository
from domain.entities.cart import Cart, CartItem

class CartUseCases:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    def get_cart(self, username: str) -> Cart:
        return self.cart_repo.get_cart(username)

    def add_item(self, username: str, product_id: str, name: str, price: float, quantity: int = 1) -> Cart:
        cart = self.cart_repo.get_cart(username)
        
        # Check if item exists
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart.items.append(CartItem(product_id=product_id, name=name, price=price, quantity=quantity))
            
        self.cart_repo.save_cart(cart)
        return cart

    def remove_item(self, username: str, product_id: str) -> Cart:
        cart = self.cart_repo.get_cart(username)
        cart.items = [item for item in cart.items if item.product_id != product_id]
        self.cart_repo.save_cart(cart)
        return cart

    def clear_cart(self, username: str) -> None:
        self.cart_repo.clear_cart(username)
