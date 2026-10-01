from fastapi import FastAPI

app = FastAPI(
    title="Address Book API",
    description="Address Book API with coordinates based search",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message":"Address book API is running"}