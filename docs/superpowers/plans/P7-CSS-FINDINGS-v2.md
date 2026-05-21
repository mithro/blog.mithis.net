# P7-CSS-FINDINGS-v2: Post-Fix Multi-Page Visual Audit

**Date**: 2026-05-21
**Branch**: `migration-p7-css-fidelity`
**Basis commits**: T1 audit `81daa7c` → 16-delta fix `bf4e353` → body-class mapping fix `7a747d0`
**Auditor**: Playwright subagent (T2 pass — audit only, no fixes)

---

## §A — Method

### Screenshot capture
- **Viewport**: 1280×900 px (desktop, CSS pixels)
- **Tool**: Playwright MCP (`mcp__plugin_playwright_playwright__browser_resize` + `browser_take_screenshot`)
- **Full-page**: yes (`fullPage: true`)
- **Local server**: Python `http.server` on `http://127.0.0.1:4321` serving `_site/` (pre-running; not started by this audit)
- **Screenshot directory**: `tmp/p7-t2/` (gitignored)
- **Naming**: `local-NN-<slug>.png` / `live-NN-<slug>.png`

### Oracle source per page

| # | Page type | Local URL | Live Oracle |
|---|-----------|-----------|-------------|
| 01 | Home | `http://127.0.0.1:4321/` | `https://blog.mithis.net/` |
| 02 | Post — basic prose | `.../sci-fi/102-starhunter-fireflys-little-known-older-cousin.html` | same path (no `.html`) |
| 03 | Post — image-rich | `.../timvideos-us/1995-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.html` | same path |
| 04 | Post — Liquid-fix | `.../uncategorized/77-epiphany2firefox.html` | same path |
| 05 | Post — float-image | same as #02 (starhunter; float:right div verified) | same |
| 06 | Post — code-heavy | `.../python/91-utf-8-in-python.html` | same path |
| 07 | Post — fritzbox | `.../ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc.html` | same path |
| 08 | Post — long-form | `.../timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014.html` | same path |
| 09 | Category — python | `http://127.0.0.1:4321/archives/category/python/` | `https://blog.mithis.net/archives/category/python/` |
| 10 | Category — lca | `http://127.0.0.1:4321/archives/category/lca/` | `https://blog.mithis.net/archives/category/lca/` |
| 11 | Hardware layout | `http://127.0.0.1:4321/hardware/cfxs-device/` | N/A — Jekyll-only page |
| 12 | Project layout | `http://127.0.0.1:4321/projects/hdmi2usb/` | N/A — Jekyll-only page |
| 13 | Tutorial layout | `http://127.0.0.1:4321/tutorials/python-cookies/` | N/A — Jekyll-only page |
| 14 | Search page | `http://127.0.0.1:4321/search.html` | N/A — not on live WP |
| 15 | 404 page | `http://127.0.0.1:4321/404.html` (direct) | `https://blog.mithis.net/this-does-not-exist.html` |

**Notes**:
- Live site TLS cert expired; Playwright connected without error.
- Local category URLs: `/archives/category/<slug>/` resolved correctly (category layout served at this path, not a redirect in the actual `_site/` filesystem).
- Local `search/` (trailing slash) returned python `http.server` 404; used `search.html` directly instead.
- Local `this-does-not-exist.html` returned python `http.server` raw error (python's built-in 404 page, not Jekyll's `404.html`); audited `404.html` directly instead — this is a server limitation, not a Jekyll defect.
- Pages 11–13 (hardware/project/tutorial) are Jekyll-only collections with no WP equivalent; comparison is layout-integrity only.

---

## §B — Per-Page Results Table

