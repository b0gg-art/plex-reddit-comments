# plex-reddit-comments

A personal, non-commercial tool that shows relevant Reddit discussion for
movies in my own Plex library.

For a movie in my Plex library, it finds the discussion thread in r/movies
(and a few other film subreddits) and displays the top comments on a local
web page that I can open from my phone.

## Reddit data usage
- **Access:** read-only (search and comment listing)
- **Subreddits:** r/movies, r/TrueFilm (configurable, small fixed list)
- **Volume:** on-demand lookups for a single user, cached, far below rate limits
- **Account:** one personal account
- **Commercial:** no

## Policy compliance
- Follows Reddit's Responsible Builder Policy and Data API Terms
- Cached content is deleted after at most 24 hours (see [PRIVACY.md](PRIVACY.md))
- No AI/ML training, no redistribution, no posting or voting

## Setup
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in your Plex URL and token.
4. Once Reddit approves API access, create a "script" app at
   https://www.reddit.com/prefs/apps and add the client ID, secret, username,
   and password to `.env`.
5. `python -m app.web` and open http://127.0.0.1:5055

To reach it from your phone, set `HOST=0.0.0.0` in `.env` and visit
`http://<your-computer-ip>:5055` on the same Wi-Fi. There is no login, so only
do this on a trusted home network.

## Project layout
```
app/
  config.py         settings from environment variables
  plex_client.py    reads your Plex movie library
  reddit_client.py  read-only Reddit search and comments
  cache.py          SQLite cache with automatic expiry
  web.py            Flask page
```

## License
MIT
