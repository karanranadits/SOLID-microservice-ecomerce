from domain.entities.token import Token
from application.interfaces.user_repository import UserRepository
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> Token:
        user = self.user_repository.find_by_username(username)
        if not user or user.password_hash != password:
            raise ValueError("Invalid credentials")
        
        return self._create_token(username)

    def _create_token(self, username: str) -> Token:
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=access_token, token_type="bearer")
