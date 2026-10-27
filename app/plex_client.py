"""Read-only access to your own Plex movie library."""
from plexapi.server import PlexServer

from . import config


def _section():
    plex = PlexServer(config.PLEX_URL, config.PLEX_TOKEN)
    return plex.library.section(config.PLEX_LIBRARY)


def list_movies(query=None, limit=100):
    """Return [{rating_key, title, year}] for movies in the library."""
    section = _section()
    items = section.search(title=query) if query else section.all()
    return [
        {"rating_key": m.ratingKey, "title": m.title, "year": m.year}
        for m in items[:limit]
    ]


def get_movie(rating_key):
    """Return {rating_key, title, year} for one movie, or None."""
    try:
        m = _section().fetchItem(int(rating_key))
    except Exception:
        return None
    return {"rating_key": m.ratingKey, "title": m.title, "year": m.year}
