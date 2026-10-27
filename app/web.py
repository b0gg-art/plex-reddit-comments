"""Small local web page: pick a movie from your Plex library, see Reddit comments."""
from flask import Flask, abort, render_template_string, request

from . import cache, config, plex_client, reddit_client

app = Flask(__name__)

BASE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; padding: 1rem; max-width: 720px;
           margin-inline: auto; background: #111; color: #eee; }
    a { color: #e5a00d; }
    input { padding: .6rem; width: 70%; border-radius: 6px; border: 1px solid #444;
            background: #222; color: #eee; }
    button { padding: .6rem 1rem; border-radius: 6px; border: 0; background: #e5a00d; }
    li { margin: .4rem 0; }
    .comment { background: #1c1c1c; padding: .8rem; border-radius: 8px; margin: .8rem 0;
               white-space: pre-wrap; }
    .meta { color: #999; font-size: .85rem; margin-top: .4rem; }
  </style>
</head>
<body>
  {{ body|safe }}
</body>
</html>
"""

INDEX = """
<h1>Movie discussions</h1>
<form method="get">
  <input name="q" value="{{ q }}" placeholder="Search your Plex library">
  <button>Search</button>
</form>
{% if error %}<p>{{ error }}</p>{% endif %}
<ul>
{% for m in movies %}
  <li><a href="/movie/{{ m.rating_key }}">{{ m.title }} ({{ m.year }})</a></li>
{% endfor %}
</ul>
"""

MOVIE = """
<p><a href="/">&larr; Back</a></p>
<h1>{{ movie.title }} ({{ movie.year }})</h1>
{% if data.error %}
  <p>{{ data.error }}</p>
{% elif not data.thread %}
  <p>No discussion thread found.</p>
{% else %}
  <p>From <a href="{{ data.thread.url }}">r/{{ data.thread.subreddit }}: {{ data.thread.title }}</a></p>
  {% for c in data.comments %}
    <div class="comment">{{ c.body }}
      <div class="meta">{{ c.score }} points &middot; <a href="{{ c.permalink }}">view on Reddit</a></div>
    </div>
  {% endfor %}
{% endif %}
<p class="meta">Content is cached for up to {{ ttl }} hours and then deleted.</p>
"""


def page(title, body_template, **ctx):
    body = render_template_string(body_template, **ctx)
    return render_template_string(BASE, title=title, body=body)


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    movies, error = [], None
    problems = config.missing("PLEX_URL", "PLEX_TOKEN")
    if problems:
        error = f"Plex not configured: {', '.join(problems)}"
    else:
        try:
            movies = plex_client.list_movies(q or None)
        except Exception as exc:  # show a friendly message instead of a stack trace
            error = f"Could not reach Plex: {exc}"
    return page("Movie discussions", INDEX, q=q, movies=movies, error=error)


@app.route("/movie/<int:rating_key>")
def movie(rating_key):
    m = plex_client.get_movie(rating_key)
    if m is None:
        abort(404)
    data = reddit_client.get_discussion(m["rating_key"], m["title"], m["year"])
    return page(m["title"], MOVIE, movie=m, data=data, ttl=config.CACHE_TTL_HOURS)


if __name__ == "__main__":
    cache.purge_expired()
    app.run(host=config.HOST, port=config.PORT)
