# Music Suggester

A Codex skill that recommends music from the desktop music apps you already use.

It looks at authorized installed apps such as Spotify Desktop, Apple Music/Music.app, Amazon Music, TIDAL, Deezer, SoundCloud, and other downloaded players, builds a lightweight taste profile, then suggests songs that are explainable and not already in your visible library or playlists.

No API keys. No browser-player automation. No export files required up front.

## Why Try It

- Personalized recommendations from real listening context: liked songs, playlists, saved albums, artists, and recent plays when visible.
- Works beyond Spotify; the workflow is designed for downloaded desktop music apps in general.
- Recommends first, then asks how you want to refine the next list.
- Avoids obvious repeats by checking liked songs, saved tracks, inspected playlists, and past recommendations.
- Can create or add to a playlist only after you confirm, and only when the desktop app exposes reliable controls.

## Safety Defaults

- Never uses Chrome, browser control, web players, or music websites for private library access.
- Never deletes, removes, reorders, renames, or cleans up existing music content by default.
- Skips ambiguous song matches instead of adding the wrong track.
- Stops playlist automation when the desktop app UI looks unstable.

Ordinary web search is still allowed for public artist, genre, release, and metadata research.

## Example Prompts

```text
$music-suggester
```

```text
$music-suggester
Recommend 10 safer K-R&B songs that are not already in my library.
```

```text
$music-suggester
Give me older J-pop songs from the 90s and 00s, then ask whether I want a playlist.
```

```text
$music-suggester
Find songs that fit my taste and add them to a new playlist if the desktop app supports it.
```

## Install

Clone into your Codex skills directory:

```bash
git clone https://github.com/dong845/music_suggester.git ~/.codex/skills/music-suggester
```

Then run:

```text
$music-suggester
```

## What Is Included

- `SKILL.md`: main workflow.
- `references/platforms.md`: desktop music app guidance.
- `references/recommendation-method.md`: taste profiling and ranking rules.
- `references/playlist-computer-use.md`: safer playlist creation/add protocol.
- `scripts/music_profile_cache.py`: cache, fingerprint, diff, and dedupe helper.

Best experience: use an installed music app that is already logged in. If login, MFA, or consent is needed, the skill should pause and ask you to complete it in the app UI.
