from infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.login_user import LoginUserUseCase
from application.use_cases.manage_profile import GetProfileUseCase, UpdateProfileUseCase
from fastapi import HTTPException, Header
import jwt

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

user_repo = SQLiteUserRepository()

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

def get_register_use_case() -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo)

def get_login_use_case() -> LoginUserUseCase:
    return LoginUserUseCase(user_repo)

def get_profile_use_case() -> GetProfileUseCase:
    return GetProfileUseCase(user_repo)

def update_profile_use_case() -> UpdateProfileUseCase:
    return UpdateProfileUseCase(user_repo)
