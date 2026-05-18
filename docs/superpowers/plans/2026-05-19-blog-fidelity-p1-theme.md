# Blog Fidelity P1 — Theme Structural Fidelity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax. TDD tasks: use @superpowers:test-driven-development. Before claiming P1 done: use @superpowers:verification-before-completion.

**Goal:** Make the Jekyll templates structurally reproduce the original Barthelme theme so the structural comparator passes for every archetype — measured browser-free against the built `_site`.

**Architecture:** Add a browser-free static structural-diff runner (`structure_check.py`) that builds the site and diffs each archetype's built `_site/*.html` against the corresponding Barthelme `.php` structural anchors using the P0 comparator (`compare.structural_diff`) with a justified phantom-anchor ignore set. Then close the gaps it reports by faithfully editing Liquid layouts/includes/CSS (never hardcoding per-post HTML) until the runner is green. The Playwright/Wayback *visual pixel* layer remains the post-P4 step (spec §6.2) — P1's gate is structural only.

**Tech Stack:** Existing P0 harness (`scripts/fidelity/`), Python via `uv`, Jekyll 4.4 (`bundle3.3` locally), stdlib `html.parser`.

**Spec:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md` (§5 P1, §6.2 CI-vs-local, containment model)
**Inputs:** `docs/superpowers/plans/P0-RESULTS.md` (Barthelme anchor target inventory), `docs/superpowers/plans/FOLLOWUPS.md` (phantom anchors, category-casing, orphan include), `theme_analysis/barthelme/*.php` + `style.css` + `screenshot.png` (fidelity source of truth).

**Local env:** no `bundle` on PATH → use `bundle3.3`. `uv` on PATH. Work from the P1 worktree root. Inline `python -c` is hook-blocked — use pytest / `python -m` / `tmp/` scripts. `tmp/` is gitignored.

**P1 EXIT GATE (precise):** `uv run python -m scripts.fidelity.structure_check` exits 0 — i.e. for ALL 6 structural archetypes (home, post, category, page, notfound, search) the built `_site` HTML contains every Barthelme structural anchor, modulo the explicitly justified `PHANTOM_ANCHORS` ignore set; AND the P0 unit suite still passes; AND `bundle3.3 exec jekyll build` stays clean (0 errors/warnings/Conflict). The visual pixel sweep is NOT a P1 gate (spec §6.2 — it is P6/post-P4).

---

## File Structure

Created:
- `scripts/fidelity/structure_check.py` — browser-free static structural-diff runner + `PHANTOM_ANCHORS` + `ARCHETYPE_SITE_PATHS` + `main()`. One responsibility: "does built `_site` structurally match Barthelme?". Composes P0 `build`/`compare`/`barthelme`/`archetypes` — no new parsing.
- `tests/fidelity/test_structure_check.py` — TDD for the pure logic (path map, phantom set, aggregation/exit policy).
- `docs/superpowers/plans/P1-GAPS.md` — the measured per-archetype MISSING-anchor worklist (data capture, drives closure tasks).
- `docs/superpowers/plans/P1-RESULTS.md` — P1 handoff (what is structurally verified; what defers to P6/post-P4 visual).

Modified during gap closure (templates only — NEVER hardcode per-post HTML; structure lives in Liquid):
- `_layouts/default.html`, `_layouts/home.html`, `_layouts/post.html`, `_layouts/category.html`, `_layouts/page.html`
- `404.html`, `search.html`
- `_includes/header.html`, `_includes/footer.html`, `_includes/sidebar.html`, `_includes/navigation.html`, `_includes/comments.html`
- `assets/css/main.css` (only where a structural element the theme needs is missing/misclassed)

**Containment model (recap):** an archetype PASSES when its built HTML contains EVERY structural anchor (`tag#id`, `tag.class`) of the matching Barthelme `.php`; extra Jekyll anchors are allowed; justified omissions go in `PHANTOM_ANCHORS` with a comment. Browser-free: anchors are static in built HTML; the baseurl/`/blog.mithis.net/` prefix affects URLs, NOT ids/classes, so reading `_site/*.html` from disk is correct and P4-independent.

---

## Task 1: `structure_check.py` — browser-free static structural-diff runner (TDD)

Use @superpowers:test-driven-development for Steps 1–4 (pure logic). Steps 5–7 integration-verify.

**Files:**
- Create: `scripts/fidelity/structure_check.py`
- Test: `tests/fidelity/test_structure_check.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_structure_check.py
from pathlib import Path
from scripts.fidelity.structure_check import (
    ARCHETYPE_SITE_PATHS, PHANTOM_ANCHORS, check_html, all_pass,
)
from scripts.fidelity.compare import StructuralResult
from scripts.fidelity.barthelme import Anchor

def test_every_structural_archetype_has_a_site_path():
    from scripts.fidelity.archetypes import structural_archetypes
    for a in structural_archetypes():
        assert a.name in ARCHETYPE_SITE_PATHS
        assert ARCHETYPE_SITE_PATHS[a.name].endswith(".html")

def test_phantom_anchors_are_barthelme_dynamic_id_artifacts():
    # Documented in FOLLOWUPS: Barthelme id="post-<?php the_ID() ?>" strips to
    # bare prefixes. These are NOT real Jekyll gaps and must be ignored.
    assert Anchor("div", "#post-") in PHANTOM_ANCHORS
    assert Anchor("div", "#post-0") in PHANTOM_ANCHORS

def test_check_html_passes_when_anchors_present():
    php = '<div id="container"><div class="entry-content">x</div></div>'
    html = '<html><div id="container"><div class="entry-content"><p>hi</p></div></div></html>'
    r = check_html("page", php, html)
    assert isinstance(r, StructuralResult) and r.passed

def test_check_html_reports_missing_and_ignores_phantoms():
    php = ('<div id="container"><div id="post-">p</div>'
           '<div id="sidebar">s</div></div>')
    html = '<div id="container"></div>'
    r = check_html("home", php, html)
    assert not r.passed
    assert Anchor("div", "#sidebar") in r.missing
    assert Anchor("div", "#post-") not in r.missing  # phantom ignored

def test_all_pass_true_only_when_every_result_passes():
    assert all_pass([StructuralResult("a", ()), StructuralResult("b", ())])
    assert not all_pass([StructuralResult("a", ()),
                         StructuralResult("b", (Anchor("div", "#x"),))])
    assert not all_pass([])  # empty => not a pass (nothing verified)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_structure_check.py -q`
Expected: FAIL — `ModuleNotFoundError: scripts.fidelity.structure_check`

- [ ] **Step 3: Write minimal implementation**

```python
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

# Built-site HTML path per structural archetype (Jekyll writes pretty-permalink
# pages as <path>/index.html; 404 and search are top-level files).
ARCHETYPE_SITE_PATHS: dict[str, str] = {
    "home":     "index.html",
    "post":     "archives/hardware/2186-nmigen-new-improved-by-whitequark/index.html",
    "category": "category/hardware/index.html",
    "page":     "about/index.html",
    "notfound": "404.html",
    "search":   "search.html",
}

# Barthelme emits id="post-<?php the_ID() ?>" / id="post-0"; PHP-stripping
# leaves bare-prefix phantom anchors that no Jekyll output can or should carry
# (see FOLLOWUPS "structural-extractor phantom anchors"). Ignored, not chased.
PHANTOM_ANCHORS: frozenset[Anchor] = frozenset({
    Anchor("div", "#post-"),
    Anchor("div", "#post-0"),
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_structure_check.py -q`
Expected: PASS (5 passed). Then full hermetic suite `uv run pytest -m "not integration" -q` → 40 passed (prior 35 + 5).

- [ ] **Step 5: Verify the `_site` path map against a real build**

Run: `bundle3.3 exec jekyll build --trace 2>&1 | tail -2` then verify each mapped file exists:
`for p in index.html archives/hardware/2186-nmigen-new-improved-by-whitequark/index.html category/hardware/index.html about/index.html 404.html search.html; do test -f "_site/$p" && echo "OK $p" || echo "MISSING $p"; done`
Expected: all `OK`. If any `MISSING`, the permalink differs — correct `ARCHETYPE_SITE_PATHS` to the real built path (record what you changed) and re-run Step 4.

- [ ] **Step 6: @superpowers:verification-before-completion** — confirm: (a) `uv run pytest -m "not integration" -q` → 40 passed; (b) Step 5 all `OK`; (c) `git status` clean except the 2 new files.

- [ ] **Step 7: Commit**

```bash
git add scripts/fidelity/structure_check.py tests/fidelity/test_structure_check.py
git -c commit.gpgsign=false commit -m "P1: browser-free static structural-diff runner

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Capture the real per-archetype gap list (data → drives closure)

**Files:** Create `docs/superpowers/plans/P1-GAPS.md`

- [ ] **Step 1: Run the runner for real**

Run: `uv run python -m scripts.fidelity.structure_check; echo "exit=$?"`
(It builds, then diffs built `_site` vs Barthelme. `structure_check` is inherently browser-free/server-free — it reads `_site/*.html` from disk, so NO `FIDELITY_SKIP_RENDER` is needed or relevant here. exit=1 with MISSING anchors is EXPECTED — that is the P1 worklist.)

- [ ] **Step 2: Record the worklist**

Write `docs/superpowers/plans/P1-GAPS.md`: paste the runner's per-archetype `MISSING` lists verbatim, and for each archetype note the Barthelme reference file (`theme_analysis/barthelme/<index|single|archive|page|404|search>.php`) and the Jekyll template(s) that own that output (mapping in Task 3). This is the authoritative, data-driven closure list.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/plans/P1-GAPS.md
git -c commit.gpgsign=false commit -m "P1: record measured per-archetype structural gap list

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Tasks 3–8: Close structural gaps — one task per archetype/template

**These are data-driven by Task 2's `P1-GAPS.md` + the Barthelme `.php` reference.** Each task follows the SAME protocol; the controller dispatches one per archetype with that archetype's measured MISSING list. Archetype → Jekyll owner → Barthelme reference:

| Task | Archetype | Edit (Liquid templates only) | Barthelme reference |
|---|---|---|---|
| 3 | home | `_layouts/home.html` (+ `default.html`, `_includes/*`) | `theme_analysis/barthelme/index.php` |
| 4 | post | `_layouts/post.html` (+ `default.html`, `_includes/comments.html`) | `theme_analysis/barthelme/single.php` |
| 5 | category | `_layouts/category.html` | `theme_analysis/barthelme/archive.php` |
| 6 | page | `_layouts/page.html` | `theme_analysis/barthelme/page.php` |
| 7 | notfound | `404.html` | `theme_analysis/barthelme/404.php` |
| 8 | search | `search.html` | `theme_analysis/barthelme/search.php` |

**Per-archetype protocol (each task):**

- [ ] **Step 1: Read the reference + gaps.** Read the Barthelme `.php` for this archetype and this archetype's `MISSING` list in `P1-GAPS.md`. The `.php` is the exact structural target: every missing `tag#id`/`tag.class` corresponds to a real Barthelme structural element (wrapper div, entry-meta span, nav block, etc.).
- [ ] **Step 2: Edit the Liquid template(s)** to introduce the missing structural elements with the SAME tag + id/class as Barthelme, in the SAME nesting, populated from Jekyll data (`page`/`post`/`site`/`paginator`) — NOT hardcoded content. Match Barthelme's structure faithfully; do not invent markup. NEVER add per-post HTML to `_posts/*.md` (that is P2/forbidden — structure lives in templates). Preserve the existing Picasa header markup (user decision: literal fidelity for now).
- [ ] **Step 3: Rebuild & re-diff this archetype.** `bundle3.3 exec jekyll build --trace 2>&1 | grep -ciE "error|warning|deprecation|conflict"` must stay `0`. Then `uv run python -m scripts.fidelity.structure_check 2>&1` and confirm THIS archetype now shows `PASS` (others may still FAIL — that's fine until their task).
- [ ] **Step 4: If a missing anchor is provably another Barthelme dynamic-id/PHP artifact** (like `#post-`), do NOT fake it in the template — add it to `PHANTOM_ANCHORS` in `structure_check.py` with a one-line comment citing the Barthelme `.php` line, and add/extend a `test_structure_check.py` assertion. Justified ignores only; never to silence a real structural gap.
- [ ] **Step 5: Commit** (this archetype only):
```bash
git add -A
git -c commit.gpgsign=false commit -m "P1: <archetype> structural fidelity vs Barthelme <ref>.php

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

**Exit per task:** the archetype's `structure_check` result is `PASS`; build still clean; harness suite still green; only templates/CSS (+ justified `PHANTOM_ANCHORS`) changed — zero `_posts/*.md` edits.

---

## Task 9: Picasa header literal-fidelity note + phantom-ignore justification

**Files:** Modify `docs/superpowers/plans/FOLLOWUPS.md` (justification record only)

- [ ] **Step 1:** Confirm `_includes/header.html` still emits the original Picasa photo-strip markup unchanged (user decision: replicate exactly for now; improvement is deferred Phase-2/P6). It only needs to contribute its structural anchors for P1; deep byte-fidelity of the strip vs the now-reachable live site (`https://blog.mithis.net` 200 with cert-verify off) is a P6 visual concern — record that, do not act on it in P1.
- [ ] **Step 2:** In `FOLLOWUPS.md`, under a new "P1 phantom-ignore justifications" note, list every entry in `PHANTOM_ANCHORS` with the Barthelme `.php` source line proving it is a dynamic-id/PHP artifact (not a hidden real gap). Commit.

---

## Task 10: P1 exit gate + handoff to P2

Use @superpowers:verification-before-completion.

- [ ] **Step 1: Full P1 gate.** `uv run python -m scripts.fidelity.structure_check; echo "exit=$?"` → MUST print `exit=0` and Result: PASS (N/N) for all 6 structural archetypes. `uv run pytest -m "not integration" -q` → all pass. `bundle3.3 exec jekyll build --trace 2>&1 | grep -ciE "error|warning|deprecation|conflict"` → `0`.
- [ ] **Step 2: Write `docs/superpowers/plans/P1-RESULTS.md`** — structural fidelity achieved per archetype; the justified phantom set; explicitly note the visual pixel-diff (Playwright/Wayback) is the post-P4 / P6 step (spec §6.2), NOT done in P1; live-site status for P3; pointer to FOLLOWUPS. Commit.
- [ ] **Step 3: Stop and re-plan.** Do NOT start P2 ad hoc. Return to @superpowers:writing-plans to author the P2 plan (content fidelity — the 47-finding linter worklist from P0-RESULTS), then P3 (missing posts — UNBLOCKED: live site 200 w/ cert-verify off), P4 (domain/baseurl=""), P5, P6.

---

## Subsequent plans (scope note — NOT this plan)

P2 content fidelity (linter→0), P3 missing-post recovery (now unblocked), P4 domain/`baseurl=""` (prereq for the real visual diff), P5 new-post workflow + linter build-guard, P6 final acceptance (Wayback pixel sweep + user signoff). Each is its own data-driven spec→plan→execute cycle. The FOLLOWUPS backlog (phantom anchors, category-casing, orphan `_includes/category-feed.xml`, gate/linter hardening, feed-timestamp normalization for P6) is carried forward.
