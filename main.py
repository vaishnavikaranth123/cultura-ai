from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database.database import initialize_database
from backend.api import (
    creators,
    works,
    stories,
    accessibility,
    translation,
    immersive,
    research,
)

app = FastAPI(
    title="Cultura AI",
    description="Human creativity, culture and technology platform",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

app.include_router(creators.router)
app.include_router(works.router)
app.include_router(stories.router)
app.include_router(accessibility.router)
app.include_router(translation.router)
app.include_router(immersive.router)
app.include_router(research.router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "platform": "Cultura AI",
        "message": "Platform is running.",
    }


@app.get("/api")
def home():
    return {
        "name": "Cultura AI",
        "purpose": "Amplify human creativity and preserve cultural stories.",
        "principle": "AI assists creators; it does not replace them.",
    }


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
UPLOAD_DIR = BASE_DIR / "uploads"

if UPLOAD_DIR.exists():
    app.mount(
        "/uploads",
        StaticFiles(directory=str(UPLOAD_DIR)),
        name="uploads",
    )

if FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )