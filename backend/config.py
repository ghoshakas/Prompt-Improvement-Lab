"""Central configuration for the Prompt Improvement Lab backend.

All tunable settings live here in one place. Values can be overridden via
environment variables (loaded from backend/.env), but every one has a sensible
default so the app runs with just a GEMINI_API_KEY set.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# --- Gemini ---------------------------------------------------------------
# Your API key (required). Set it in backend/.env — never commit it.
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

# Which model to call. Google retires model names over time, so this is easy
# to change. gemini-3.6-flash is the current fast, cheap default.
GEMINI_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

# How long to wait on a single Gemini request before giving up (milliseconds).
GEMINI_TIMEOUT_MS: int = _int("GEMINI_TIMEOUT_MS", 30000)

# How many times to attempt a request (handles transient 503 "high demand").
GEMINI_RETRIES: int = _int("GEMINI_RETRIES", 3)


# --- Server ----------------------------------------------------------------
HOST: str = os.environ.get("HOST", "127.0.0.1")
PORT: int = _int("PORT", 8000)

# Browser origins allowed to call the API (the Vite dev server).
ALLOWED_ORIGINS: list[str] = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")
