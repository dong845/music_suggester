# Recommendation Method

## Build The Taste Profile

Separate evidence into signal groups:

- Strong positive: liked tracks, repeated scrobbles, saved albums, user-made playlists, loved tracks.
- Medium positive: followed playlists, followed artists, recent plays, search/play history.
- Weak positive: tracks in broad imported playlists, algorithmic playlists, one-off listens.
- Negative or uncertain: removed tracks, explicit dislikes, skipped tracks, stale recommendations ignored by the user.

Analyze across:

- Artist affinity: repeated artists, side projects, collaborators, labels, scenes, regions.
- Genre and tags: platform genres, Last.fm tags, playlist names, MusicBrainz/Discogs metadata.
- Sound and production: energy, tempo, danceability, acousticness, electronic texture, vocal style, instrumentation, mood.
- Era and geography: release decades, regional scenes, languages, local vs international tilt.
- Discovery posture: mainstream vs niche, deep-cut tolerance, album orientation, singles orientation.
- Current-session intent: mood/atmosphere, language preference, era/time age, artist/singer focus, listening context, desired recommendation count, and whether the user wants safe or exploratory recommendations, only when the user already stated it.

Keep long-term taste and current-session intent separate. Long-term taste predicts what the user usually likes; stated current intent tells what they want now, including how many songs they requested. Do not ask for a current brief before recommending. When no current intent is stated, rank for balanced long-term fit and use the default recommendation count. When taste and stated intent diverge, include a small number of intent-matching picks and label the tradeoff clearly.

If there is no usable library evidence, do not invent a taste profile. Build from the user's stated mood, language, era, focus, and discovery posture when provided. If no intent was provided, recommend a broad lower-confidence starter set based on common listener choices.

If usable library evidence exists, provide the taste analysis before the recommendation list. Cover the evidence from multiple aspects: dominant genres/scenes, recurring artists and artist archetypes, mood and sound profile, tempo/energy, language/region distribution, era distribution, mainstream vs niche posture, and how any user-stated intent changes candidate ranking.

## Candidate Generation

Use several sources so recommendations are not one-note:

1. Neighbor artists and tracks from platform recommendation/search tools.
2. Similar tags and microgenres from Last.fm, ListenBrainz, MusicBrainz, Discogs metadata, ordinary web research, or already-authorized music connectors.
3. Collaborators, producers, labels, remixers, and scene-adjacent artists.
4. Deep cuts from artists the user likes but has not saved.
5. Newer releases matching established taste axes.
6. Cross-era analogs: older roots of current favorites or newer artists carrying older traits.

## Ranking

Score candidates with a simple transparent rubric:

- Fit: overlaps with multiple strong taste axes.
- Intent match: satisfies the user's stated current mood, language, era/time age, singer focus, listening context, or requested recommendation count when provided.
- Novelty: not in library, not previously recommended, not too obvious.
- Diversity: avoids returning the same artist, genre, decade, or mood repeatedly.
- Confidence: backed by strong user evidence or multiple independent signals.
- Explainability: can be justified in one sentence without hand-waving.

Default list composition:

- 45 percent close fits from long-term taste
- 30 percent adjacent discoveries
- 15 percent deep cuts or exploratory picks
- 10 percent fresh/publicly researched picks matching established taste axes

Adjust only when the user already asks for adventurous, mainstream, obscure, new releases, specific moods, workout music, study music, or another listening context.

Use the user's requested song count as the target final list size when provided. Otherwise default to 10-20 recommendations. If the requested count is too large for the available evidence or playlist-add workflow, provide a clearly labeled first batch and state the cap or reason.

For empty-library runs, use this composition instead:

- 60 percent direct intent matches
- 25 percent common listener choices for the requested genre/language/era/mood, such as widely liked tracks, canon artists, popular playlist staples, or critically recognized entry points
- 15 percent exploratory picks

## Output Rules

Always dedupe against:

1. Current library snapshot
2. Previous recommendation ledger
3. Current response list

For each recommendation include:

- Artist
- Track/album/playlist name
- Type
- Why it fits
- Which signals it uses: long-term taste if available, current mood, language/region, era/time age, artist focus, discovery posture
- If no current intent was provided, say recommendations are ranked for balanced taste-profile fit; do not ask follow-up preference questions before listing them.
- Link if available, otherwise a search phrase

Immediately after `Taste analysis` and before the recommendation sections, include `Questions to refine the next list`. If there is no usable library evidence and no `Taste analysis` section, place these questions after the lower-confidence evidence note and before the starter recommendations. These are optional follow-up questions for the user to answer while still receiving the current recommendations in the same response, not prerequisites for the current run. Cover only questions that would materially change the next batch, such as:

- Which music type or genre should the next list emphasize or avoid?
- Which era or time age should it target?
- Which country, region, or language should it focus on?
- How many songs should the next recommendation list include?
- Is there a mood, use case, or energy level for the next list?
- Should it focus on, resemble, or avoid any specific musician?
- Should the next list be safer, more obscure, newer, older, or more exploratory?

After the recommendation sections, include `Playlist availability`. Check or infer whether the chosen installed desktop app exposes reliable playlist creation and add-to-playlist controls, but treat this as status reporting only. Do not create a playlist or add tracks during the initial recommendation response. Leave the recommendation list visible so the user can decide which tracks, if any, should be added to a playlist or song list. End the initial recommendation response with `Playlist action?`: ask whether the user wants Codex to add the recommendations with computer-use, and ask them to choose an existing playlist or a new playlist.

If the user later confirms playlist creation or adding, create or modify the playlist only after the final deduped recommendation list is known and only through an installed desktop app with reliable controls. If the user says to add all recommendations, add the full deduped list. If their intent is unclear, ask only the missing target or selection question: existing vs new playlist, target playlist name, or all vs selected items. The final response should still include the recommendation rationale, plus playlist status: supported but awaiting user selection, created, unavailable, or partially completed with skipped items.

Mention changes since the last analysis when the cache fingerprint changed.

For non-empty-library runs, the final answer should make the taste model visible before the list; do not only output songs. For empty-library runs, explicitly say that the list is based on common preferences rather than personal listening history.
