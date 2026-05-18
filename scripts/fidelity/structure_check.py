# scripts/fidelity/structure_check.py
"""Browser-free static structural-diff runner (P1 gate).

Builds the site, then for each structural archetype reads the built
`_site/*.html` from disk and diffs it against the matching Barthelme `.php`
anchors via the P0 comparator. No browser, no server, no baseurl dependency
(structural ids/classes are static in built HTML; the baseurl prefix only
affects URLs). The visual pixel layer is the separate post-P4 step (spec §6.2).
"""
from __future__ import annotations
import sys
from pathlib import Path

from .archetypes import structural_archetypes
from .barthelme import Anchor
from .build import run_build
from .compare import StructuralResult, structural_diff

BARTHELME = Path("theme_analysis/barthelme")

ARCHETYPE_SITE_PATHS: dict[str, str] = {
    "home":     "index.html",
    "post":     "archives/hardware/2186-nmigen-new-improved-by-whitequark.html",
    "category": "category/hardware/index.html",
    "page":     "about/index.html",
    "notfound": "404.html",
    "search":   "search.html",
}

PHANTOM_ANCHORS: frozenset[Anchor] = frozenset({
    # #post- is a genuine PHP artifact: id="post-<?php the_ID()?>" strips to #post-
    # (home/post/category/archive all use the dynamic WordPress post ID)
    Anchor("div", "#post-"),
    # NOTE: #post-0 is NOT a phantom — it is a static literal in 404.php and
    # search.php (no-results branch). It is a real structural element and must
    # NOT be silently ignored. It was removed from PHANTOM_ANCHORS so that
    # structure_check correctly requires div#post-0 in notfound/search archetypes.
})

def check_html(archetype: str, barthelme_php: str, built_html: str
                ) -> StructuralResult:
    return structural_diff(archetype, barthelme_php, built_html,
                           ignore=PHANTOM_ANCHORS)

def all_pass(results: list[StructuralResult]) -> bool:
    return bool(results) and all(r.passed for r in results)

def check(site_root: str | Path = "_site") -> list[StructuralResult]:
    site = Path(site_root)
    out: list[StructuralResult] = []
    for a in structural_archetypes():
        php = (BARTHELME / a.barthelme_template).read_text(
            encoding="utf-8", errors="replace")
        hp = site / ARCHETYPE_SITE_PATHS[a.name]
        html = hp.read_text(encoding="utf-8", errors="replace") if hp.exists() else ""
        out.append(check_html(a.name, php, html))
    return out

def _format(results: list[StructuralResult]) -> str:
    L = ["# P1 Structural Check", ""]
    L.append(f"- Result: {'PASS' if all_pass(results) else 'FAIL'} "
             f"({sum(1 for r in results if r.passed)}/{len(results)})")
    for r in results:
        L.append(f"\n### {r.archetype}: {'PASS' if r.passed else 'FAIL'}")
        for an in r.missing:
            L.append(f"- MISSING `{an.tag}{an.ident}`")
    return "\n".join(L) + "\n"

def main() -> int:
    build_ok, log = run_build()
    if not build_ok:
        print("BUILD FAILED — cannot run structural check\n" + log[-1500:])
        return 2
    results = check("_site")
    report = _format(results)
    out = Path("tmp/fidelity"); out.mkdir(parents=True, exist_ok=True)
    (out / "p1-structure.md").write_text(report, encoding="utf-8")
    print(report)
    return 0 if all_pass(results) else 1

if __name__ == "__main__":
    sys.exit(main())
