from fastapi import FastAPI
from routes import health, search, populate_qdrant
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(populate_qdrant.router, prefix="/api", tags=["Populate Qdrant"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
