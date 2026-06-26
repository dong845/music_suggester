# Music Suggester

Music Suggester is a Codex skill for personalized music recommendations from the desktop music apps you already use. It is built for people who want better suggestions than generic charts, without setting up developer APIs, exporting library files, or handing over browser sessions.

The skill can inspect authorized installed music clients such as Spotify Desktop, Apple Music/Music.app, Amazon Music, YouTube Music desktop apps, TIDAL, Deezer, SoundCloud, and other downloaded players. It builds a taste profile from visible library evidence, then recommends songs that are explainable, deduplicated, and not already in your liked songs or inspected playlists.

## Why Try It

- Uses your real listening context: liked songs, saved tracks, playlists, albums, artists, recents, and app-specific library surfaces when available.
- Stays desktop-first: it avoids Chrome, browser automation, web players, and web music apps for private account access.
- Does not ask for API keys, cookies, OAuth tokens, or exported files up front.
- Works beyond Spotify: the workflow is platform-neutral and can adapt to Apple Music, Amazon Music, TIDAL, Deezer, SoundCloud, and other installed clients.
- Recommends directly: it does not interview you for mood, genre, or list-size preferences before producing a list.
- Respects requested list sizes: ask for 5, 12, 30, or another count when you want a specific number of songs.
- Avoids repeats: it excludes liked songs, saved/library tracks, visible playlist contents, and previous recommendations.
- Can create a playlist only when explicitly requested and when the desktop app exposes reliable controls.

## Safety Rules

This skill is intentionally conservative around user accounts and libraries:

- No Chrome or browser-player automation for private music libraries.
- No deletion, removal, reordering, renaming, deduping, or cleanup of existing user content unless the user explicitly asks for that exact action.
- Playlist edits are additive only by default.
- If add-to-playlist controls are unstable, it stops and leaves the recommendation list for the user to play or add manually.
- If a match is ambiguous, it skips the item rather than adding the wrong song.

Ordinary web search is still allowed for public music research, release metadata, genre context, and artist discovery.

## Example Prompts

```text
$music-suggester
Analyze my desktop music app and recommend songs I probably do not already know.
```

```text
$music-suggester
Use my installed music app and make a playlist of recommendations if playlist creation is available.
```

```text
$music-suggester
Give me Japanese R&B and city-pop-adjacent recommendations based on my taste.
```

```text
$music-suggester
Recommend 15 older J-pop songs from the 90s and 00s that are not already in my library.
```

```text
$music-suggester
Find newer songs that fit my liked songs, but skip anything already in my playlists.
```

## Install

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/dong845/music_suggester.git ~/.codex/skills/music-suggester
```

Then invoke it in Codex with:

```text
$music-suggester
```

## Repository Contents

- `SKILL.md`: the main skill instructions.
- `references/platforms.md`: platform-specific source and fallback guidance.
- `references/recommendation-method.md`: taste profiling and ranking guidance.
- `scripts/music_profile_cache.py`: helper for cache paths, fingerprints, diffs, and dedupe.
- `agents/openai.yaml`: agent metadata.

## Notes

The skill is designed to work best when a supported desktop music app is installed and already logged in. If the app needs login, MFA, or consent, the skill should pause and ask you to complete that step in the app UI.
