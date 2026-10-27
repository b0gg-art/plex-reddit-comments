"""Loads settings from environment variables (.env file supported)."""
import os

from dotenv import load_dotenv

load_dotenv()

PLEX_URL = os.getenv("PLEX_URL", "")
PLEX_TOKEN = os.getenv("PLEX_TOKEN", "")
PLEX_LIBRARY = os.getenv("PLEX_LIBRARY", "Movies")

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")
REDDIT_USER_AGENT = os.getenv(
    "REDDIT_USER_AGENT", "plex-reddit-comments/0.1 by u/unknown"
)

# Small, fixed list of subreddits. Keep this short.
SUBREDDITS = [s.strip() for s in os.getenv("SUBREDDITS", "movies,TrueFilm").split(",") if s.strip()]
MAX_COMMENTS = int(os.getenv("MAX_COMMENTS", "10"))

# Cached Reddit content is deleted after this many hours.
# Keep this at or below 48 to respect Reddit's deletion requirements.
CACHE_TTL_HOURS = min(int(os.getenv("CACHE_TTL_HOURS", "24")), 48)
DB_PATH = os.getenv("DB_PATH", "cache.db")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5055"))


def missing(*names):
    """Return the names of any required settings that are empty."""
    return [n for n in names if not globals().get(n)]
