import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent


# ==========================================
# LOAD .ENV
# ==========================================

load_dotenv(
    BASE_DIR / ".env"
)


# ==========================================
# GEMINI SETTINGS
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# ==========================================
# UPLOAD SETTINGS
# ==========================================

try:

    MAX_UPLOAD_MB = int(
        os.getenv(
            "MAX_UPLOAD_MB",
            "20"
        )
    )

except ValueError:

    MAX_UPLOAD_MB = 20


MAX_UPLOAD_BYTES = (
    MAX_UPLOAD_MB * 1024 * 1024
)


# ==========================================
# UPLOAD DIRECTORY
# ==========================================

UPLOAD_DIR = (
    BASE_DIR / "uploads"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# DATABASE
# ==========================================

DATABASE_PATH = (
    BASE_DIR / "cultural_heritage.db"
)