# Privacy Policy

**plex-reddit-comments** is a personal, non-commercial, open-source tool that
runs on the user's own computer or home server.

## What data is accessed
- **Plex:** movie titles and release years from the user's own Plex library.
- **Reddit:** publicly visible posts and comments from a small, fixed list of
  film subreddits, retrieved read-only through Reddit's Data API.

## What is stored
- Comment text, score, and permalink for recently viewed movies, in a local
  SQLite file on the user's own machine.
- Reddit usernames of commenters are **not** stored or displayed.
- Nothing is sent to any third party, and no analytics are used.

## Retention and deletion
- Cached Reddit content is automatically deleted after at most 24 hours
  (never more than 48 hours).
- Comments that appear as removed or deleted are not displayed.
- The user can delete all stored data at any time by deleting the cache file.

## Use restrictions
- Reddit data is not used to train machine learning or AI models.
- Reddit data is not sold, licensed, or redistributed.
- The tool does not post, vote, comment, or send messages on Reddit.

## Compliance
This project follows Reddit's Responsible Builder Policy and Data API Terms.

## Contact
Open an issue on this repository.
