# P1 Results — theme structural fidelity achieved & handoff to P2

**Date:** 2026-05-19  **Branch:** `migration-p1-theme-fidelity` (23 commits ahead of main)
**Spec:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md` (§5 P1, §6.2)
**Plan:** `docs/superpowers/plans/2026-05-19-blog-fidelity-p1-theme.md`
**Regenerate gate:** `uv run python -m scripts.fidelity.structure_check` (exit 0 = PASS 6/6)

## P1 EXIT GATE — PASSED

- `scripts.fidelity.structure_check` → **`Result: PASS (6/6)`, exit 0** — every
  structural archetype's built `_site` HTML contains every Barthelme structural
  anchor (modulo the justified single phantom `div#post-`).
- `uv run pytest -m "not integration" -q` → **40 passed** (P0 harness + the new
  `test_structure_check.py`, incl. the tightened exact-set phantom invariant).
- `bundle3.3 exec jekyll build --trace` → **0** errors/warnings/deprecation/Conflict.
- Worktree clean; every P1 task (T1–T10) two-stage reviewed (spec + code-quality),
  every reviewer-found Critical/Important fixed and re-reviewed.

## Per-archetype structural fidelity (built `_site` vs Barthelme `.php`)

| Archetype | Built path | vs Barthelme | What was made faithful |
|---|---|---|---|
| home | `index.html` | `index.php` | `div.entry-content` wrapper, unconditional `div#nav-below` (Older/Newer) |
| post | `archives/.../<slug>.html` | `single.php` | `span.entry-interact` (comment-status), single canonical `post_slug` shared with comments |
| category | `category/<slug>/index.html` | `archive.php` | archive-meta header, per-post `post-container>post-content>h3.entry-title`+`entry-meta`, nav; **fixed multi-word category filter** (`site.categories[url-slug]`) — all 19 categories list posts |
| page | `about/index.html` | `page.php` | `h2.entry-title` |
| notfound | `404.html` | `404.php` | rewrote to Barthelme `div#container>div#content>div#post-0.post>h2.entry-title+div.entry-content+form#error404-searchform`; removed old custom 404 |
| search | `search.html` | `search.php` | full Barthelme has-results+no-results structure via a statically-parsed `<template>` + `div#post-0`/`form#noresults-searchform`, **client-side search kept functional** (3-state machine, tz-correct dates) |

## Gate-integrity & phantom invariant (resolved)

`PHANTOM_ANCHORS == { div#post- }` ONLY. Justification: Barthelme
`single.php`/`index.php`/`archive.php`/`page.php` emit
`<div id="post-<?php the_ID(); ?>" …>` → PHP-stripping leaves the bare prefix
`#post-` which no Jekyll output can carry → correctly ignored, enforced by an
exact-set unit test. `#post-0` was **de-listed** (commit `63b1d47`, P1-T7): it
is a real static literal in `404.php`/`search.php` and is now a gate-enforced
element (satisfied by T7/T8).

## Scope boundary — P1 is STRUCTURAL fidelity ONLY

Per spec §6.2, P1's gate is the browser-free static structural diff (Barthelme
anchors present in built HTML). **The visual/pixel diff (Playwright + Wayback)
is NOT a P1 deliverable** — it is the post-P4 / P6 acceptance step (it needs P4's
`baseurl=""` so served URLs resolve, and a normalized feed-timestamp baseline).
Structural PASS ≠ pixel-perfect. The P6 acceptance MUST: (a) run the real
Playwright/Wayback pixel sweep across archetypes + sample posts; (b) do a
**functional** sweep (e.g. all 19 category pages list posts; search works in
both branches) — the structural gate checks only one representative per
archetype and would not catch functional emptiness (a Critical category bug was
caught by deeper review, not the gate — see FOLLOWUPS). All accumulated CSS/
visual micro-deltas, the Picasa-strip byte-fidelity, and `#nav-below` clearfix
behavior are logged in FOLLOWUPS for the P6 pixel sweep.

## Picasa header

`_includes/header.html` Picasa photo-strip is UNCHANGED by P1 (user decision:
literal fidelity now; Phase-2/P6 improvement deferred). The `lh*.ggpht.com`
thumbnails / `picasaweb.google.com` links are defunct — a P6 visual-sweep
consideration, not a P1 structural issue.

## P3 status (carried forward — de-risked)

`blog.mithis.net` root = 200 (TLS cert expired → fetch verification-disabled).
The 4 missing posts return HTTP 500 but with the FULL themed article;
snapshotted to `exports/p3-missing-raw/{15,35,84,92}.html` (committed). P3 can
recover them offline regardless of future site state; Wayback is now only a
cross-check. (See the P3 STATUS section in FOLLOWUPS.)

## Deferred — see `docs/superpowers/plans/FOLLOWUPS.md`

P2 content (47-finding linter worklist), P4 domain/`baseurl=""`+CNAME +
404/search/sidebar form actions, P5 new-post workflow + linter build-guard +
gate/linter hardening, P6 visual pixel sweep + functional sweep + CSS micro-
delta audit + Picasa improvement + user signoff. Prior P0/P1 review follow-ups
are annotated RESOLVED where closed.

## Next step (do NOT fix ad hoc)

P1 complete. Per the subagent-driven flow: final whole-P1 review →
finishing-a-development-branch (user preference established at P0: merge to
main, then continue) → then `superpowers:writing-plans` to author the **P2**
plan (content fidelity: drive `lint_content` to zero findings across all posts,
Markdown not hardcoded HTML), then P3 (recover the 4 captured posts), P4
(domain/baseurl), P5 (new-post workflow + linter guard), P6 (visual+functional
acceptance + signoff). Each is its own spec→plan→subagent-execute cycle.
