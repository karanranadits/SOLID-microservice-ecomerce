from typing import Optional
from domain.entities.user import User
from application.interfaces.user_repository import UserRepository

class MemoryUserRepository(UserRepository):
    def __init__(self):
        # Mock Database
        self._db = {
            "admin": User(username="admin", password_hash="password123")
        }

    def find_by_username(self, username: str) -> Optional[User]:
        return self._db.get(username)

    def save(self, user: User) -> None:
        self._db[user.username] = user
