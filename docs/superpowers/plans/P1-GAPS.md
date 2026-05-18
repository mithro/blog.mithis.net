# P1-GAPS — measured per-archetype structural gap list (drives P1-T3…T8)

**Date:** 2026-05-19  **Branch:** `migration-p1-theme-fidelity`
**Source:** `uv run python -m scripts.fidelity.structure_check` → Result: **FAIL (0/6)**, exit=1
**Regenerate:** `uv run python -m scripts.fidelity.structure_check` (also writes `tmp/fidelity/p1-structure.md`)

Each `MISSING tag.class`/`tag#id` is a Barthelme structural element the built
Jekyll `_site` HTML for that archetype does NOT contain. Close by faithfully
adding the element (same tag + id/class + nesting, populated from Jekyll data)
to the **Jekyll owner template** — Liquid templates ONLY, never `_posts/*.md`.
The **Barthelme reference** is the exact structural target. Phantoms
(`div#post-`, `div#post-0`) are correctly suppressed by `PHANTOM_ANCHORS` and do
NOT appear below (but see the `#post-0` gate-integrity note in FOLLOWUPS — T7/T8
must verify it explicitly, do not rely on its absence here).

| Archetype | Jekyll owner template(s) | Barthelme reference |
|---|---|---|
| home | `_layouts/home.html` (+ `default.html`, `_includes/*`) | `theme_analysis/barthelme/index.php` |
| post | `_layouts/post.html` (+ `default.html`, `_includes/comments.html`) | `theme_analysis/barthelme/single.php` |
| category | `_layouts/category.html` | `theme_analysis/barthelme/archive.php` |
| page | `_layouts/page.html` | `theme_analysis/barthelme/page.php` |
| notfound | `404.html` | `theme_analysis/barthelme/404.php` |
| search | `search.html` | `theme_analysis/barthelme/search.php` |

## home — P1-T3 (2 gaps)
- MISSING `div#nav-below`
- MISSING `div.entry-content`

## post — P1-T4 (1 gap)
- MISSING `span.entry-interact`

## category — P1-T5 (12 gaps)
- MISSING `abbr.published`
- MISSING `div#nav-below`
- MISSING `div.archive-meta`
- MISSING `div.entry-meta`
- MISSING `div.nav-next`
- MISSING `div.post-container`
- MISSING `div.post-content`
- MISSING `h3.entry-title`
- MISSING `span.archive-meta`
- MISSING `span.entry-category`
- MISSING `span.entry-comments`
- MISSING `span.entry-date`

## page — P1-T6 (1 gap)
- MISSING `h2.entry-title`

## notfound — P1-T7 (8 gaps) — ALSO resolve the `#post-0` gate-integrity item (FOLLOWUPS)
- MISSING `div#container`
- MISSING `div#content`
- MISSING `div.entry-content`
- MISSING `div.post`
- MISSING `form#error404-searchform`
- MISSING `h2.entry-title`
- MISSING `input#error404-s`
- MISSING `input#error404-searchsubmit`

## search — P1-T8 (18 gaps) — ALSO resolve the `#post-0` gate-integrity item (FOLLOWUPS)
- MISSING `abbr.published`
- MISSING `div#container`
- MISSING `div#content`
- MISSING `div#nav-below`
- MISSING `div.entry-meta`
- MISSING `div.hfeed`
- MISSING `div.nav-next`
- MISSING `div.post`
- MISSING `div.post-container`
- MISSING `div.post-content`
- MISSING `form#noresults-searchform`
- MISSING `h3.entry-title`
- MISSING `input#noresults-s`
- MISSING `input#noresults-searchsubmit`
- MISSING `span.archive-meta`
- MISSING `span.entry-comments`
- MISSING `span.entry-date`
- MISSING `span.search-meta`

## Notes for closure tasks
- Total gaps: 42 across 6 archetypes (home 2, post 1, category 12, page 1,
  notfound 8, search 18). The current Jekyll templates already emit most
  Barthelme anchors — these are targeted structural additions, not rewrites.
- `notfound`/`search` are the most divergent (search forms, post wrappers,
  `div#container`/`div#content` — these wrappers come from `_layouts/default.html`
  vs the standalone `404.html`/`search.html`; check whether those pages use the
  default layout or are standalone, and whether the search form structure
  matches Barthelme's `error404-`/`noresults-` ids).
- Each closure task must keep the build clean (0 errors/warnings/Conflict),
  re-run `structure_check`, confirm THAT archetype flips to PASS, and touch
  ONLY templates/CSS (+ justified `PHANTOM_ANCHORS`) — zero `_posts/*.md` edits.
