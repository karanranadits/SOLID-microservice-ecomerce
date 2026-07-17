import logging
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routers import payment_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="SOLID Payment Service - Strict Clean Architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router.router)

@app.get("/")
def root():
    return {"message": "Payment Service running"}