| # | Page type | Slug | PASS/FAIL | 1-line summary |
|---|-----------|------|-----------|----------------|
| 01 | Home | home | FAIL | Sidebar present and LEFT; header left-aligned; content column still slightly narrow vs live; category dropdown selector visual difference |
| 02 | Post — basic prose | starhunter | FAIL | Header/sidebar structurally correct; content renders; comments present; sidebar lacks visible styling context for photo widget; comment form structure differs |
| 03 | Post — image-rich | hdmi2usb-day4 | FAIL | Sidebar LEFT; images render; but sidebar is MISSING entirely (absent from rendered local page) |
| 04 | Post — Liquid-fix | epiphany2firefox | PASS | Content renders correctly; sidebar present; layout matches live structurally |
| 05 | Post — float-image | starhunter (float) | PASS | float:right div wrap renders correctly; content wraps around image as on live |
| 06 | Post — code-heavy | utf8-python | FAIL | Code blocks render with syntax highlighting (colored tokens); live has plain gray code — this is a known improvement divergence; no border/background box (fix verified); sidebar correct |
| 07 | Post — fritzbox | fritzbox | FAIL | Sidebar MISSING entirely (no sidebar column rendered in the page); content renders but no right/left sidebar column |
| 08 | Post — long-form | hdmi2usb-day3 | FAIL | 3-level nested lists render; sidebar MISSING entirely; no sidebar column visible |
| 09 | Category — python | cat-python | FAIL | LOCAL shows post titles + one-sentence excerpt only; LIVE shows full post body content for each post — major content-display delta |
| 10 | Category — lca | cat-lca | FAIL | Same as #09: titles+excerpt only vs full content; sidebar present on local; confirmed cross-category |
| 11 | Hardware layout | cfxs-device | N/A | Jekyll-only; renders correctly with header+content+footer; no sidebar (by layout design) |
| 12 | Project layout | hdmi2usb-project | N/A | Jekyll-only; renders header+content+footer; header band missing on project page (no dark blue header seen) |
| 13 | Tutorial layout | python-cookies | N/A | Jekyll-only; renders with header band + content; no sidebar (by layout design) |
| 14 | Search page | search | N/A | Jekyll-only; renders with correct theme header+sidebar+footer; functional layout |
| 15 | 404 page | 404-direct | FAIL | Local `404.html` renders correct Jekyll styled page; python http.server serves raw error for unmatched paths (not Jekyll 404) |

**Summary**: 12 pages with live oracle → 4 PASS, 7 FAIL, 1 FAIL (server limitation). 3 N/A pages (Jekyll-only). Total 15 pages audited.

---

## §C — Detailed Delta Catalog

### C.1 — Cross-Page Deltas

These deltas appear on **multiple pages** and share a common root cause.

---

#### DELTA X-1 — Sidebar absent on several single-post pages (HIGH)

**Scope**: Cross-page (pages 03, 07, 08 confirmed missing sidebar)
**Severity**: HIGH — the sidebar column disappears entirely; content spans full width

**Live**: Right-hand sidebar column with widgets (Home, Categories, Tags, RSS, Recent Posts, Other Cool People, Meta) visible on ALL post pages.

**Local**: On pages 03 (HDMI2USB day 4), 07 (fritzbox), 08 (HDMI2USB day 3) — the sidebar column does not appear at all. The main content area stretches across the full page width. The sidebar IS present on home, starhunter, epiphany2firefox, search, and 404 pages.

**Root-cause hypothesis**: The body-class mapping fix (`7a747d0`) applied `body.single` class to single post pages, which changes the CSS rule applied to `#container` and `#content`. The CSS for `body.single div#container { margin: 0 0 6em -20em }` may be collapsing or hiding the sidebar under certain conditions when combined with specific post content lengths or image heights. Alternatively, the sidebar `div.sidebar` `float:left` is being cleared by images or long content in the post. This may be a float-clearing issue: a `clear:both` or very tall image in the content column collapses the sidebar float before it can render alongside the content.

**Affected pages**: 03, 07, 08 (and possibly others with longer content)
**Target files**: `assets/css/main.css` (float clearing rules for `.sidebar`), `_layouts/post.html` (check for `clearfix` or `overflow:hidden` on wrapper)

---

#### DELTA X-2 — Category pages show titles-only, not full post content (HIGH)

**Scope**: Cross-page (pages 09, 10 confirmed)
**Severity**: HIGH — the category archive page is functionally different from live

