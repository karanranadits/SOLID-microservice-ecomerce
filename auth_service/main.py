from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routers import auth_router

app = FastAPI(title="SOLID Auth Service - Strict Clean Architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "Auth Service running"}
