from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, photos
from app.db import Base, SessionLocal, engine
from app.migrate import migrate_photos_schema
from app.models.photo import PhotoModel  # noqa: F401 — register model with Base
from app.seed import seed_photos


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    migrate_photos_schema()
    db = SessionLocal()
    try:
        seed_photos(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="my-photo-gallery API",
    version="0.3.0",
    description="Photo gallery backend (SQLite BLOB + SQLAlchemy).",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(photos.router)