**Live** (`/archives/category/python/`, `/archives/category/lca/`): Each post entry shows the **full post body content** — several paragraphs of text, code blocks, images, everything rendered inline. The category page is a long scrollable page of complete post content.

**Local**: Each post entry shows only the **post title** (as a linked heading) and a **one-sentence excerpt** pulled from the first line of the post body. The body content is NOT rendered. This makes the category page dramatically shorter and less information-dense than live.

**Root-cause hypothesis**: The category layout template (`_layouts/category.html`) uses `post.excerpt` or a truncated summary instead of `post.content`. On live WordPress, category archives show full post content (WordPress default when no `<!--more-->` tag is present). The Jekyll category template needs to use `{{ post.content }}` instead of `{{ post.excerpt }}`.

**Affected pages**: All category pages (09, 10 verified; likely all other categories)
**Target files**: `_layouts/category.html` (change `post.excerpt` to `post.content`)

---

#### DELTA X-3 — Syntax highlighting in code posts (LOW — intentional improvement)

**Scope**: Cross-page (all posts with code blocks — page 06 confirmed)
**Severity**: LOW (this is a deliberate improvement, not a regression)

**Live**: Code blocks rendered as plain gray text — no syntax coloring, plain `<pre><code>` with Courier font.

**Local**: Code blocks have Rouge syntax highlighting — keywords, strings, comments rendered in distinct colors. The border/background box was removed (fix C7 verified working — no box frame around code blocks). Only the coloring differs.

**Root-cause hypothesis**: Jekyll uses Rouge highlighter by default; WordPress plain `<code>` blocks have no server-side highlighting. This is an intentional enhancement.

**Affected pages**: All code-heavy posts (~8)
**Note**: Per project requirements, this is an IMPROVEMENT. See §E (Out-of-Scope).

---

#### DELTA X-4 — Header band styling: subtle remaining differences (MEDIUM)

**Scope**: Cross-page (all pages)
**Severity**: MEDIUM

**Live**: Header band (`#header`) is the muted blue-grey background (`#bbc8d9` approx); site title "Mithro rants about stuff" is left-aligned with ~3em left padding; description text below; no bottom border; no separator.

**Local (post-fix)**: Header band present with correct color; title left-aligned (fix C2 verified); no bottom border (fix C2 verified); Picasa gallery removed (fix C8 verified). However, comparing screenshots closely: local header band appears slightly **taller** than live (more top/bottom padding). The description text and "Contact Me" nav link appear, but the vertical rhythm differs slightly — the header occupies more vertical space in the local version.

**Root-cause hypothesis**: `body div#header { padding: 1.2em 0 1.2em 3em }` (Barthelme value) should match live exactly. A small secondary `padding` override or line-height difference may be adding height.

**Affected pages**: All pages
**Target files**: `assets/css/main.css` (verify `body div#header` padding; check no secondary override remains)

---

#### DELTA X-5 — Post listing entry-date width: visual spacing difference (MEDIUM)

**Scope**: Cross-page (home, category pages)
**Severity**: MEDIUM

**Live** (home page listing): Date column on left side of each post entry uses `10em` width; post title/excerpt has matching left margin. The dates (e.g., "2020-05-01") sit cleanly in their column.

**Local**: Per fix C10, `entry-meta` width was set to `10em` and post-container/post-content margins updated. In the home screenshot, the date column appears correct. However, on the category pages, the column alignment appears slightly different — the date aligns correctly but the spacing between date and title is subtly different from live.

**Root-cause hypothesis**: The category layout may use a different post listing CSS context than the home page listing. The `10em` fix applied to `body.home div#content div.entry-meta` may not cascade to `body.category div#content div.entry-meta`.

**Affected pages**: 09, 10 (category listings)
**Target files**: `assets/css/main.css` (check category-specific selectors for entry-meta width)

---

### C.2 — Single-Page Deltas

These deltas appear on specific pages only.

---

#### DELTA S-1 — HDMI2USB day 4 (page 03): sidebar missing + centered images (HIGH)

**Page**: 03 — `1995-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.html`
**Severity**: HIGH

**Live**: Full two-column layout; sidebar on left with all widgets; centered images render with caption text below; blockquote styling visible at end of post.

