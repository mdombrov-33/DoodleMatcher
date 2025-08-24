from fastapi import FastAPI
from routes import health

app = FastAPI()

app.include_router(health.router, prefix="/api", tags=["Health"])
