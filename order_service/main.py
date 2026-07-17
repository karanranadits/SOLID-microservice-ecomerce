from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.routers import order_router, cart_router

app = FastAPI(
    title="SOLID Order Service",
    description="A simple FastAPI microservice demonstrating SOLID principles",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router.router, prefix="/api/v1")
app.include_router(cart_router.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the SOLID Order Service!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
