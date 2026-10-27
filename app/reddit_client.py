"""Read-only Reddit lookups: find a movie's discussion thread and top comments.

This module never posts, votes, or messages. It only reads.
"""
import praw

from . import cache, config

REMOVED_BODIES = {"[removed]", "[deleted]"}


def _reddit():
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD,
        user_agent=config.REDDIT_USER_AGENT,
    )
    reddit.read_only = True  # enforce read-only behavior
    return reddit


def _find_thread(reddit, title, year):
    """Search the configured subreddits for the best-matching discussion thread."""
    needle = title.lower()
    fallback = None
    for name in config.SUBREDDITS:
        query = f'{title} {year} "Official Discussion"'
        for post in reddit.subreddit(name).search(query, sort="relevance", limit=5):
            post_title = post.title.lower()
            if needle in post_title and "discussion" in post_title:
                return post
            if needle in post_title and fallback is None:
                fallback = post
    return fallback


def _top_comments(submission):
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=0)  # don't expand "load more" chains
    results = []
    for c in submission.comments:
        body = (c.body or "").strip()
        if not body or body in REMOVED_BODIES:
            continue
        # Author names are intentionally not stored or shown.
        results.append(
            {
                "score": c.score,
                "body": body,
                "permalink": f"https://www.reddit.com{c.permalink}",
            }
        )
        if len(results) >= config.MAX_COMMENTS:
            break
    return results


def get_discussion(rating_key, title, year):
    """Return cached discussion data if fresh, otherwise fetch it once and cache it."""
    key = f"movie:{rating_key}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    problems = config.missing(
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"
    )
    if problems:
        return {"error": f"Reddit credentials not configured: {', '.join(problems)}"}

    reddit = _reddit()
    thread = _find_thread(reddit, title, year)
    if thread is None:
        data = {"thread": None, "comments": []}
    else:
        data = {
            "thread": {
                "title": thread.title,
                "subreddit": str(thread.subreddit),
                "url": f"https://www.reddit.com{thread.permalink}",
            },
            "comments": _top_comments(thread),
        }
    cache.put(key, data)
    return data