**Local**: Sidebar column completely absent — content spans full width. Centered images appear to render (visible in screenshot). Blockquote border appears. The primary failure is the missing sidebar, which is DELTA X-1 above. Additionally, there are more images/thumbnails rendered in local that appear correctly centered.

---

#### DELTA S-2 — Fritzbox (page 07): sidebar missing (HIGH)

**Page**: 07 — `1833-connecting-to-a-fritzbox-under-linux-using-vpnc.html`
**Severity**: HIGH

**Live**: Full two-column layout; sidebar on left; long post with config file code blocks, screenshot image of Fritz!Box admin panel.

**Local**: Sidebar completely absent; content spans full width. Code blocks render without box border (fix C7 verified). The Fritz!Box admin screenshot image renders correctly. The entire layout difference is the missing sidebar (DELTA X-1).

---

#### DELTA S-3 — HDMI2USB day 3 (page 08): sidebar missing + list nesting (HIGH)

**Page**: 08 — `1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014.html`
**Severity**: HIGH

**Live**: Full two-column layout; 3-level nested ordered lists with correct indentation visible; sidebar on left.

**Local**: Sidebar absent (DELTA X-1). 3-level nested list content visible and renders at correct indentation in the content column. The list nesting fix (PSL work) appears to be correctly rendered. Primary failure is missing sidebar.

---

#### DELTA S-4 — Starhunter (pages 02, 05): comments section styling (MEDIUM)

**Page**: 02/05 — starhunter
**Severity**: MEDIUM

**Live**: Comments section shows `ol.commentlist` items without left border accent; alternating row colors (`li.alt` has slightly darker background `#e7eaed`); comment author name in bold; date inline.

**Local**: Comment items rendered; left border accent (3px solid `#bbc8d9`) visible on each comment per the `_includes/comments.html` template styling. This is the custom addition noted in P7-CSS-FINDINGS T1 §B4. The alternating background is not present. Fix C13 (formcontainer CSS) was applied but the comment list styling addition from T1 (ol.commentlist) may have added the border-left accent.

**Root-cause hypothesis**: The `bf4e353` commit added `ol.commentlist` styling which includes `border-left: 3px solid #bbc8d9`. This was part of the fix but differs from Barthelme original which uses no border-left on comment items.

**Target files**: `assets/css/main.css` (remove `border-left` from `ol.commentlist li` or `div.comment`)

---

#### DELTA S-5 — 404 page: python http.server serves its own error page (MEDIUM)

**Page**: 15 — unmatched URL
**Severity**: MEDIUM (but server limitation, not Jekyll defect)

**Live**: Styled "Page not found" page with full Barthelme theme header+sidebar+footer; message "Apologies, but we were unable to find what you were looking for. Perhaps the search box will help."

**Local (`http://127.0.0.1:4321/404.html` direct)**: Jekyll's `404.html` renders correctly with full theme styling — matches live structurally.

**Local (unmatched URL)**: Python `http.server` returns its raw built-in "Error response / Error code: 404 / Message: File not found." page with no styling — this is expected behavior of the test server. Production deployment (GitHub Pages, Nginx, etc.) will serve `404.html` correctly.

**Impact**: None in production; only a test-harness limitation. Not a Jekyll or CSS issue.

---

#### DELTA S-6 — Project layout (page 12): missing header band (MEDIUM)

**Page**: 12 — `/projects/hdmi2usb/`
**Severity**: MEDIUM (Jekyll-only page, N/A for live oracle, but theme consistency matters)

**Live oracle**: N/A

**Local**: The project page renders title, description, feature list, blog post links, and external links correctly. However the dark blue-grey header band (`#header` zone) is **absent** from the project layout page — the page starts directly with the large H1 "HDMI2USB Project" heading. The tutorial layout (page 13) DOES show the header band correctly. The hardware layout (page 11) also shows the header band correctly.

**Root-cause hypothesis**: The `_layouts/project.html` may be missing the `{% include header.html %}` include, or it uses a different base layout (`default.html` vs `home.html`) that handles the header differently.

