---
name: music-suggester
description: Access installed desktop music apps such as Spotify, Apple Music/Music.app, Amazon Music, YouTube Music desktop apps, TIDAL, Deezer, SoundCloud, or other downloaded clients through desktop automation, existing app sessions, or authorized connectors to analyze listening history and recommend music without asking for API keys, tokens, exports, or files up front. Never use Chrome, browser control, web players, or web music apps to access the user's account or private library; ordinary web search is allowed for public music research. Use for personalized recommendations, taste analysis, playlist discovery, optional creation of a recommendation playlist in the installed app when requested and available, or reusable recommendation history.
---

# Music Suggester

## Overview

Build recommendations from evidence, not vibes alone. Enter the user's authorized installed music app or connected music account, collect music-library data, derive a durable taste profile, compare it with any previous profile, then recommend items that are novel, explainable, and deduplicated. Do not stop to ask preference-brief questions before recommending; use any intention, mood, language, era, artist, or discovery constraints the user already provided, otherwise infer a balanced recommendation set from the taste profile. After the taste analysis, include a short non-blocking set of questions the user can answer to refine the next list, such as music type, era/time age, country or language, and specific musicians; then continue directly into recommendations without waiting for answers. After recommendations, check whether the chosen desktop app appears to support playlist creation and adding tracks, report that availability, and leave the recommended list visible for the user to review. Create a playlist or add recommendations only after the user explicitly agrees in a follow-up; do not add tracks during the initial recommendation response. Keep the workflow platform-neutral: Spotify, Apple Music, Amazon Music, YouTube Music desktop apps, TIDAL, Deezer, SoundCloud, and other downloaded music clients are valid sources when installed and authorized.

Default to automatic installed-app access. Use desktop app control through computer-use, existing authenticated desktop-app sessions, or already-installed connectors. Do not use Chrome, browser control, web players, or web music apps to access the user's music account, even if they appear available; this skill treats browser automation as unsafe for account/library access. Ordinary web search is allowed for public music research, metadata enrichment, release recency, genre context, and candidate discovery. Do not ask the user to create an API app, paste API keys, provide tokens, or export files up front. Treat API setup and user-provided exports as last-resort fallbacks after desktop-app automation and already-authorized connectors are unavailable, blocked, or explicitly declined.

## Workflow

1. Identify automatic access paths.
   - If the user names a platform, use that installed desktop app first when available.
   - If the user does not name a platform, inspect available downloaded music apps and recent app usage, then choose the richest accessible source. Do not assume Spotify just because it is common.
   - Prefer opening or attaching to an installed desktop app such as Spotify Desktop, Apple Music/Music.app, Amazon Music, YouTube Music as a standalone installed app only if it can be controlled without Chrome, TIDAL, Deezer, SoundCloud, Last.fm desktop tooling, or another named downloaded music app using the user's existing logged-in session.
   - Use computer-use tools to navigate the installed app and inspect library pages directly.
   - Never use Chrome, browser plugins, in-app browser control, web players, or music websites to access the user's account or private library for this skill. If only a web-player path exists, skip it and use connectors or file/export fallback instead.
   - Use ordinary web search when it improves recommendations with public facts, current releases, artist/genre context, or metadata. Do not put private playlist contents or sensitive listening details into search queries unless the user explicitly asks for that level of research.
   - Use already-installed connectors or MCP tools when they are present and already authorized; do not require the user to create developer apps, provide API credentials, or paste tokens.
   - If the first-choice app is unavailable, inspect available downloaded apps/plugins/connectors for Spotify Desktop, Apple Music/Music.app, Amazon Music, YouTube Music installed app, TIDAL, Deezer, SoundCloud, Last.fm, ListenBrainz, MusicBrainz, or generic desktop-app automation.
   - In Claude Code, use MCP/plugin discovery and computer-use automation if present; fall back to local files or user-provided URLs only when installed-app or connector access is not possible.
   - Ask only for permission to open/control an app or for the user to complete login/OAuth/MFA in the app UI when required.

