from fastapi import FastAPI
from app.routes.address import router as address_router

app = FastAPI(
    title="Address Book API",
    description="Address Book API with coordinates based search",
    version="0.1.0"
)
app.include_router(address_router)

@app.get("/")
def root():
    return {"message":"Address book API is running"}