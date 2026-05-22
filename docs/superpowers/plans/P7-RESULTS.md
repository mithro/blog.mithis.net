# P7 — Visual/Pixel Fidelity (theme CSS + broken-stuff pivot): RESULTS & Handoff

**Status: COMPLETE (this iteration).** P7 exit gate met (§1). Branch
`migration-p7-css-fidelity`, merged to `main`. Remaining cosmetic deltas
are recorded as P8 followups (§5) per the user's "merge now + iterate on
followups" direction.

## Why P7 happened

After P0–P6 were merged and declared "software-complete", the user asked:
"So now the screenshot of blog.mithis.net is identical to the new github
pages hosted version?" An actual pixel comparison (Playwright screenshots
local `_site/` vs live `blog.mithis.net`) revealed that prior phases had
verified **structural HTML fidelity** but NOT **rendered pixel fidelity** —
the theme CSS, header, sidebar, and several layout elements diverged
visibly. P7 closes that gap.

**Two user directives reshaped the goal during P7:**
1. "Do not suggest any type of cut over until you have verified 100%
   fidelity." → No deployment framing until pixel-verified.
2. "The github version should be faithful to the current live
   https://blog.mithis.net — broken stuff and all." → This **inverted** the
   prior CLAUDE.md "Remove Broken Features: Twitter + Picasa" requirement.
   The Jekyll site must now reproduce the live WP rendering INCLUDING its
   broken bits (broken Picasa thumbnails, Twitter cached-tweets widget,
   full-content category archives).

## 1. Exit gate (verified from clean tree at `64c2cf4`)

| Gate | Required | Observed |
|---|---|---|
| Content linter (CLI, CI-enforced) | 0 findings | **PASS (0)** ✓ |
| `structure_check` | 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **56 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean ✓ |
| `_posts` count | 76 | **76** ✓ |
| CI build-guard (P5-H) | still wired | `.github/workflows/jekyll.yml` unchanged ✓ |
| Sidebar position | RIGHT (matches live) | sidebar.x=1040 w=240 float:right ✓ |
| Header Picasa gallery | present + broken (matches live) | Shashin `<table>` w/ 6 ggpht-404 thumbs ✓ |
| Twitter widget | present (matches live) | aktt-widget cached tweets ✓ |
| Category pages | full post content (matches live) | `post.content` inline ✓ |
| Category separator | `<br/>` (matches live) | `<a>Cat1</a><br/><a>Cat2</a>` ✓ |
| Post-date timezone | +1000 (matches live) | `2020-05-02T...+10:00` → "2020 05 02" ✓ |
| Body class | Barthelme `single/home/archive/...` | mapped from Jekyll layout ✓ |
| `_posts/` / scripts / tests / category .md | UNCHANGED (P0–P6 intact) | zero diff ✓ |
| Working tree | clean | 11 commits ahead of `main` |

## 2. What P7 did (11 commits)

### Audit
- **`81daa7c` P7-T1:** Multi-page screenshot-pair audit; catalogued 17
  deltas. (NOTE: this audit's "sidebar should be float:left" inference was
  WRONG — corrected in `9bb4cd0`. Lesson: infer layout from the live
  *rendered* DOM via Playwright `getComputedStyle`, not from the base
  Barthelme stylesheet, which the live WP overrides.)
- **`90c007d` P7-T2:** 15-page post-fix audit (findings v2); found the
  category-content-inline + sidebar-disappears deltas + (mistakenly in §E)
  listed Picasa/Twitter removals as "correct" — later inverted by the
  user's pivot.

### CSS + layout fixes
- **`bf4e353`:** 16 CSS deltas (header alignment, widget de-boxing, tag
  cloud, code-block borders, comment list, etc.). NOTE: its C1/C4
  (sidebar float) was later corrected.
- **`7a747d0`:** Map Jekyll `page.layout` → Barthelme body class
  (`post`→`single`, `category`→`archive`, +`search`, +`home`); use
  `page.date` for the y/m/d/h body-class tokens. **This fixed the
  single-post two-column layout** (Barthelme's `body.single div#container`
  rules were dead-code before).
