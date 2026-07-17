import sqlite3
import json
from typing import Optional
from domain.entities.user import User
from domain.entities.profile import Profile
from application.interfaces.user_repository import UserRepository

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    profile_json TEXT
                )
            ''')
            conn.commit()
            
            # Create default admin if not exists
            cursor.execute("SELECT username FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                admin_user = User(username="admin", password_hash="password123")
                cursor.execute(
                    "INSERT INTO users (username, password_hash, profile_json) VALUES (?, ?, ?)",
                    (admin_user.username, admin_user.password_hash, admin_user.profile.model_dump_json())
                )
                conn.commit()

    def find_by_username(self, username: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password_hash, profile_json FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                uname, pw_hash, profile_json = row
                user = User(username=uname, password_hash=pw_hash)
                if profile_json:
                    user.profile = Profile.model_validate_json(profile_json)
                return user
            return None

    def save(self, user: User) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            profile_json = user.profile.model_dump_json() if user.profile else None
            cursor.execute('''
                INSERT INTO users (username, password_hash, profile_json) 
                VALUES (?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET 
                    password_hash=excluded.password_hash,
                    profile_json=excluded.profile_json
            ''', (user.username, user.password_hash, profile_json))
            conn.commit()
