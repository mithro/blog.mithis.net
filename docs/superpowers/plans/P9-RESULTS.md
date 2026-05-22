# P9 — Residual Pixel-Perfect Fidelity: RESULTS & Handoff

**Status: COMPLETE.** P9 exit gate met (§1). Branch
`migration-p9-pixel-perfect`, merged to `main`. P9 closed the three
residual visual deltas that P8 had deferred — the site is now
pixel-faithful to live blog.mithis.net (broken stuff and all) across the
audited page types.

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| Content linter (CLI, CI-enforced) | 0 | **PASS (0)** ✓ |
| `structure_check` | 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **56 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean ✓ |
| `_posts` count | 76 | **76** ✓ |
| Tag slugs match live | dot-tags WP-style | `sys.stdout`→`sysstdout` ✓ |
| Code-block token colors match live | GeSHi palette | 6/6 tokens verified via getComputedStyle ✓ |
| Highslide lightbox | initializes like live | `hs.expand` fn, `addHSSlideshow` defined, 20 `.highslide` links ✓ |
| `_posts/` bodies + P0–P6 frozen areas | unchanged | only `_layouts`/`_includes`/`assets`/tag-archives touched ✓ |

## 2. What P9 did (3 commits)

### Tag slug WP-match (`ebb33da`)
Live WP slugifies tags by REMOVING dots (`sys.stdout`→`sysstdout`,
`linux.conf.au`→`linuxconfau`); Jekyll's `slugify` converts dots→hyphens.
Changed the tag-slug expression in `post.html` + `tag.html` to
`{{ tag | remove: '.' | slugify }}` (no-op for the 83 non-dot tags).
Removed the 2 hyphenated duplicate archive pages; the WP-slug archives
(created in P8) are now canonical. Verified: utf-8-in-python `sys.stdout`
footer link → `/archives/tag/sysstdout` == live exactly.

### GeSHi/wp-syntax code token colors (`f1ae541`)
Live uses wp-syntax (GeSHi) token colors (keywords `#ff7700` bold,
comments `#808080` italic, strings `#483d8b`, escapes `#000099` bold,
builtins `#008000`, operators `#66cc66`, names `#dc143c`). Added a
GeSHi-palette override mapping Rouge token classes, placed at the END of
`_includes/syntax-highlighting.css` — that include loads LAST (main.css
`{% include %}`), so it wins over both the in-include Rouge defaults AND
the duplicate Rouge block in main.css. (An earlier attempt to add the
override in main.css body had no effect because the include overrode it —
the bug was a triple-duplicated Rouge token set; the include is the
authoritative last-loaded copy.) Verified via getComputedStyle: all 6 key
tokens match GeSHi exactly.

### Highslide lightbox vendoring (`a1fecc9`)
Live loads the shashin plugin's highslide lightbox so clicking a Picasa
thumbnail opens a JS lightbox. Locally the thumbnails had inline
`onclick="hs.expand(...)"` but `hs` was undefined → clicks were no-ops.
Vendored highslide.js (47K) + highslide.css (21K) + highslideSettings.js +
shashin.css + 11 lightbox-chrome graphics into
`assets/shashin/Public/Display/` (mirroring live's path so the CSS's
relative `graphics/` refs resolve). Wired into `default.html <head>` with
the inline `var highslideSettings` (graphicsDir → vendored path). Skipped
photoGroupsDisplayer.js + jQuery (only for AJAX photo groups, not the
inline-onclick lightbox). Verified: `hs.expand` is a function,
`addHSSlideshow` defined, 20 `.highslide` links. Clicking opens the
lightbox showing the broken ggpht 404 image — faithful to live's broken
state. Robust post-cutover (vendored, not referencing wp-content).

## 3. Cumulative project state (P0 → P9)

- Content + tags + structure + comments + URL fidelity (P0–P8).
- **Rendered visual fidelity (P7+P8+P9)** — header (broken Picasa gallery +
  working highslide lightbox), sidebar RIGHT (Twitter widget + Shashin
  photos), categories (sort order + `<br/>` separator + full-content
  archives), dates (+1000), code blocks (GeSHi container + token colors),
  tag/author archives, WP-style tag slugs — all match live, broken stuff
  and all.
- Authoring workflow + CI build-guard (P5) — intact.
- **The only remaining work is the user's DNS cutover** — still NOT to be
  suggested until the user confirms they're satisfied with fidelity.

## 4. P9 gate — independent re-verification

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # 0
uv run python -m scripts.fidelity.structure_check                      # 6/6
uv run python -m pytest tests/ -q                                      # 56
bundle3.3 exec jekyll build                                            # clean
ls _posts/*.md | wc -l                                                 # 76
# Tag slug: grep sysstdout in built utf-8-in-python.html → matches live
# Code colors + highslide: serve _site/ + Playwright getComputedStyle / hs check
```

After P9, no known visible visual delta remains vs live across the audited
page types (home, post, code-heavy, category, tag, author, search, 404).