2. Capture stated recommendation intent without asking an interview.
   - Do not ask mood/language/era/focus questions before listing recommendations.
   - If the user already provided constraints such as mood, language, region, era, artist focus, singer type, discovery posture, use case, or platform, treat them as current-session intent.
   - If the user gave no current-session intent, proceed with a balanced default: combine closest fits, adjacent discoveries, deep cuts, and a small number of fresh/publicly researched picks.
   - Only ask a clarifying question when the request is impossible or risky without it, such as an unnamed app that cannot be identified, blocked login, or a destructive/permission-changing action. Do not ask preference questions merely to improve ranking.
   - Treat any stated intent as temporary session intent, not a replacement for library evidence.

3. Load historical state before fetching new data.
   - Use `scripts/music_profile_cache.py` for cache paths, fingerprinting, diffing, and dedupe helpers.
   - Store per-user state outside the skill folder. Prefer `${CODEX_HOME:-~/.codex}/data/music-suggester/`; in Claude Code prefer `${CLAUDE_CONFIG_DIR:-~/.claude}/data/music-suggester/`; otherwise use a project-local `.music-suggester/` only with user approval.
   - Keep snapshots labeled by platform and account label when visible, so Spotify, Apple Music, Amazon Music, and other app profiles do not overwrite each other. When multiple sources are available, merge them only after preserving the source platform for each item.
   - Never store OAuth tokens, raw cookies, or secrets in the cache.

4. Enter the app and collect or refresh library evidence.
   - Open or attach to the relevant downloaded music app: Spotify Desktop, Apple Music/Music.app, Amazon Music, YouTube Music installed app, TIDAL, Deezer, SoundCloud, Last.fm desktop tooling, or another installed platform the user names.
   - Use the user's logged-in session when available. If login, OAuth consent, MFA, captcha, or payment/account prompts appear, pause and ask the user to complete that step in the app UI; do not ask for passwords, API keys, secrets, tokens, or cookies.
   - Navigate library surfaces directly using the app's native terminology: liked songs, loved songs, favorites, library songs, saved playlists, owned playlists, saved albums, followed artists, stations, recently played, listening history, top tracks, top artists, and recommendation pages.
   - Scroll and paginate until the useful library scope is captured or until platform limits make continuation unreasonable. Record any limits in the analysis.
   - Fetch the broadest authorized set: liked/saved tracks, saved albums, saved playlists, owned playlists, recently played tracks, and platform top tracks/artists when available.
   - For each track, normalize at least: title, artist names, album, ISRC if available, platform URI/URL or search phrase, release year, duration, popularity/playcount if available, source platform, playlist/station names, saved/liked/loved/favorited flags, and audio descriptors if available.
   - Build an "already owned or already present" exclusion set from liked songs, loved/favorited songs, library songs, saved tracks, saved albums where track lists are visible, owned playlists, saved playlists, and any user playlist inspected during the run. Use this exclusion set before recommendations are shown and before any playlist creation/add step.
   - When platform audio features are unavailable, infer descriptors from metadata and tags using Last.fm, MusicBrainz, playlist context, genres, artist metadata, already-authorized connectors, user-provided files, or ordinary web search over public music sources.
   - Treat all music-library and playlist inspection as read-only unless a later playlist-creation step is explicitly requested. Never remove, delete, hide, unlike, unfollow, reorder, rename, overwrite, or clean up existing user content while collecting evidence.
   - If the selected platform, playlist, account, or app surface is empty, inaccessible after reasonable attempts, or has too little usable history, do not stop. Say that the run has no personal-library reference, use any user-provided constraints plus common listener choices, or a broad starter set when no constraints were provided, and mark the recommendations as lower-confidence and less personalized.

5. Decide whether to reuse analysis.
   - Compute a stable fingerprint from normalized library items and metadata counts.
   - If the fingerprint matches the previous snapshot, reuse the saved taste profile and only generate fresh recommendations.
   - If it changed, produce a concise diff first: new liked tracks, removed tracks, new playlists, newly dominant artists/genres/moods, and notable changes in era or language.

