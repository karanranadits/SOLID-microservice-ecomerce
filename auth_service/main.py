from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="SOLID Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "my_super_secret_jwt_key"
ALGORITHM = "HS256"

class UserCredentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Mock Database for demo
MOCK_USERS = {
    "admin": "password123"
}

@app.post("/register", response_model=Token)
def register(credentials: UserCredentials):
    if credentials.username in MOCK_USERS:
        raise HTTPException(status_code=400, detail="Username already registered")
    MOCK_USERS[credentials.username] = credentials.password
    return _create_token(credentials.username)

@app.post("/login", response_model=Token)
def login(credentials: UserCredentials):
    if credentials.username not in MOCK_USERS or MOCK_USERS[credentials.username] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return _create_token(credentials.username)

def _create_token(username: str) -> Token:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="bearer")

@app.get("/")
def root():
    return {"message": "Auth Service running"}
