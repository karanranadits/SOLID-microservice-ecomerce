import sqlite3
from typing import Optional
from domain.entities.payment import Payment
from application.interfaces.payment_repository import PaymentRepository

class SQLitePaymentRepository(PaymentRepository):
    def __init__(self, db_path: str = "payments.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    transaction_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    checkout_url TEXT
                )
            ''')
            conn.commit()

    def save(self, payment: Payment) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO payments (transaction_id, order_id, amount, status, checkout_url) 
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(transaction_id) DO UPDATE SET 
                    status=excluded.status
            ''', (payment.transaction_id, payment.order_id, payment.amount, payment.status, payment.checkout_url))
            conn.commit()

    def get_by_id(self, transaction_id: str) -> Optional[Payment]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT transaction_id, order_id, amount, status, checkout_url FROM payments WHERE transaction_id = ?", (transaction_id,))
            row = cursor.fetchone()
            if row:
                return Payment(
                    transaction_id=row[0],
                    order_id=row[1],
                    amount=row[2],
                    status=row[3],
                    checkout_url=row[4]
                )
            return None