- **`5ce31c7`:** Move sidebar `{% include %}` outside the floated
  `#container` in `post.html` so it doesn't disappear on tall/image-heavy
  posts (X-1).
- **`9bb4cd0`:** Flip sidebar to RIGHT (revert bf4e353 C1/C4) — verified
  against live's actual rendered DOM (sidebar float:right, x=992).
- **`64c2cf4`:** Category separator `<br/>` + timezone Australia/Brisbane
  (+1000) to match live's date display + category stacking.

### Broken-stuff-faithful pivot (per user directive)
- **`ce45bae`:** Restore the Picasa Shashin gallery in the header using
  live's exact `<table class="shashinThumbnailsTable">` markup (6 thumbs
  with broken-by-design ggpht 404 URLs) + Shashin/highslide CSS rules.
- **`e0e0b4e`:** Restore the Twitter (`aktt-widget`) cached-tweets widget
  in the sidebar + the Shashin photos widget (14 broken thumbs).
- **`009caac`:** Category archive pages render full `post.content` inline
  (WP archive behavior) instead of title+excerpt.
- **`5a2e0ee`:** Update CLAUDE.md ("Full WP Fidelity … broken bits and
  all"), P6-PICASA-CHECK.md (disposition inverted), FOLLOWUPS.md.

## 3. Verification method (reusable)

- Serve `_site/` locally: `uv run python -m http.server 4321 --bind 127.0.0.1`.
- Playwright at 1280×900 viewport (`browser_resize` — note Playwright
  **resets viewport to 780 on navigation**, so resize AFTER each navigate).
- Playwright **HTTP-caches CSS aggressively** even across `browser_close`;
  bust by appending `?bust=<ts>` to the `<link>` href via `browser_evaluate`
  before measuring/screenshotting.
- Compare via `getComputedStyle` + `getBoundingClientRect` for exact
  positions/floats; screenshot + Read tool for visual diff.
- Live oracle has TLS-expired cert (Playwright tolerates; `curl -sk` for
  HTML fetches).

## 4. Cumulative project state (P0 → P7)

- Content/structure/comments/URL fidelity (P0–P6) — intact (P7 touched no
  `_posts/`, no `_data/`, no scripts, no category `.md`).
- **Rendered visual fidelity (P7)** — header, sidebar (RIGHT), widget
  order, category-full-content, date timezone, category `<br/>` separator
  all match live; broken Picasa + Twitter widgets reproduced
  (broken-stuff-faithful per user directive).
- Authoring workflow + CI build-guard (P5) — intact.
- **NOT yet done:** P8 cosmetic followups (§5) + the user's DNS cutover
  (still NOT to be suggested until the user is satisfied with fidelity).

## 5. P8 followups (recorded in FOLLOWUPS.md)

Cosmetic deltas deferred per the user's "merge now + iterate" decision:
- **Category ORDER** on multi-category posts differs from live (live order
  vs frontmatter order). Needs WP category-order replication.
- **More page-type verification**: image-heavy posts, code-heavy posts,
  search page, 404, hardware/project/tutorial layouts, date archives,
  tag pages, author page — screenshot-compare each vs live.
- **Subtle font-weight / spacing** micro-deltas not yet exhaustively
  checked.
- **Shashin highslide lightbox JS** not loaded locally — clicking a header
  thumbnail opens the ggpht 404 URL directly instead of the JS lightbox.
  (Low priority: the thumbnails are broken anyway; the lightbox would also
  show a broken image.)
- **`<br/>` vs WP's exact whitespace** in other meta areas — spot-check.

## 6. P7 gate — independent re-verification

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # exit 0
uv run python -m scripts.fidelity.structure_check                      # 6/6
uv run python -m pytest tests/ -q                                      # 56
bundle3.3 exec jekyll build                                            # clean
ls _posts/*.md | wc -l                                                 # 76
# Visual: serve _site/ + Playwright screenshot vs live (see §3)
```