6. Analyze taste across multiple axes.
   - Artists: recurring artists, related scenes, collaborations, labels, regions, and artist eras.
   - Genres and microgenres: both explicit platform genres and inferred tags.
   - Sound: tempo, energy, danceability, acoustic/electronic balance, vocal/instrumental balance, texture, production style, and mood.
   - Listening context: playlists, liked vs saved albums, recency, repeats, long-tail tracks, mainstream vs niche, languages, decades, and seasonality.
   - Current intent: any mood/atmosphere, language/region, era/time age, singer/artist focus, discovery posture, and use case explicitly provided by the user. If none was provided, say that ranking uses balanced taste-profile fit.
   - Negative space: overrepresented artists already known, genres with low affinity, skipped or removed items if that evidence exists.
   - If there is no usable library evidence, skip durable taste claims and build from any user-provided constraints. If no constraints were provided, use a broad starter set based on common listener choices and clearly mark it lower-confidence.
   - If usable library evidence exists, present a concise but detailed taste analysis before recommendations. Cover at least: dominant genres/scenes, recurring artists or artist types, mood/sound profile, language/region pattern, era pattern, discovery posture, and any user-provided constraints that changed ranking.

7. Recommend with dedupe and explanation.
   - Exclude anything already in the user's library, liked songs, loved/favorited songs, saved tracks, visible saved album tracks, owned playlists, saved playlists, or any inspected user playlist. This means a song already present in `Liked Songs` or another user playlist must not be recommended again.
   - Also exclude anything previously recommended or too close to repeated past misses.
   - Deduplicate and exclude by ISRC first, then normalized artist-title key. When exact IDs are unavailable, compare normalized title, primary artist, featured artists, duration when visible, album, and obvious translated/romanized title variants.
   - If the app cannot expose liked songs or playlist contents after reasonable attempts, say that dedupe against that surface is incomplete and be conservative with obvious repeats.
   - Mix recommendation types unless the user asks otherwise: high-confidence songs, adjacent discoveries, deeper cuts from liked artists, unfamiliar artists, albums/EPs, and playlist seeds.
   - Balance long-term taste and any user-provided current preference. Favor candidates that satisfy both; when they conflict, include a short note such as "temporary mood pick" or "profile-faithful pick outside the stated mood." If no current preference was provided, rank for balanced fit across the taste profile.
   - When no library evidence is available, still provide a useful starter set from any user-provided constraints. If no constraints were provided, base it on common listener choices across broadly popular genres and clearly label it as lower-confidence and not personalized.
   - For each recommendation, give a short "why this fits" note tied to observed taste axes.
   - Include platform links when tools provide them for the selected app; otherwise include search-ready artist and title strings. Do not force Spotify links when the source app is Apple Music, Amazon Music, or another platform.

8. Offer optional refinement questions.
   - Immediately after `Taste analysis`, include a section named `Questions to refine the next list`, then continue to the recommendation sections in the same response.
   - Do not wait for answers before giving recommendations; these questions are visible steering options for the next list, not a blocking interview for the current one.
   - Ask concise, optional questions that would materially change the next recommendation round: preferred music type/genre, era or time age, country/region/language, mood/use case, discovery level, and whether to focus on or avoid specific musicians.
   - Tailor the questions to uncertainty in the taste profile. Avoid generic questionnaires when the user's prior request already answered a point.
   - If the user answers any refinement questions, treat those answers as current-session intent for the next run, not as permanent taste unless they recur.

9. Check playlist availability and create only after consent.
   - After the recommendation sections, inspect or infer whether the chosen installed desktop app exposes reliable playlist creation and add-to-playlist controls. Do this as a capability/status check; do not create or modify anything during this check.
   - Include a `Playlist availability` status in the response: supported, unavailable, ambiguous, subscription/login blocked, or not checked, plus a short reason.
   - Leave the recommended list in the response for user review so the user can decide which tracks, if any, they want added to a playlist or song list.
   - Use playlist creation/addition only when the user explicitly requested it after seeing the recommendation list, or when the user confirms after the `Playlist availability` status. Creating or modifying playlists changes the user's music account, so do not do it silently.
   - Use computer-use in the selected installed desktop app. Do not use Chrome, browser control, web players, or web music apps for playlist creation.
   - First verify that the app exposes reliable playlist creation controls. If creation is missing, ambiguous, subscription-blocked, or too unreliable, do not create the playlist; say playlist creation is not available in the current app state and provide the recommendation list/status for manual review.
   - Treat playlist changes as additive only. Never delete, remove, replace, reorder, rename, overwrite, deduplicate, or clean up any existing playlist content unless the user explicitly asks for that exact destructive action. If a duplicate or wrong item is added by accident, report it clearly and ask before removing it.
   - Prefer a user-provided playlist name. Otherwise use a concise dated name such as `Codex Recommendations YYYY-MM-DD` or a platform-native equivalent.
   - If the user confirms adding recommendations, ask whether to add all recommendations or only selected items when their intent is unclear. If the user says to add all, add only the final deduped recommendation set after checking it against liked songs, saved tracks, owned playlists, saved playlists, and the target playlist contents visible in the app. Search by artist-title, verify the matched track/album when possible, skip uncertain matches rather than adding the wrong item or an existing library item, and report skipped/ambiguous items.
   - If add-to-playlist controls are unavailable, ambiguous, or unstable, stop adding. Leave the playlist as created or leave the recommendation list/status in the response so the user can play or add items manually.
   - Do not play music, follow artists, like songs, remove songs, delete items, rename existing playlists, change privacy settings, or share the playlist unless the user explicitly asks.
   - After creation, report the playlist name, source app, number of items added if any, skipped items, whether adding was stopped or not attempted, and any limits encountered.