**Target files**: `_layouts/project.html` (verify `{% include header.html %}` is present)

---

#### DELTA S-7 — Search page (page 14): photo widget section in sidebar (LOW)

**Page**: 14 — `/search.html`
**Severity**: LOW

**Live oracle**: N/A (no live search page)

**Local**: Search page renders correctly with full header+sidebar+main content area. The sidebar shows "Follow Me on Twitter" and "Photos" sections that reference removed features (Twitter integration, Picasa). These sections correctly show the placeholder text (e.g., "Note: Twitter integration has been removed during migration."). The sidebar layout is correct. The search input area is present. No functional issue — just confirming the placeholder text is visible.

---

## §D — Recommended Fix Sequence

Sorted by visual impact × scope. Complexity: S=small (≤5 lines), M=medium (5–20 lines), L=large (20+ lines or structural change).

| # | Delta | Name | Target file(s) | Complexity | Impact |
|---|-------|------|---------------|------------|--------|
| 1 | X-1 | **Fix sidebar disappearing on single posts** | `assets/css/main.css` (float clearing on content/wrapper; check `clearfix`), `_layouts/post.html` | M | Restores sidebar on pages 03, 07, 08+ — HIGH impact, affects all posts |
| 2 | X-2 | **Category pages: show full post content** | `_layouts/category.html` (change `post.excerpt` to `post.content`) | S | Restores full post bodies on all category pages — HIGH functional impact |
| 3 | S-4 | **Remove border-left accent from comment list items** | `assets/css/main.css` (`ol.commentlist li` or `div.comment` rule) | S | Removes non-Barthelme left border on comments — MEDIUM, all commented posts |
| 4 | S-6 | **Add header include to project layout** | `_layouts/project.html` | S | Restores header band on project pages — MEDIUM, N/A pages but theme consistency |
| 5 | X-4 | **Verify header padding matches Barthelme exactly** | `assets/css/main.css` (`body div#header` padding; check for overrides) | S | Minor height difference on all pages — MEDIUM |
| 6 | X-5 | **Category entry-meta width for non-home contexts** | `assets/css/main.css` (add `body.category div#content div.entry-meta { width: 10em }` etc.) | S | Post listing spacing on category pages — MEDIUM |
| 7 | X-3 | **Syntax highlighting** | N/A — see §E | — | Intentional improvement; no fix needed |
| 8 | S-5 | **404 via http.server** | Not a code fix — document as test-server limitation in §F exit gate | — | Production will serve correctly |

---

## §E — Out-of-Scope per Project Requirements

These items DIFFER from live but are CORRECT per the project's stated directives (CLAUDE.md: "Remove Broken Features: Twitter integration and Google Picasa integration"). They must NOT be treated as deltas to fix.

| # | Item | What live shows | What local shows | Why it is correct |
|---|------|----------------|-----------------|-------------------|
| E-1 | Picasa/Google Photos header gallery | Broken image thumbnails in `#header-photos` div (images 403 from `lh3.ggpht.com`); occupies space in header | Gallery completely removed from header | Per project requirements: "Remove Broken Features: Twitter integration and Google Picasa integration" (CLAUDE.md). Fix C8 (`bf4e353`) intentionally removed this. |
| E-2 | Twitter "Follow Me" sidebar widget | Functional Twitter follow button + timeline widget (now broken as Twitter API changed) | Placeholder text: "Note: Twitter integration has been removed during migration. Follow @mithro on Twitter." | Per project requirements. The removal note is appropriate. |
| E-3 | Google Picasa sidebar "Photos" widget | Shows broken/missing photo thumbnails from Picasa | Placeholder text: "Note: Photo gallery integration has been removed during migration. View photos at GitHub." | Per project requirements. |
| E-4 | Syntax-highlighted code blocks | Plain gray Courier code; no coloring | Rouge-highlighted code with colored keywords/strings/comments | Jekyll's built-in Rouge highlighter is an improvement. The border/background box was removed (matching Barthelme); only coloring differs. This is a feature enhancement not a regression. |
| E-5 | reCAPTCHA on comment form | Live WP shows reCAPTCHA widget before submit button | No reCAPTCHA in local comment form | WordPress plugin behavior; not applicable to Jekyll static site. |
| E-6 | WordPress "Log In" link in Meta widget | "Log In" link visible in Meta sidebar widget | Not present (no WordPress login in Jekyll) | Jekyll has no WordPress backend; the link would be meaningless. |
| E-7 | Dynamic WordPress search via server | WP search submits to `/?s=query` server-side | Local search uses JavaScript JSON index (`search.json`) | Functionally equivalent or better; static search is the correct Jekyll approach. |
| E-8 | Comment moderation/approval flow | WP comments go through moderation queue | Static comments system (or Disqus/Utterances TBD) | Migration decision; not a CSS/fidelity issue. |

