from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="LegalEase")

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "LegalEase API is running!"
    }