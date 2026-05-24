#!/usr/bin/env python3
# scripts/fidelity/live_oracle_diff.py
"""Exhaustive per-post fidelity diff: built `_site` vs the live WordPress oracle.

This is the tool that found the deltas remediated in P10 (structure), P11
(link/image targets), and the P11-fix (prose text) — gaps that representative
visual sampling missed. It compares EVERY post across four dimensions, so it
catches content/structure regressions a hand-picked screenshot sweep won't.

It is a MANUAL diligence tool, not a CI gate: it needs the live site
(`https://blog.mithis.net`, TLS cert expired → fetched with `curl -sk`) and a
local `_site` build. Re-run after any content/template change.

Four comparison dimensions (per post's entry-content):
  - structure : counts of p/ul/ol/li/img/blockquote/pre/h2-h4 tags
  - targets   : <a href> + <img src> URLs (folds the local image-hosting
                scheme `/assets/images/wp-content/` ↔ live `/wp-content/`)
  - text      : visible prose words (tags stripped, entities + typography +
                whitespace folded)
  - alt       : <img alt> text

Usage:
    # 1. build the site
    bundle3.3 exec jekyll build
    # 2. fetch the live oracle into a cache dir (one curl per post)
    uv run python -m scripts.fidelity.live_oracle_diff --fetch --cache tmp/oracle
    # 3. diff (re-uses the cache; add a dimension filter if desired)
    uv run python -m scripts.fidelity.live_oracle_diff --cache tmp/oracle
    uv run python -m scripts.fidelity.live_oracle_diff --cache tmp/oracle --only text

Exit code is non-zero if any non-noise delta is found, so it can gate a
release check if wired with a curated allowlist of documented WP-artifacts
(see docs/superpowers/plans/P10-RESULTS.md §3 for the 7 accepted artifacts).
"""
from __future__ import annotations

import argparse
import glob
import html as _html
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

LIVE_BASE = "https://blog.mithis.net"
# entry-content ends at the first of these (footer meta / comments / nav)
_END_MARKERS = (
    'class="entry-meta"', 'class="entry-utility"', "class='entry-utility'",
    'id="comments"', 'class="comments', 'class="navigation"', 'id="nav-below"',
)
_STRUCT_TAGS = frozenset(
    {"p", "ul", "ol", "li", "img", "blockquote", "pre", "h2", "h3", "h4"}
)


def entry_content(page_html: str) -> str:
    """Slice from the first entry-content div to the first footer/comments marker."""
    m = re.search(r'class="entry-content"', page_html)
    if not m:
        return ""
    rest = page_html[m.start() + 10:]
    ends = [i for i in (rest.find(x) for x in _END_MARKERS) if i != -1]
    return rest[: min(ends)] if ends else rest


def _norm_url(u: str) -> str:
    if not u:
        return u
    for _ in range(2):  # unwrap nested wayback prefixes first
        u = re.sub(r"^https?://web\.archive\.org/web/\d+\w*/", "", u)
    u = re.sub(r"^https?://blog\.mithis\.net", "", u)
    u = re.sub(r"^https?://mithro\.github\.io", "", u)  # built staging host (absolute_url)
    # Strip the staging baseurl path prefix (baseurl: /blog.mithis.net on the
    # mithro.github.io subpath; empty at the blog.mithis.net production cutover) so a
    # built `/blog.mithis.net/assets/images/wp-content/X` compares equal to live's
    # `/wp-content/X` instead of false-flagging the staging prefix on every asset/link.
    u = re.sub(r"^/blog\.mithis\.net(?=/)", "", u)
    u = u.replace("/assets/images/wp-content/", "/wp-content/")  # local-hosting scheme == live
    return re.sub(r"^http://", "https://", u.rstrip("/"))


def _fold_text(t: str) -> str:
    t = _html.unescape(t)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("\xa0", " "), ("–", "-"),
                 ("—", "-"), ("…", "...")):
        t = t.replace(a, b)
    return t


