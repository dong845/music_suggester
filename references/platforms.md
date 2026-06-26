# Music Platform Data Sources

Use the richest safe automatic source available. Prefer computer-use automation against the user's installed, downloaded music app, then already-authorized connectors, then file/export fallback. Do not use Chrome, browser control, web players, or music websites to access the user's account or private library. Ordinary web search is allowed for public artist metadata, genre context, release recency, reviews, and candidate discovery. Do not ask the user to provide API keys, tokens, developer app credentials, or files until installed-app access and connector access have been tried or are unavailable.

## General Desktop App Selection

If the user names a platform, use that installed app first. If not, inspect available downloaded music apps and recent app usage, then choose the richest authorized source. Treat Spotify, Apple Music/Music.app, Amazon Music, YouTube Music desktop apps, TIDAL, Deezer, SoundCloud, and other downloaded music clients as peers. Do not default to Spotify unless it is the best available source.

For any desktop app, prioritize surfaces with the strongest personal signal:

1. Liked/loved/favorited tracks or library songs
2. User-created playlists and saved playlists
3. Saved albums and followed artists
4. Recently played/listening history
5. Top tracks, top artists, stations, radio seeds, mixes, and recommendation pages

Normalize records with a `source_platform` field and preserve platform-specific terms such as loved, favorited, added to library, saved, thumbs-up, station, or mix.

After recommendations, report whether the chosen installed desktop app appears to support playlist creation and adding tracks. Treat this as status reporting only: do not create a playlist or add tracks during the initial recommendation response. Leave the recommendation list visible for the user to review, then create or add only after the user explicitly agrees in a follow-up. If their intent is unclear, ask whether to add all recommendations or only selected tracks. Prefer computer-use in the selected desktop app. If playlist creation, search, or adding tracks is unavailable or ambiguous, do not force it; report the limitation and provide the recommendation list.

## Spotify

Access order:

1. Spotify Desktop through computer-use automation with the user's existing login.
2. Already-authorized Spotify connector/API if one is installed and usable without asking the user for API credentials.
3. Spotify account export, playlist URLs, CSV/JSON, pasted data, or user-created API credentials only as a fallback.

Prioritize:

1. Saved/liked tracks
2. User playlists and followed playlists
3. Saved albums
4. Followed artists
5. Recently played tracks
6. Top tracks and top artists by time range

Useful fields: track name, artist names, album, ISRC, Spotify URI/URL, release date, duration, popularity, explicit flag, playlist memberships, saved timestamp, artist genres, album label, and audio descriptors if available.

If audio features are not available, infer from artist genres, playlist context, release metadata, tags, already-authorized connectors, user-provided files, and ordinary web search over public music sources. Do not use browser or Chrome automation for account access.

When using the desktop app, navigate to library sections rather than asking the user to export. Scroll long lists, open playlists as needed, and extract visible track/artist/album rows. Capture enough rows for a representative analysis when full extraction is impractical, and say what was sampled.

For confirmed playlist creation after recommendations, use Spotify Desktop controls only when visible and reliable: create a new playlist, name it, search each agreed recommendation by artist-title, verify the match, then add to that playlist. Skip ambiguous search results. Do not use Spotify Web Player.

## Apple Music

Use Music.app or the Apple Music desktop app when installed. Prioritize library songs, playlists, favorites, play counts if visible, loved/disliked status, recently played, Replay surfaces, radio stations, and catalog metadata. Apple metadata may be stronger for library organization and weaker for public audio descriptors. Normalize loved/favorite/library-added states distinctly rather than mapping everything to Spotify-style "liked".

For confirmed playlist creation after recommendations, use Music.app or Apple Music desktop controls only when a new playlist and add-to-playlist flow is visible and reliable. Apple may require catalog/library availability for adding tracks; skip tracks that cannot be confidently found or added.

## Amazon Music

Use the Amazon Music desktop app when installed. Prioritize Library, My Music, Liked/Favorited songs, Followed artists, Playlists, Albums, Recently Played, Stations, My Soundtrack/My Discovery Mix-style surfaces, and purchased/imported music if visible. Amazon UI labels can vary by region and subscription tier, so record the exact surface sampled. If full track metadata is not visible, capture visible title, artist, album/playlist/station context, duration when available, and whether the item is liked/favorited/in library.

For confirmed playlist creation after recommendations, use Amazon Music desktop controls only when Create Playlist and add controls are available in the current account/app state. Amazon Music UI varies by plan and region; if the flow is unavailable or results are ambiguous, skip creation and report the limitation.

## YouTube Music

Use a standalone downloaded app only if it can be controlled without Chrome or browser automation. Use liked songs, playlists, uploads, library albums, history, and channel/artist metadata. Normalize official videos, audio tracks, remasters, and live sessions carefully; dedupe by artist-title plus duration when ISRC is absent.

## TIDAL / Deezer / SoundCloud / Other Desktop Clients

Use the installed desktop client when present and authorized. Prefer favorites/liked tracks, collections/library, playlists, albums, followed artists, listening history, stations/mixes, and recommendation pages. Preserve platform-specific terms and confidence notes, especially when a service exposes partial metadata or user-generated uploads.

For confirmed playlist creation after recommendations, apply the same rule: create and add through the installed client only when the controls are clear and reliable; otherwise provide the recommendations without modifying the account.

## Last.fm / ListenBrainz

Use scrobbles, loved tracks, top artists, top albums, top tracks, tags, and time-window charts. These sources are especially useful for weighting actual listening behavior rather than saved-library intent.

## MusicBrainz / AcousticBrainz / Discogs

Use as enrichment sources for canonical artist names, aliases, releases, labels, countries, genres, dates, and identifiers. Treat genre tags as noisy evidence, not truth.

## Files And Exports

Use files and exports only after installed-app automation and already-authorized connector access are unavailable, blocked, or declined. Accept CSV, JSON, TXT, playlist URLs, Spotify export files, Apple Music exports, Amazon Music exports, Last.fm exports, and manually pasted lists. Normalize everything into a list of track-like records with:

```json
{
  "title": "Song title",
  "artists": ["Artist"],
  "album": "Album",
  "isrc": "OPTIONAL",
  "url": "OPTIONAL",
  "source_platform": "spotify|apple_music|amazon_music|youtube_music|lastfm|other",
  "playlists": ["OPTIONAL"]
}
```

When app-collected data is sparse, first try another in-app surface such as liked songs, top tracks, recently played, or a favorite playlist before asking the user for files.
