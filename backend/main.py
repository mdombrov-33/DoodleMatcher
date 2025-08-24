from fastapi import FastAPI
from backend.routes import search
from routes import health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(search.router, prefix="/api", tags=["Search"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