10. Save state.
   - Save the latest normalized snapshot fingerprint, profile summary, recommendation ledger, and timestamp.
   - Save any user-provided current-session intent with the run summary, but do not treat it as permanent taste unless it recurs across sessions.
   - For empty-library runs, save the source state as `no_usable_library_evidence` and preserve only any user-provided current-session intent plus recommendation ledger.
   - Append new recommendations to the ledger immediately after presenting them so future runs avoid repeats.
   - If a playlist was created, save the playlist name, source platform, creation date, added recommendations, skipped recommendations, and whether the playlist link/URI was visible. Do not store secrets, cookies, or private account tokens.

## Recommendation Shape

Default to 10-20 recommendations unless the user asks for a different size. Use compact sections:

- `Closest fits`: safest picks from strong taste signals.
- `Adjacent discoveries`: similar enough to land, different enough to be useful.
- `Deep cuts`: less obvious tracks, underrated catalog items, or niche scenes.
- `Current mood picks`: use only when the user already asked for a specific atmosphere, language, singer, or listening context.
- `No-library starter set`: use when there is no usable platform history; be explicit that confidence is lower.
- `Taste analysis`: required when usable library evidence exists; summarize multiple taste axes before listing recommendations.
- `Playlist availability`: required after recommendation sections; report whether the chosen desktop app appears to support playlist creation and adding recommendations, but do not modify the account unless the user confirms.
- `Playlist created`: use only when a requested playlist was actually created in the installed app; include app, playlist name, count added if any, skipped items, and whether adding was stopped or left for the user.
- `Why these`: a brief synthesis of the recommendation logic and what changed since last run.
- `Questions to refine the next list`: required immediately after `Taste analysis` and before recommendation sections; ask optional follow-up questions about music type/genre, era/time age, country/region/language, mood/use case, discovery level, and specific musicians to focus on or avoid.

When evidence is thin or empty, say so and ask for one additional source only after giving a small starter set.

## Intent Handling

Do not ask a preference brief before recommending. Extract intent only from the user's request, such as "Japanese R&B", "workout", "new releases", "female vocals", "similar to X", "avoid Y", or "more obscure". If no intent is stated, proceed with balanced recommendations from the taste profile and mention that no extra preference constraints were provided. After the taste analysis, list optional refinement questions so the user can steer the next list, then give recommendations in the same response without waiting.

## Platform Notes

Read `references/platforms.md` when choosing a data source or fallback path.

Read `references/recommendation-method.md` when building the profile, ranking candidates, or explaining recommendations.

Use `scripts/music_profile_cache.py --help` for deterministic cache, fingerprint, diff, and dedupe operations.

## Privacy And Consent

Use the user's existing authenticated downloaded app/session when authorized by the task. Ask before connecting a new account, installing a connector, granting OAuth scopes, opening or controlling a desktop app, creating or modifying a playlist when the user has not already requested it, or sending private listening history to third-party services. Never use broad browser automation, Chrome automation, in-app browser control, web players, or music websites to access the user's account or private library. Ordinary web search is allowed for public music research; keep queries at the artist, genre, release, or aggregate taste level unless the user asks for detailed research over private library contents. Do not ask for passwords, API keys, raw cookies, tokens, or developer credentials. Do not expose raw private playlist contents unnecessarily in the final answer. Summarize sensitive listening data at the taste-profile level unless the user asks for detailed tables.
