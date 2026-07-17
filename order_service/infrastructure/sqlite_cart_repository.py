import sqlite3
import json
from domain.entities.cart import Cart
from application.interfaces.cart_repository import CartRepository

class SQLiteCartRepository(CartRepository):
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS carts (
                    username TEXT PRIMARY KEY,
                    items_json TEXT NOT NULL
                )
            ''')
            conn.commit()

    def get_cart(self, username: str) -> Cart:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT items_json FROM carts WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                items = json.loads(row[0])
                return Cart(username=username, items=items)
            return Cart(username=username, items=[])

    def save_cart(self, cart: Cart) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            items_json = json.dumps([item.model_dump() for item in cart.items])
            cursor.execute('''
                INSERT INTO carts (username, items_json)
                VALUES (?, ?)
                ON CONFLICT(username) DO UPDATE SET
                    items_json=excluded.items_json
            ''', (cart.username, items_json))
            conn.commit()

    def clear_cart(self, username: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM carts WHERE username = ?", (username,))
            conn.commit()
