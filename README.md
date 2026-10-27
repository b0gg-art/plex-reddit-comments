# plex-reddit-comments

A personal, non-commercial tool that shows relevant Reddit discussion
for movies in my own Plex library.

## What it does
For a movie in my Plex library, it finds the discussion thread in
r/movies (and a few other film subreddits) and displays the top comments
on a local web page.

## Reddit data usage
- Access: read-only (search + comment listing)
- Subreddits: r/movies, r/TrueFilm, r/horror (configurable, small list)
- Volume: on-demand lookups for one user; results cached; well under rate limits
- Account: single personal account
- Commercial: no

## Policy compliance
- Follows Reddit's Responsible Builder Policy and Data API Terms
- Comments are cached briefly; deleted/removed content is purged on refresh
  and within 48 hours
- No AI/ML training, no redistribution, no posting or voting

## Setup
Copy `.env.example` to `.env` and fill in Plex and Reddit credentials.
