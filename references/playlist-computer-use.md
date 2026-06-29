# Playlist Computer-Use Protocol

Use this reference before modifying a playlist through a downloaded desktop music app. The goal is to make playlist creation and song adding fast enough while preventing wrong additions, duplicates, playback, or accidental edits.

## Core Rules

- Use only the installed desktop app or already-authorized non-browser connector. Never use Chrome, browser control, web players, or web music apps.
- Prefer an already-authorized, platform-specific connector/API for playlist creation and bulk add when it is available without asking the user for credentials. It is faster and more reliable than UI automation. Still verify the final playlist contents through the desktop app when practical.
- Treat playlist operations as additive transactions. Never delete, remove, reorder, rename existing playlists, unlike, unfollow, or clean up existing content unless the user explicitly asks for that exact action.
- Do not press Play-like controls. Avoid result titles, artwork, row bodies, or focused buttons that might trigger playback.
- Prefer accessibility element actions over coordinates. Use coordinate clicks only when the element is visible, stable, and no semantic accessibility action exists.
- Keep a per-run `attempted`, `added`, `skipped`, and `pending_user_decision` list. Add a song at most once per run.
- Stop immediately if a wrong track or duplicate is added. Report it and ask before removing anything.
- Do not use parallel subagents or parallel UI automation to modify the same desktop music app. Parallel work is allowed for public metadata lookup or candidate matching only; a single controller must perform playlist mutations in order.

## Fast, Stable Add Loop

Before the loop:

1. Freeze the final agreed track list. Normalize each item by lowercase title, primary artist, featured artists, and obvious punctuation variants.
2. Freeze the playlist target before mutating anything: user-selected existing playlist, or a new playlist with a confirmed/default name. If the target is missing or ambiguous, ask before continuing.
3. If a safe connector/API route exists and is allowed by the current user request, resolve all track IDs first, preview the matched artist/title list, perform one bulk add call when supported, then verify the playlist count and contents. Do not fall back to UI per-track adding unless the connector/API route is unavailable or ambiguous.
4. If UI automation is required, choose exactly one add surface before mutating anything. Close or ignore all other visible add/search panels. Never mix buttons, search fields, or accessibility IDs from multiple add surfaces in one run.
5. Run a preflight stability test on the chosen surface before adding the agreed list:
   - Search one known target or harmless candidate.
   - Verify the search field value and result table both reflect the same query.
   - Verify the intended row has one row-local `Add` control that can be tied to that row.
   - If the search value, result table, or row-local Add mapping is stale or ambiguous, do not start bulk UI adding.
6. Inspect the target playlist contents currently visible. Build `target_playlist_seen` from visible title/artist rows and the intended additions already present.
7. If a recommended track is already in the target playlist, liked songs, or another inspected user playlist, skip it and record the reason.
8. Confirm the app is showing the intended target playlist and its current visible song count or visible row count.

For each track:

1. Check `attempted` and `target_playlist_seen`. If the normalized key is already present, skip instead of searching.
2. Clear stale search state using the safest available control:
   - Prefer setting the playlist search field value to an empty string, then verify the field is empty.
   - If using a clear button, verify the old query and old results disappeared before typing a new query.
   - Never press any `Add` button while clearing or while an old query/result set is still visible.
3. Enter one concise query: `primary artist title` or `title primary artist`. Do not type the same query twice into the same field.
4. Poll the app state a small number of times until the search field value and result table both reflect the current query. If results remain stale, skip the track instead of using stale buttons.
5. Match exactly one candidate row:
   - Require normalized title match and primary artist match.
   - Prefer album/duration/featured-artist agreement when visible.
   - Reject karaoke, instrumental, live, remix, podcast, video, or cover results unless the recommendation explicitly asked for that version.
   - If two plausible catalog versions appear, prefer the single/album version that best matches the displayed recommendation metadata; otherwise skip as ambiguous.
6. Press the `Add` control that belongs to the matched row. Prefer the row-local control. If the app exposes both row-local and column-duplicated controls, use the duplicated column control only after confirming its row order maps to the matched row in the current state snapshot.
7. Verify the transaction before moving on:
   - The playlist count or visible target rows must increase by exactly one.
   - The newly visible row must match the intended title/artist.
   - A search-result button changing to `Remove from playlist` is not sufficient by itself. Treat it as a hint only.
   - If the count does not change, do not retry more than once.
   - If a retry appears to succeed but a fresh target-playlist verification reverts to the old count, mark the item `not_persisted`, stop or skip according to the stop rules, and do not click the same Add button again.
   - If the count changes by more than one, or the visible new row does not match the intended track, stop and report.
8. Add the normalized key to `attempted`, `added`, and `target_playlist_seen`.

Use at most two `get_app_state` checks per normal track after the app has proven stable: one after search, one after add. Add extra checks only when UI state is stale, ambiguous, or changing.

## Cost Control

- Avoid full app-state reads while merely thinking or planning. Use them only at preflight, after search, after add, and after suspected stale UI.
- After two clean transactions on the same surface, keep the normal per-track budget to one state read after search and one after add.
- If the app emits very large accessibility trees, prefer matching from the smallest visible result area and stop early when stale state repeats. Do not spend more tokens trying to force an unstable UI.

## Spotify Desktop Notes

- Use Spotify Desktop only. Do not use Spotify Web Player.
- Spotify can expose both the playlist page's `Let's find something for your playlist` area and the right-side `Add to playlist` panel. Use exactly one. If both are open, close one before searching or adding.
- The playlist page's `Let's find something for your playlist` search field is acceptable, but it can keep stale results. Always verify both the search field value and the `Top` result table before adding.
- The right-side `Add to playlist` panel is acceptable only if its add actions persist after preflight. If a result briefly changes to `Remove from playlist` but the target playlist header count later reverts, treat that surface as unreliable and stop using it for the run.
- Do not use the `Recommended / Based on what's in this playlist` block as a substitute for search results. It may contain valid-looking songs but pressing its Add buttons can duplicate items or add tracks out of the intended order.
- If Spotify shows duplicate `Add to Playlist` controls for the same result table, row order matters. Use the duplicate column control only when the matched row is selected or when the column cell index clearly maps to that row.
- After each add, verify the playlist header count changed by exactly one and that the new row appears in the target playlist table. If the same song appears twice, stop and ask before removing the extra copy.
- If Spotify accessibility IDs become invalid, refresh with `get_app_state` once and retry the same semantic element. If IDs keep changing, skip the track instead of falling back to blind coordinates.
- If Spotify reports `noWindowsAvailable` for coordinate clicks, stop coordinate fallback for the run and continue only with valid accessibility elements.

## When To Stop

Stop adding and report partial progress when:

- Search results are stale for two consecutive tracks.
- Add buttons cannot be tied to a verified row.
- The app focuses an `Add` button from a previous song after the query changes.
- A playlist count changes unexpectedly.
- A track appears to add but does not persist after fresh target-playlist verification.
- Two consecutive add attempts on the chosen surface fail to persist.
- Multiple add/search surfaces are visible and cannot be reduced to one stable surface.
- A duplicate or wrong track is added.
- The app starts playback unexpectedly.

Final status should include playlist name, source app, added tracks, skipped tracks with reasons, and any `pending_user_decision` items.
