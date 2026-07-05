#!/usr/bin/env python3
"""Cache, fingerprint, diff, and dedupe helpers for the music-suggester skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\(\[].*?[\)\]]", " ", text)
    text = re.sub(r"\b(remaster(ed)?|explicit|clean|mono|stereo|radio edit|single version)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def find_items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if not isinstance(value, dict):
        return []
    for key in ("tracks", "items", "songs", "recommendations", "library"):
        items = value.get(key)
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    return []


def artists_for(item: dict[str, Any]) -> list[str]:
    artists = item.get("artists") or item.get("artist_names") or item.get("artist")
    if isinstance(artists, str):
        return [part.strip() for part in re.split(r",|&|\bfeat\.?\b", artists) if part.strip()]
    if isinstance(artists, list):
        names: list[str] = []
        for artist in artists:
            if isinstance(artist, str):
                names.append(artist)
            elif isinstance(artist, dict):
                name = artist.get("name")
                if name:
                    names.append(str(name))
        return names
    return []


def title_for(item: dict[str, Any]) -> str:
    return str(item.get("title") or item.get("name") or item.get("track") or "").strip()


def item_keys(item: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    isrc = str(item.get("isrc") or item.get("ISRC") or "").strip().upper()
    if isrc:
        keys.add(f"isrc:{isrc}")
    title = slug(title_for(item))
    artists = [slug(artist) for artist in artists_for(item)]
    artists = [artist for artist in artists if artist]
    if title and artists:
        keys.add(f"track:{'|'.join(sorted(artists))}:{title}")
    url = str(item.get("url") or item.get("uri") or "").strip()
    if url:
        keys.add(f"url:{url}")
    return keys


def canonical_items(value: Any) -> list[dict[str, Any]]:
    canonical: list[dict[str, Any]] = []
    for item in find_items(value):
        keys = sorted(item_keys(item))
        if not keys:
            continue
        canonical.append(
            {
                "keys": keys,
                "title": title_for(item),
                "artists": artists_for(item),
                "album": item.get("album") or item.get("album_name"),
                "source": item.get("source") or item.get("platform"),
            }
        )
    canonical.sort(key=lambda row: row["keys"][0])
    return canonical


def playlist_names(value: Any) -> list[str]:
    playlists = []
    if isinstance(value, dict):
        raw_playlists = value.get("playlists")
        if isinstance(raw_playlists, list):
            for playlist in raw_playlists:
                if isinstance(playlist, str):
                    playlists.append(playlist)
                elif isinstance(playlist, dict) and playlist.get("name"):
                    playlists.append(str(playlist["name"]))
    return sorted(slug(name) for name in playlists if slug(name))


def fingerprint(value: Any) -> dict[str, Any]:
    items = canonical_items(value)
    playlists = playlist_names(value)
    payload = json.dumps(
        {"items": items, "playlists": playlists},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return {
        "fingerprint": digest,
        "track_count": len(items),
        "playlist_count": len(playlists),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def diff_snapshots(old_value: Any, new_value: Any) -> dict[str, Any]:
    old_items = [item for item in find_items(old_value) if item_keys(item)]
    new_items = [item for item in find_items(new_value) if item_keys(item)]
    old_keys = set().union(*(item_keys(item) for item in old_items)) if old_items else set()
    new_keys = set().union(*(item_keys(item) for item in new_items)) if new_items else set()
    added = [
        {"title": title_for(item), "artists": artists_for(item), "keys": sorted(item_keys(item))}
        for item in new_items
        if not item_keys(item) & old_keys
    ]
    removed = [
        {"title": title_for(item), "artists": artists_for(item), "keys": sorted(item_keys(item))}
        for item in old_items
        if not item_keys(item) & new_keys
    ]
    return {
        "old": fingerprint(old_value),
        "new": fingerprint(new_value),
        "added": added,
        "removed": removed,
    }


def dedupe(candidates: Any, libraries: list[Any]) -> list[dict[str, Any]]:
    blocked: set[str] = set()
    for library in libraries:
        for item in find_items(library):
            blocked.update(item_keys(item))

    seen: set[str] = set()
    kept: list[dict[str, Any]] = []
    for item in find_items(candidates):
        keys = item_keys(item)
        if not keys:
            continue
        if keys & blocked or keys & seen:
            continue
        seen.update(keys)
        kept.append(item)
    return kept


def default_cache_dir(agent: str | None) -> Path:
    if agent == "claude" or (agent is None and os.environ.get("CLAUDE_CONFIG_DIR")):
        base = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    else:
        base = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return base / "data" / "music-suggester"


def main() -> int:
    parser = argparse.ArgumentParser(description="Music profile cache helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    cache_parser = sub.add_parser("cache-dir", help="Print the recommended cache directory")
    cache_parser.add_argument("--agent", choices=["codex", "claude"], default=None)

    fp_parser = sub.add_parser("fingerprint", help="Fingerprint a normalized snapshot JSON file")
    fp_parser.add_argument("snapshot")

    diff_parser = sub.add_parser("diff", help="Diff old and new normalized snapshot JSON files")
    diff_parser.add_argument("old_snapshot")
    diff_parser.add_argument("new_snapshot")

    dedupe_parser = sub.add_parser("dedupe", help="Remove candidates already in library or ledger JSON files")
    dedupe_parser.add_argument("candidates")
    dedupe_parser.add_argument("--library", action="append", default=[])
    dedupe_parser.add_argument("--ledger", action="append", default=[])

    args = parser.parse_args()

    if args.command == "cache-dir":
        print(default_cache_dir(args.agent).expanduser())
    elif args.command == "fingerprint":
        dump_json(fingerprint(load_json(args.snapshot)))
    elif args.command == "diff":
        dump_json(diff_snapshots(load_json(args.old_snapshot), load_json(args.new_snapshot)))
    elif args.command == "dedupe":
        libraries = [load_json(path) for path in args.library + args.ledger]
        dump_json({"recommendations": dedupe(load_json(args.candidates), libraries)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
