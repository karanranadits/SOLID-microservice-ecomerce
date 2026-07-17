import sqlite3
import json
from typing import Optional, List
from domain.entities.order import Order
from application.interfaces import OrderWriter, OrderReader

class SQLiteOrderRepository(OrderWriter, OrderReader):
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    customer_name TEXT,
                    shipping_address_json TEXT,
                    items_json TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    checkout_url TEXT
                )
            ''')
            conn.commit()

    def save(self, order: Order) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            shipping_address_json = order.shipping_address.model_dump_json() if order.shipping_address else None
            items_json = json.dumps([item.model_dump() for item in order.items])
            
            cursor.execute('''
                INSERT INTO orders (id, customer_id, customer_name, shipping_address_json, items_json, total_amount, status, checkout_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status=excluded.status,
                    checkout_url=excluded.checkout_url
            ''', (
                order.id, order.customer_id, order.customer_name, 
                shipping_address_json, items_json, order.total_amount, 
                order.status, order.checkout_url
            ))
            conn.commit()

    def get_by_id(self, order_id: str) -> Optional[Order]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_order(row)
            return None

    def get_all_by_customer(self, customer_id: str) -> List[Order]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
            rows = cursor.fetchall()
            return [self._row_to_order(row) for row in rows]

    def _row_to_order(self, row) -> Order:
        order_dict = {
            "id": row[0],
            "customer_id": row[1],
            "customer_name": row[2],
            "total_amount": row[5],
            "status": row[6],
            "checkout_url": row[7],
            "items": json.loads(row[4])
        }
        if row[3]:
            order_dict["shipping_address"] = json.loads(row[3])
        return Order(**order_dict)
