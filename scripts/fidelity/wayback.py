# scripts/fidelity/wayback.py
"""Resolve the best Wayback Machine snapshot for an original URL via the
Availability API. Network is injected for testability."""
from __future__ import annotations
import json
import urllib.parse
import urllib.request

_AVAIL = "http://archive.org/wayback/available"

def parse_availability(payload: dict | None) -> str | None:
    snap = ((payload or {}).get("archived_snapshots") or {}).get("closest") or {}
    if snap.get("available") and snap.get("url"):
        return snap["url"]
    return None

def snapshot_url(original_url: str, timestamp: str = "", *,
                 opener=urllib.request.urlopen) -> str | None:
    q = {"url": original_url}
    if timestamp:
        q["timestamp"] = timestamp
    url = f"{_AVAIL}?{urllib.parse.urlencode(q)}"
    with opener(url, timeout=30) as r:
        return parse_availability(json.loads(r.read().decode("utf-8")))