class _Extractor(HTMLParser):
    """Collect structural tag counts, link/img targets, prose text, and alts."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: Counter[str] = Counter()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.alts: list[str] = []
        self.text_parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        if tag in _STRUCT_TAGS:
            self.tags[tag] += 1
        if tag == "a" and d.get("href"):
            self.hrefs.append(_norm_url(d["href"]))
        if tag == "img":
            if d.get("src"):
                self.srcs.append(_norm_url(d["src"]))
            self.alts.append(_html.unescape((d.get("alt") or "").strip()))

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.text_parts.append(data)

    def words(self) -> Counter[str]:
        folded = _fold_text(" ".join(self.text_parts)).lower()
        return Counter(re.findall(r"[a-z0-9]+", folded))


def _extract(page_html: str) -> _Extractor:
    e = _Extractor()
    try:
        e.feed(entry_content(page_html))
    except Exception:  # noqa: BLE001 - best-effort parse of imperfect WP HTML
        pass
    return e


@dataclass
class PostRef:
    wid: str
    permalink: str


def post_refs(posts_glob: str = "_posts/*.md") -> list[PostRef]:
    refs = []
    for p in sorted(glob.glob(posts_glob)):
        txt = Path(p).read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^permalink:\s*(\S+)", txt, re.M)
        if not m:
            continue
        w = re.search(r"^wordpress_id:\s*(\S+)", txt, re.M)
        refs.append(PostRef(w.group(1) if w else Path(p).stem, m.group(1).strip()))
    return refs


def fetch_live(refs: list[PostRef], cache: Path) -> None:
    cache.mkdir(parents=True, exist_ok=True)
    for r in refs:
        out = cache / f"{r.wid}.html"
        subprocess.run(
            ["curl", "-sk", "--max-time", "30", f"{LIVE_BASE}{r.permalink}", "-o", str(out)],
            check=False,
        )
    n = len(list(cache.glob("*.html")))
    print(f"fetched {n}/{len(refs)} live pages into {cache}")


def _built_path(permalink: str) -> Path:
    p = Path("_site" + permalink + ".html")
    return p if p.exists() else Path("_site" + permalink + "/index.html")


@dataclass
class PostDiff:
    wid: str
    permalink: str
    struct: dict[str, tuple[int, int]] = field(default_factory=dict)
    href_live_only: list[str] = field(default_factory=list)
    href_built_only: list[str] = field(default_factory=list)
    src_live_only: list[str] = field(default_factory=list)
    src_built_only: list[str] = field(default_factory=list)
    text_live_only: Counter[str] = field(default_factory=Counter)
    text_built_only: Counter[str] = field(default_factory=Counter)
    alt_live_only: list[str] = field(default_factory=list)
    alt_built_only: list[str] = field(default_factory=list)

    def has(self, dim: str) -> bool:
        if dim == "structure":
            return bool(self.struct)
        if dim == "targets":
            return bool(self.href_live_only or self.href_built_only
                        or self.src_live_only or self.src_built_only)
        if dim == "text":
            return sum(self.text_live_only.values()) + sum(self.text_built_only.values()) > 1
        if dim == "alt":
            return bool(self.alt_live_only or self.alt_built_only)
        return False


def diff_post(ref: PostRef, cache: Path) -> PostDiff | None:
    bp = _built_path(ref.permalink)
    lp = cache / f"{ref.wid}.html"
    if not bp.exists() or not lp.exists() or lp.stat().st_size < 500:
        return None
    b = _extract(bp.read_text(encoding="utf-8", errors="replace"))
    live = _extract(lp.read_text(encoding="utf-8", errors="replace"))
    d = PostDiff(ref.wid, ref.permalink)
    for k in _STRUCT_TAGS:
        if b.tags.get(k, 0) != live.tags.get(k, 0):
            d.struct[k] = (b.tags.get(k, 0), live.tags.get(k, 0))
    d.href_live_only = sorted(set(live.hrefs) - set(b.hrefs))
    d.href_built_only = sorted(set(b.hrefs) - set(live.hrefs))
    d.src_live_only = sorted(set(live.srcs) - set(b.srcs))
    d.src_built_only = sorted(set(b.srcs) - set(live.srcs))
    bw, lw = b.words(), live.words()
    d.text_live_only = lw - bw
    d.text_built_only = bw - lw
    ba, la = sorted(x for x in b.alts if x), sorted(x for x in live.alts if x)
    if ba != la:
        d.alt_live_only = [x for x in la if x not in ba]
        d.alt_built_only = [x for x in ba if x not in la]
    return d


DIMENSIONS = ("structure", "targets", "text", "alt")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", default="tmp/oracle", help="live-HTML cache dir")
    ap.add_argument("--fetch", action="store_true", help="curl the live oracle first")
    ap.add_argument("--only", choices=DIMENSIONS, help="restrict to one dimension")
    args = ap.parse_args(argv)

    refs = post_refs()
    cache = Path(args.cache)
    if args.fetch:
        fetch_live(refs, cache)

    dims = (args.only,) if args.only else DIMENSIONS
    flagged = 0
    missing = 0
    for ref in refs:
        d = diff_post(ref, cache)
        if d is None:
            missing += 1
            continue
        hits = [dim for dim in dims if d.has(dim)]
        if not hits:
            continue
        flagged += 1
        slug = ref.permalink.split("/")[-1][:46]
        print(f"\n{slug}  [{', '.join(hits)}]")
        if "structure" in hits:
            for k, (bb, ll) in sorted(d.struct.items()):
                print(f"    {k}: built={bb} live={ll}")
        if "targets" in hits:
            for x in d.href_live_only:
                print(f"    href LIVE-only:  {x[:78]}")
            for x in d.href_built_only:
                print(f"    href BUILT-only: {x[:78]}")
            for x in d.src_live_only:
                print(f"    img  LIVE-only:  {x[:78]}")
            for x in d.src_built_only:
                print(f"    img  BUILT-only: {x[:78]}")
        if "text" in hits:
            if d.text_live_only:
                print(f"    text LIVE-only:  {dict(list(d.text_live_only.items())[:12])}")
            if d.text_built_only:
                print(f"    text BUILT-only: {dict(list(d.text_built_only.items())[:12])}")
        if "alt" in hits:
            for x in d.alt_live_only:
                print(f"    alt LIVE-only:  {x[:60]!r}")
            for x in d.alt_built_only:
                print(f"    alt BUILT-only: {x[:60]!r}")

    print(f"\n=== {flagged}/{len(refs)} posts flagged "
          f"({', '.join(dims)}); {missing} unfetched ===")
    if missing and not args.fetch:
        print("(run with --fetch to populate the live cache)")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