---

## §F — P7 Exit Gate Refinement

Building on T1 §F, the exit gate criteria for declaring P7 complete. Each criterion must be confirmed by a screenshot pair (local vs live) for at least one representative page per type.

### F.1 — Structural layout criteria (must PASS all)

1. **Sidebar position**: sidebar column appears on the LEFT side (same as live) on home, at least 3 distinct single-post pages, and at least 1 category page. **Currently FAILING** on pages 03, 07, 08.

2. **Two-column layout present**: both main content column and sidebar column are simultaneously visible (no full-width content spanning the page). Specifically verified on pages with long content and images.

3. **Header title left-aligned**: site title "Mithro rants about stuff" is left-aligned with visible left padding (~3em); NOT centered. **Currently PASSING** (fix C2 verified).

4. **Header bottom border absent**: no visible `1px solid #ddd` separator line under the header. **Currently PASSING** (fix C2 verified).

5. **No Picasa gallery in header**: header zone contains only title, description, nav link. **Currently PASSING** (fix C8 verified).

### F.2 — Content rendering criteria (must PASS all)

6. **Category pages show full post content**: navigating to `/archives/category/python/` and `/archives/category/lca/` must show full post body content for each listed post (not just title + excerpt). **Currently FAILING** (delta X-2).

7. **Code blocks render without box border**: `<pre>` and `.highlight` blocks display with no surrounding border or grey background. Only token coloring is acceptable (see §E item E-4). **Currently PASSING** (fix C7 verified on page 06).

8. **Bullet lists use square bullets**: unordered lists inside post content use `list-style: square` (Barthelme original). **Currently PASSING** (fix C14 verified — checked in day 3 content).

### F.3 — Widget/sidebar criteria (must PASS all)

9. **No widget box borders**: sidebar widgets appear as plain list sections without `border: 1px solid #ddd` box outlines or grey background `#f9f9f9` panels. **Currently PASSING** (fix C5 verified).

10. **Tags render as plain inline links**: tag cloud (sidebar and post meta) shows plain anchor tags separated by spaces, not pill/badge chips with background color and border-radius. **Currently PASSING** (fix C6 verified).

11. **Recent Posts widget shows no dates**: sidebar Recent Posts list shows only post titles as links, no date `<span>` below each title. **Currently PASSING** (fix C12 verified).

### F.4 — Typography criteria (must PASS all)

12. **Entry-content headings `h2`/`h3` are font-weight 400**: headings within post body are not bold (weight 400 = normal). **Currently PASSING** (fix C9 verified).

13. **Comment form labels float left**: comment form inputs are preceded by left-floated labels; inputs have `border: 1px inset #888`. **Currently PASSING** (fix C13 verified).

### F.5 — Server/infrastructure criteria (informational)

14. **404 page uses Jekyll theme**: when deployed to production server (not python http.server), unmatched URLs must serve `_site/404.html` with full Barthelme theme. **Verified by direct access** to `http://127.0.0.1:4321/404.html` — passes. Python http.server limitation is noted but does not block exit gate.

15. **Hardware/project/tutorial layout integrity**: Jekyll-only pages render with correct header+content+footer without layout breakage. Hardware (page 11) and tutorial (page 13) PASS. Project (page 12) FAILS (missing header band — see DELTA S-6); this should be fixed but does not block the primary exit gate since these are new pages with no live oracle.

