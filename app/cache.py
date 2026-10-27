"""Tiny SQLite cache. Entries expire and are deleted after CACHE_TTL_HOURS."""
import json
import sqlite3
import time

from . import config


def _conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cache ("
        "key TEXT PRIMARY KEY, payload TEXT NOT NULL, fetched_at REAL NOT NULL)"
    )
    return conn


def purge_expired():
    """Delete every entry older than the TTL."""
    cutoff = time.time() - config.CACHE_TTL_HOURS * 3600
    with _conn() as conn:
        conn.execute("DELETE FROM cache WHERE fetched_at < ?", (cutoff,))


def get(key):
    """Return cached data if it is still fresh, otherwise None."""
    purge_expired()
    with _conn() as conn:
        row = conn.execute("SELECT payload FROM cache WHERE key = ?", (key,)).fetchone()
    return json.loads(row[0]) if row else None


def put(key, data):
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO cache (key, payload, fetched_at) VALUES (?, ?, ?)",
            (key, json.dumps(data), time.time()),
        )