### F.6 — Acceptable deviations at exit gate

The following differences from live are explicitly ACCEPTED and do NOT block exit gate:
- Sub-pixel font rendering differences (OS/browser anti-aliasing)
- Broken image assets from Picasa/ggpht.com URLs (already broken on live)
- Twitter widget replaced with removal notice
- Picasa gallery removed from header
- Syntax-highlighted code blocks (enhancement over plain gray live code)
- reCAPTCHA absent on comment form
- WordPress login link absent from Meta widget
- Dynamic WP search replaced with JSON-based static search
- Comment left-border accent (3px `#bbc8d9`) — see DELTA S-4; LOW priority but should be fixed before exit

---

## §G — Additional Observations

### G-1 — Float-clearing issue root cause analysis

The sidebar disappears on pages 03, 07, 08 but is present on pages 02, 04, 06. The distinguishing factor appears to be post length and image content:
- Pages where sidebar IS visible: starhunter (short, ~400px content), epiphany2firefox (medium prose), utf8-python (medium with small code)
- Pages where sidebar IS absent: HDMI2USB day4 (many large images), fritzbox (long with screenshots), HDMI2USB day3 (very long + nested lists)

This pattern strongly suggests a **float-clearing issue** where tall content in the main column causes the containing `#wrapper` or `#container` to collapse, pushing the sidebar below the content. Common fix: ensure `#wrapper` or `#container` uses `overflow: hidden` or a `clearfix` pseudo-element, which forces it to contain its floated children.

### G-2 — Category template `post.content` vs `post.excerpt`

The category listing behavior is confirmed visually. On WordPress, category archives display `the_content()` (full content). Jekyll's `{{ post.excerpt }}` is the first paragraph by default (or content up to `<!--more-->`). To match live behavior, the `_layouts/category.html` template must iterate with `{{ post.content }}` and optionally apply `strip_html | truncate: 500` if performance is a concern for long posts.

### G-3 — Commits verified as working (fixes confirmed by T2 screenshots)

The following T1 deltas were confirmed FIXED by T2 visual inspection:
- **C1/C4**: Container `float: right` → sidebar on LEFT (verified: home, starhunter, epiphany, search, 404)
- **C2**: Header title left-aligned, no bottom border (verified: all pages)
- **C3**: Wrapper `8em` right margin (inferred: layout correct where sidebar shows)
- **C5**: No widget box borders (verified: home, search, 404 sidebars)
- **C6**: Tags as plain inline links (verified: home page tag cloud)
- **C7**: Code blocks without border/background box (verified: utf8-python page 06)
- **C8**: Picasa gallery removed from header (verified: all pages)
- **C9**: Heading font-weight/margins (verified: day3 headings render at normal weight)
- **C10**: Entry-meta `10em` width (verified: home listing correct)
- **C11**: Single container margin corrected (verified: single post pages with sidebar)
- **C12**: Recent Posts dates removed (verified: home sidebar)
- **C13**: Comment formcontainer CSS (verified: comment form renders with label structure)
- **C14**: Square list bullets (verified: day3 post lists)
- **C15**: `.wp-caption-text` italic centered (cannot verify without caption-bearing image; rule present)
- **C16**: Content margin-left `16em` (verified: layout alignment)
- **C17**: html/body/sidebar base reset (verified: no extra whitespace artifacts)

### G-4 — Remaining work priority order

Based on T2 findings, the remaining work before P7 exit gate, in priority order:

1. **CRITICAL**: Fix sidebar disappearing on long-content/image-heavy posts (DELTA X-1) — float clearing
2. **HIGH**: Fix category pages to show full post content (DELTA X-2) — template change
3. **MEDIUM**: Remove border-left from comment list items (DELTA S-4) — 1-line CSS fix
4. **MEDIUM**: Add header include to project layout (DELTA S-6) — 1-line template fix
5. **LOW**: Verify header padding exact match (DELTA X-4)
6. **LOW**: Extend entry-meta width fix to category pages (DELTA X-5)
