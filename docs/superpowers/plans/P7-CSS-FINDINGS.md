# P7-CSS-FINDINGS: Theme CSS Fidelity Delta Audit

**Date**: 2026-05-21  
**Branch**: `migration-p7-css-fidelity`  
**Method**: Playwright screenshot pairs (local `_site/` vs live `https://blog.mithis.net`)  
**Audit scope**: 13 representative pages across all major page types  

---

## §A — Method

### Screenshot capture
- **Viewport**: 1280×900 px (desktop)
- **Tool**: Playwright MCP (mcp__plugin_playwright_playwright__)
- **Full-page**: yes (`fullPage: true`)
- **Local server**: Python `http.server` on `http://127.0.0.1:4321` serving `_site/`
- **Screenshots stored**: `tmp/p7/` (gitignored)

### Oracle source per page

| Slug | Local URL | Live Oracle | Oracle status |
|------|-----------|-------------|---------------|
| home | `http://127.0.0.1:4321/` | `https://blog.mithis.net/` | Live (TLS expired, Playwright allowed) |
| archives | `http://127.0.0.1:4321/archives/` | no equivalent on live | Local-only; live used LCA category instead |
| category-lca | `http://127.0.0.1:4321/archives/category/lca/` | `https://blog.mithis.net/archives/category/lca` | Live |
| starhunter | `…/sci-fi/102-starhunter-fireflys-little-known-older-cousin.html` | `…/102-starhunter-fireflys-little-known-older-cousin` | Live |
| utf8python | `…/python/91-utf-8-in-python.html` | `…/python/91-utf-8-in-python` | Live |
| hdmi2usb-day4 | `…/timvideos-us/1995-hdmi2usb-production-board-bring-up-day-4…html` | live equivalent | Live |
| hdmi2usb-day3 | `…/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3…html` | live equivalent | Live |
| epiphany2ff | `…/uncategorized/77-epiphany2firefox.html` | live equivalent | Live |
| resume | `…/uncategorized/3-resume.html` | live equivalent | Live |
| fastcomplete | `…/useful-bits/407-fastcomplete.html` | live equivalent | Live |
| lca-resolutions | `…/lca/2167-timvideos-us-2016-new-years-resolutions.html` | live equivalent | Live |
| nmigen | `…/hardware/2186-nmigen-new-improved-by-whitequark.html` | live equivalent | Live |
| search | `http://127.0.0.1:4321/search.html` | no live `/search` page (404) | Local-only |

**Notes on URL differences**: Live site uses no `.html` suffix; Jekyll local serves `.html` files directly. Live site issued 301 redirects from trailing-slash URLs. No Wayback fallback needed — live site was accessible (TLS cert expired but Playwright connected).

---

## §B — Per-page Delta Catalog

### B1. Home page (`/`)

| Element | Live (oracle) | Local (_site) | Severity |
|---------|--------------|---------------|----------|
| **Header background** | Solid medium blue-grey (`#bbc8d9` approx), no border, full-width spanning entire header zone, padding visible top/left | Same color appears correct BUT header has a visible **bottom border `1px solid #ddd`** and a `text-align: center` applied via `#header { text-align: center; padding: 20px 0; border-bottom: 1px solid #ddd; }` (lines 974-978 main.css) — not present in Barthelme original | HIGH |
| **Header title alignment** | Title "Mithro rants about stuff" left-aligned, padded `3em` from left, no centering | Title is centered due to `#header { text-align: center }` in main.css lines 974-978; this overrides the structural left-alignment. Also, `body div#header` margin is `margin: 0 -2em 3em 0` (correct) but the overriding `#header` block at line 974 sets `text-align: center; padding: 20px 0` | HIGH |
| **Header photo strip** | Live shows a row of small square thumbnail photos (`~64px`) inside the header zone, from Picasa/Google Photos — they resolve visually as broken images (403s from lh3.ggpht.com) but the space/layout is present as a `div#header-photos` row with photo thumbnails and EXIF metadata text below each | Local also shows broken thumbnails in same location — structurally matched. BUT the layout differs: live uses the WordPress photo widget which renders in the **sidebar** not the header. Local has moved the photo gallery into the header HTML (`_includes/header.html`). The photos row appears BELOW the title on local (inside header), but on live the photos are in the sidebar. | HIGH |
| **Wrapper/layout right margin** | Live: `body div#wrapper` has `margin: 0 8em 0 0` (Barthelme original line 27) — provides wide right gutter for sidebar | Local: `body div#wrapper { margin: 0 2em 0 0 }` (main.css line 35) — only `2em` right margin instead of `8em`. This makes entire content area wider than expected, compressing the sidebar | HIGH |
| **Container float direction** | Live: `body div#container { float: right; … }` (Barthelme line 19) — sidebar is on LEFT | Local: `body div#container { float: left; … }` (main.css line 39) — reversed float direction. Sidebar on RIGHT in local. | HIGH |
| **Content left margin** | Live: `body div#content { margin: 0 0 0 16em; }` (Barthelme line 20) | Local: `body div#content { margin: 0 0 0 17em; }` (main.css line 45) — 1em wider | MEDIUM |
| **Sidebar position** | Live: Sidebar is a LEFT column (float left, content margin-left pushes past it) | Local: Sidebar is a RIGHT column due to `float: left` on container (reversed) — see container delta above | HIGH |
| **Sidebar widget styling** | Live: Sidebar items rendered as plain `<ul><li>` list — NO border, no `background: #f9f9f9`, no box. Widget titles (`h3`) are grey, small, uppercase plain text. Widget `<ul>` has `margin: 0 1.5em 0 3em`. | Local: Sidebar uses `.sidebar-widget` class with `border: 1px solid #ddd; background: #f9f9f9; padding: 1em` — each widget has a visible box/border. H3 titles have `border-bottom: 1px solid #ddd`. This is NOT in Barthelme original and creates visible widget boxes absent from the live site. | HIGH |
| **Tags cloud** | Live: Tags appear as plain inline text links separated by spaces (no borders, no background, no pill shape) | Local: Tags have `.tag-link` class with `background: #e0e0e0; border-radius: 3px; padding: 0.25em 0.5em` — styled as pill/chip badges. Not present in Barthelme original. | HIGH |
| **Recent Posts widget** | Live: Each post title as plain `<li>` link, NO date shown below it | Local: Each post has date in `<span class="post-date">` with `font-size: 0.8em; color: #999` shown below the link — extra element not in live | MEDIUM |
| **Footer** | Live: Single line footer, text `© 2026 | Thanks, WordPress | Barthelme theme by Scott | Standards Compliant XHTML & CSS | RSS Posts & Comments` — all lowercase, no separating borders | Local: Same text content — MATCHES footer HTML | LOW |
| **Post listing entry-meta column** | Live: Date column (`entry-meta`) is `width: 10em` (Barthelme line 35) | Local: Date column is `width: 7.5em` (main.css lines 223, 617) | MEDIUM |
| **Post listing post-container** | Live: `margin: 0 0 4em -11.5em` (Barthelme line 38) matching the 10em entry-meta | Local: `margin: 0 0 4em -8.5em` (main.css line 251) matching 7.5em date column | MEDIUM |
| **Post listing post-content left margin** | Live: `margin: 0 0 0 11.5em` (Barthelme line 39) | Local: `margin: 0 0 0 8.5em` (main.css line 259) | MEDIUM |
| **Single/page container margin** | Live: `body.single div#container, body.page div#container { margin: 0 0 6em -20em }` (Barthelme line 21) | Local: `margin: 0 0 0 -16em` (main.css line 50) — 6em bottom margin missing; -16em instead of -20em offset | MEDIUM |
| **Single/page content margin** | Live: `body.single div#content, body.page div#content { margin: 0 0 0 20em }` (Barthelme line 22) | Local: `margin: 0 0 0 17em` (main.css line 55) | MEDIUM |

### B2. Archives index (`/archives/`)

| Element | Live (oracle) | Local (_site) | Severity |
|---------|--------------|---------------|----------|
| **Header** | N/A (live has no `/archives/` page) | Shows all posts grouped by year/month — layout consistent with home-page issues above | — |
| **All cross-site issues** | See B1 | Header centering, sidebar position/styling, tag pills all present | HIGH |

### B3. Category page (`/archives/category/lca/`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **Header** | Left-aligned title, photo thumbnails in header (broken images but laid out inline), no bottom border | Centered title, photo thumbnails in header, visible `border-bottom: 1px solid #ddd` | HIGH |
| **Sidebar position** | LEFT side | RIGHT side | HIGH |
| **Sidebar widgets** | Plain `ul/li` lists, no box borders | Boxed widgets with borders and grey backgrounds | HIGH |
| **Content area** | Posts list with date column (`10em`) on left, titles and content to the right | Posts list with date column (`7.5em`) on left — narrower than live | MEDIUM |
| **Page title** | "{ Category Archives } linux.conf.au" centered with category description below | "{ Category Archives } linux.conf.au" present — text matches but styling matches otherwise | LOW |
| **Tag cloud** | Plain inline text tags | Pill-shaped badges | HIGH |

### B4. Comment-heavy post — Starhunter (`/archives/sci-fi/102-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **Header** | Same cross-site issues: left-aligned title, no bottom border | Centered title, bottom border | HIGH |
| **Sidebar** | LEFT column; plain widget lists | RIGHT column; boxed widgets | HIGH |
| **Comments section** | Original WP theme: `ol.commentlist li` with `background: #f6f7f9; margin: 1em 3em; padding: 0.5em 1em`. Alternating `li.alt` has `background: #e7eaed`. Comment metadata (`div.comment-meta`) is plain text. | Local has `.comment { background: #f9f9f9; border-left: 3px solid #bbc8d9; }` — adds prominent left border not in original. No alternating row colors. Uses flex `.comment-header` instead of plain div structure. | HIGH |
| **Comment meta / author** | `div.comment-meta span.comment-author { font-weight: 700 }` — author bold; date inline | Local uses `.comment-author { font-weight: bold }` + `.comment-date` in a flex row — visually similar but border-left accent stripe is foreign to original | MEDIUM |
| **Navigation prev/next** | Uppercase bold, centered, 45% wide divs | Matches Barthelme structure — OK | LOW |

### B5. Code-heavy post — UTF-8 in Python (`/archives/python/91-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar, tag pills | Same as B1 | HIGH |
| **Code blocks** | Rendered as plain `<pre><code>` with `font: 1em/150% "courier new"` — no border, no background shading | Local adds `.highlight { background: #f8f8f8; border: 1px solid #ddd; border-radius: 3px; padding: 1em }` — adds visible box around code blocks. The Barthelme original has NO boxed highlight. | HIGH |
| **Code font** | `font: 1em/150% "courier new", courier, monospace` | Same — matches | LOW |
| **Inline code** | Same mono font, no special background | Same | LOW |

### B6. Image-rich post — HDMI2USB Day 4 (`/archives/timvideos-us/1995-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar, tag pills, code highlights | Same as B1 | HIGH |
| **Images in content** | `div.entry-content img { overflow: hidden; max-width: 99% }` — no border, natural size up to 99% width | Local matches — `div.entry-content img { overflow: hidden; max-width: 99% }` — OK | LOW |
| **Image captions** | `.wp-caption-text { font-style: italic; margin: 0.2em auto 1em auto; text-align: center }` (Barthelme line 99) | NOT present in `main.css` — captions won't be italic/centered if they appear | MEDIUM |
| **Sidebar recent posts** | Live shows recent posts list without dates | Local shows dates under each post | MEDIUM |

### B7. Long-form post — HDMI2USB Day 3 (`/archives/timvideos-us/1993-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | See B1 | Same | HIGH |
| **Post content headings** | Barthelme: `div.entry-content h2, h3 { font-size: 1.4em; font-weight: 400; line-height: 150%; margin: 1.5em 0 -0.7em }` — note the **-0.7em bottom margin** producing tight headings | Local `main.css` does NOT have this rule — headings will have default browser margins (typically 0.83em top/bottom) not the tight Barthelme negative-bottom-margin style | HIGH |
| **Ordered list items in code sections** | `div.entry-content ul li { list-style: square }` (Barthelme line 134) | NOT in `main.css` — lists use browser default (disc/decimal) instead of square bullets | MEDIUM |

### B8. Liquid-fix post — Epiphany2Firefox (`/archives/uncategorized/77-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar | Same | HIGH |
| **Post body text** | Appears as plain text paragraphs | Local appears similar — content renders correctly | LOW |
| **Comments form** | Barthelme: `div.formcontainer` with `div.form-input input`, `div.form-label`, `div.form-submit` — structured form with left-floating label (`width: 6em`) and input (`width: 50%; border: 1px inset #888`) | Local has no `.formcontainer` / `.form-label` / `.form-input` CSS in `main.css`. Comment form uses different HTML structure — may render but styling differs | HIGH |

### B9. Short post — Resume (`/archives/uncategorized/3-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar | Same | HIGH |
| **Page title order** | Live: `{date} — {title}` — date shown centered above the title as a separate `div.entry-date` | Local: Same ordering — matches | LOW |
| **Very sparse content** | One-liner body, no images, no code — layout differences mostly from header/sidebar | Same | LOW |
| **Comment form structure** | `div.formcontainer` with label floats | Missing CSS rules as noted in B8 | HIGH |

### B10. Code post with headings — FastComplete (`/archives/useful-bits/407-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar, highlight boxes | Same | HIGH |
| **Content headings h3** | `font-size: 1.4em; font-weight: 400; margin: 1.5em 0 -0.7em` — tight to next paragraph | No such rule in local — normal browser heading margin applies | HIGH |
| **`<pre>` blocks** | No background, no border — raw Barthelme styling | Local adds bordered `.highlight` box | HIGH |

### B11. Medium post — LCA Resolutions (`/archives/lca/2167-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar, tag pills | Same | HIGH |
| **Bullet lists** | `list-style: square` (Barthelme) | Default disc (browser default) in local | MEDIUM |
| **Sidebar** | LEFT column | RIGHT column | HIGH |

### B12. Short hardware post — nMigen (`/archives/hardware/2186-…`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **All cross-site issues** | Header, sidebar | Same | HIGH |
| **Comment form** | `div.formcontainer` structure | Missing CSS | HIGH |
| **Entry body text links** | `div#content a { color: #546188 }` — correct | Matches | LOW |

### B13. Search page (`/search.html`)

| Element | Live | Local | Severity |
|---------|------|-------|----------|
| **Search form** | Not present on live (404) | Local shows a search input and results scaffold | N/A |
| **All cross-site issues** | N/A for live | Header centering, sidebar right, tag pills present | HIGH |

---

## §C — Whole-Corpus Pattern (cross-page deltas)

Ranked by visual impact × scope (how many of the 13 pages affected):

| # | Delta | Pages affected | Severity |
|---|-------|---------------|----------|
| C1 | **Sidebar on WRONG side (RIGHT instead of LEFT)** | ALL 13 | HIGH |
| C2 | **Header title centered instead of left-aligned; spurious bottom border** | ALL 13 | HIGH |
| C3 | **Wrapper right margin `2em` instead of `8em`** — shrinks entire layout | ALL 13 | HIGH |
| C4 | **Container float direction reversed (`float:left` vs `float:right`)** | ALL 13 | HIGH |
| C5 | **Sidebar widgets have box borders + grey background** (`.sidebar-widget` CSS) — not in Barthelme | ALL 13 | HIGH |
| C6 | **Tags rendered as pill/badge chips** (`.tag-link` with background + border-radius) — not in Barthelme | ALL 13 (sidebar) | HIGH |
| C7 | **Code/pre blocks have border + background box** (`.highlight` class CSS) — not in Barthelme original | All code posts (~8) | HIGH |
| C8 | **Photo gallery placed in HEADER HTML** instead of sidebar (as on live site) | ALL 13 | HIGH |
| C9 | **Content heading `h2/h3` missing `font-weight:400; margin: 1.5em 0 -0.7em`** | All posts with headings (~6) | HIGH |
| C10 | **`entry-meta` date column width `7.5em` instead of `10em`**; post-container/post-content margins mismatched | Home + archive list pages (~4) | MEDIUM |
| C11 | **`body.single` container margin `-16em` instead of `-20em`; missing `6em` bottom margin** | All single post pages (~10) | MEDIUM |
| C12 | **Recent Posts sidebar widget shows post dates** — not present on live | ALL 13 | MEDIUM |
| C13 | **Comment form lacks `.formcontainer` CSS** (label floats, inset border inputs) | All pages with comment forms (~10) | HIGH |
| C14 | **`ul li` list-style not `square`** — missing Barthelme list bullet rule | Posts with lists (~6) | MEDIUM |
| C15 | **`.wp-caption-text` rule missing** — image captions won't be italic/centered | Image-rich posts (~4) | MEDIUM |
| C16 | **`body div#content margin-left: 17em` instead of `16em`** | ALL 13 | LOW |
| C17 | **`body.single div.entry-date` `word-spacing` missing** from Barthelme | All single posts (~10) | LOW |

---

## §D — Root-Cause Hypotheses per Delta

| Delta | Root Cause | File(s) |
|-------|-----------|---------|
| **C1 — Sidebar wrong side** | `body div#container { float: left }` in `main.css` line 39. Barthelme has `float: right`. The container floats **right** so the sidebar (floated left) appears on the **left** of the container. Current `float:left` pushes the sidebar right. | `assets/css/main.css` line 39 |
| **C2 — Header centering + border** | Duplicate/override `#header { text-align: center; padding: 20px 0; border-bottom: 1px solid #ddd; }` at lines 974–978 of `main.css` overrides the structural `body div#header` rule. The selector `#header` (ID, high specificity) overrides `body div#header`. Barthelme original has `body div#header { margin: 3em -2em 3em 0; padding: 1.2em 0 1.2em 3em }` — left-padded, no centering, no border. | `assets/css/main.css` lines 974–978 (delete/replace); `assets/css/main.css` lines 59–63 (fix padding) |
| **C3 — Wrapper margin** | `body div#wrapper { margin: 0 2em 0 0 }` (line 35). Barthelme: `margin: 0 8em 0 0`. The 8em right gutter is what leaves room for the left-floated sidebar. With only 2em, the layout collapses. | `assets/css/main.css` line 35 |
| **C4 — Container float reversed** | See C1. Same root cause. `float: left` → should be `float: right`. | `assets/css/main.css` line 39 |
| **C5 — Sidebar widget boxes** | `.sidebar-widget { border: 1px solid #ddd; background: #f9f9f9; padding: 1em }` (lines 293–298) was added as a "nicety" not present in Barthelme. The Barthelme sidebar uses plain `div.sidebar ul li` styling (no boxes). The sidebar HTML uses class `widget` not `sidebar-widget`; so this may not be applying anyway. But the `#sidebar` block (`float:left; width:15em; padding:0 1em 0 0`) at line 286–291 is a duplicate/conflicting selector alongside `body div.sidebar`. | `assets/css/main.css` lines 286–370 (sidebar widget block — needs removal/replacement with Barthelme's `div.sidebar ul li` rules) |
| **C6 — Tag pill badges** | `.tag-link { background: #e0e0e0; border-radius: 3px; padding: 0.25em 0.5em }` (lines 354–368). The Barthelme original has NO `.tag-link` class. Tags are rendered as plain inline `<a>` links separated by spaces. The `tag-cloud` and `tag-link` classes are a custom addition. | `assets/css/main.css` lines 350–368 (remove pill styling, replace with plain inline links per Barthelme) |
| **C7 — Code block boxes** | `.highlight { background: #f8f8f8; border: 1px solid #ddd; border-radius: 3px; padding: 1em }` (lines 447–454). Barthelme original has NO `.highlight` wrapper rule — code is `font: 1em/150% "courier new"` only. The Rouge lexer wraps code in `.highlight` divs which is fine, but the border+background styling is not Barthelme. | `assets/css/main.css` lines 447–454 (remove border/background from `.highlight`, keep only rouge token colors) |
| **C8 — Photos in header** | `_includes/header.html` puts a `.photo-gallery` div inside `#header`. On the live WP site, the photo widget is in the sidebar (WordPress widget area). The header HTML should only contain `h1#blog-title`, `div#blog-description`, and `div#header-nav`. | `_includes/header.html` (remove `#header-photos` div from header); `_includes/sidebar.html` (add photo widget in correct sidebar position if desired, or remove entirely as a removed feature) |
| **C9 — Heading margins** | `div.entry-content h2, h3` are missing `font-weight: 400; line-height: 150%; margin: 1.5em 0 -0.7em` from Barthelme lines 83–84. The `main.css` has no corresponding rule for entry-content headings. | `assets/css/main.css` (add missing heading rule) |
| **C10 — Date column width** | `body.home div#content div.entry-meta { width: 7.5em }` vs Barthelme's `width: 10em`. Also post-container margin `-8.5em` vs `-11.5em`, and post-content margin `8.5em` vs `11.5em`. These three values must change together atomically. | `assets/css/main.css` lines 223, 251, 259 (home/archive listing section) and lines 617, 622, 628 (duplicate block) |
| **C11 — Single container margin** | `body.single div#container { margin: 0 0 0 -16em }` vs Barthelme `margin: 0 0 6em -20em`. And `body.single div#content { margin: 0 0 0 17em }` vs `0 0 0 20em`. | `assets/css/main.css` lines 49–56 |
| **C12 — Recent Posts dates** | `_includes/sidebar.html` line 117 outputs `<span class="post-date">…</span>` with date. Live WP sidebar shows only title with no date. | `_includes/sidebar.html` line 116–117 (remove `post-date` span); `assets/css/main.css` lines 371–376 (`.post-date` rule can be removed) |
| **C13 — Comment form styling** | `main.css` lacks the Barthelme `div.formcontainer` rules (lines 116–121 of Barthelme original): form-input/form-label float layout, `border: 1px inset #888` on inputs, 50% width inputs. | `assets/css/main.css` (add formcontainer rules) |
| **C14 — List bullets** | `div.entry-content ul li { list-style: square }` (Barthelme line 134) and `ul li ul li { list-style: circle }` (line 135) are not in `main.css`. | `assets/css/main.css` (add list-style rules) |
| **C15 — wp-caption-text** | `.wp-caption-text { font-style: italic; margin: 0.2em auto 1em auto; text-align: center }` (Barthelme line 99) absent from `main.css`. | `assets/css/main.css` (add wp-caption-text rule) |
| **C16 — Content margin 1em off** | `body div#content { margin: 0 0 0 17em }` vs Barthelme `16em`. Off by 1em — minor but measurable. | `assets/css/main.css` line 45 |
| **C17 — body/html/sidebar reset** | Barthelme line 136: `div.sidebar ul li p, div.sidebar ul li ul, div.sidebar ul li ul li, html, body, div.formcontainer form#commentform, div.sidebar ul li#search form#searchform { margin: 0; padding: 0 }`. This reset rule is absent from `main.css`, potentially causing sidebar indent/spacing issues. | `assets/css/main.css` (add margin/padding reset for sidebar and html/body) |

---

## §E — Proposed Fix Sequence

Ordered by highest cross-page visual impact first. Estimated complexity: S=small (1–5 lines), M=medium (5–20 lines), L=large (20+ lines or structural change).

| # | Delta(s) | Change description | File(s) | Complexity | Expected screenshot impact |
|---|----------|-------------------|---------|------------|---------------------------|
| 1 | C1, C3, C4 | Fix layout core: set `body div#wrapper { margin: 0 8em 0 0 }` and `body div#container { float: right; margin: 0 0 5em -16em }` — matches Barthelme exactly | `assets/css/main.css` lines 35, 39 | S | Sidebar moves to LEFT on all 13 pages — biggest single impact |
| 2 | C2 | Remove/replace the rogue `#header { text-align: center; padding: 20px 0; border-bottom: 1px solid #ddd }` block (lines 974–978). Fix `body div#header` padding to match Barthelme `padding: 1.2em 0 1.2em 3em` (not the current `0`). Add `color` rules for title/description to match Barthelme (they appear to be white on the blue-grey background). | `assets/css/main.css` lines 59–110, 974–978 | S | Header title left-aligns, bottom border disappears — all 13 pages |
| 3 | C8 | Remove `#header-photos` div from `_includes/header.html` (lines 7–69). Header should only contain: `h1#blog-title`, optional `div#blog-description`, `div#header-nav` | `_includes/header.html` | S | Photo gallery removed from header — cleaner header matching Barthelme |
| 4 | C11 | Fix single/page container and content margins: `body.single div#container { margin: 0 0 6em -20em }` and `body.single div#content { margin: 0 0 0 20em }` | `assets/css/main.css` lines 49–56 | S | Single post layout widens to match live — all single post pages |
| 5 | C10 | Fix listing date-column widths: entry-meta `width: 10em`, post-container `margin: 0 0 4em -11.5em`, post-content `margin: 0 0 0 11.5em` — update both duplicate blocks (lines 217–260 and lines 613–632) | `assets/css/main.css` two blocks | S | Home and archive listing layout tightened to match live |
| 6 | C5 | Remove `.sidebar-widget` box styling (lines 293–298) or reduce to plain styling; add Barthelme's `div.sidebar ul li { margin: 0 0 1.5em; list-style: none; font-size: 1em; line-height: 175% }` and `div.sidebar ul li h3 { color: #777; font-size: 1em; text-transform: uppercase }` | `assets/css/main.css` lines 285–332 (replace sidebar widget block) | M | Widget boxes disappear; sidebar matches live plain list style |
| 7 | C6 | Remove `.tag-link` pill styling (lines 354–368); tags in sidebar/content should be plain inline links | `assets/css/main.css` lines 350–368 | S | Tag cloud becomes plain text inline links matching live |
| 8 | C7 | Remove border/background from `.highlight` block (lines 447–454): keep only `overflow-x: auto; margin: 1em 0` — drop `background`, `border`, `border-radius`, `padding` | `assets/css/main.css` lines 447–454 | S | Code blocks lose box styling — matches live's unbordered code | 
| 9 | C9 | Add missing heading rules for entry-content: `div.entry-content h2, div.entry-content h3 { font-size: 1.4em }` and `div.entry-content h2, div.entry-content h3, div.entry-content h4, div.entry-content h5, div.entry-content h6 { font-weight: 400; line-height: 150%; margin: 1.5em 0 -0.7em }` | `assets/css/main.css` (add new block) | S | Headings tighten in posts — all posts with h2/h3/h4 |
| 10 | C13 | Add Barthelme `div.formcontainer` rules for comment form: form-label float, form-input widths, inset border | `assets/css/main.css` (add ~8 lines) | S | Comment form labels properly aligned |
| 11 | C14 | Add `div.entry-content ul li { list-style: square }` and `div.entry-content ul li ul li { list-style: circle }` | `assets/css/main.css` (add 2 lines) | S | Bullets change from disc to square — posts with lists |
| 12 | C15 | Add `.wp-caption-text { font-style: italic; margin: 0.2em auto 1em auto; text-align: center }` | `assets/css/main.css` (add 1 block) | S | Image captions italic/centered |
| 13 | C12 | Remove `post-date` span from Recent Posts sidebar template; remove `.post-date` CSS rule | `_includes/sidebar.html` line 116–117; `assets/css/main.css` lines 371–376 | S | Dates removed from Recent Posts widget — matches live |
| 14 | C16 | Fix `body div#content { margin: 0 0 0 16em }` (currently 17em) | `assets/css/main.css` line 45 | S | 1em alignment correction across all pages |
| 15 | C17 | Add Barthelme base reset: `html, body { margin: 0; padding: 0 }` and `div.sidebar ul li p, div.sidebar ul li ul, div.sidebar ul li ul li { margin: 0; padding: 0 }` | `assets/css/main.css` (add ~5 lines near top) | S | Baseline spacing normalised |
| 16 | — | Add missing Barthelme font rules: `body { font-family: arial, helvetica, sans-serif; font-size: 100% }` (already present but verify) and check `body div#header, body div label, input#s, input#submit { cursor: pointer }` | `assets/css/main.css` | S | Minor cursor behaviour fix |

**Total fix-sequence items**: 16  
**Estimated total complexity**: 1 L (structural), 1 M (sidebar widget block), 14 S (small targeted rules)  
**Aggregate lines to change**: approximately 40–60 lines of CSS + 2 HTML template touches

---

## §F — P7 Exit Gate

**Definition of "done" for P7:**

For each of the 13 audit pages listed in §A, a side-by-side Playwright screenshot pair (local `_site/` vs live `https://blog.mithis.net`) must show:

1. **Layout structure matches**: sidebar is on the LEFT in both; content column occupies the same relative width; no extra right-hand column appears in local.
2. **Header matches**: title is left-aligned (padded ~3em from left); background color `#bbc8d9` (or equivalent); NO bottom border; no centering applied; photo strip is absent (it was a live WordPress widget — removed feature).
3. **Sidebar widget appearance matches**: no border boxes around widgets; h3 titles are small uppercase grey text; tag cloud is plain inline links.
4. **Code blocks match**: no border/background box around `<pre>` or `.highlight` blocks.
5. **Body text headings match**: `h2/h3` inside post content are `font-weight: 400` and have tight negative bottom margin.
6. **Footer text matches**: one-line footer identical to live.
7. **Comment form structure** (where present): label left-floated, inputs with inset border — or structurally equivalent.
8. **Acceptable deviations** (do not block exit gate):
   - Sub-pixel font rendering differences due to OS/browser differences
   - Broken image assets (Picasa/ggpht.com URLs returning 403 — these were already broken on live)
   - reCAPTCHA widget (live WP comment form has it; Jekyll version does not — acceptable)
   - Twitter widget (removed feature — note in sidebar is acceptable)
   - WordPress login link in Meta widget (live WP; Jekyll note is acceptable)
   - Any dynamic/JS widget that was a WordPress plugin

---

## §G — Additional Observations

### G1 — Duplicate CSS blocks
`main.css` has two near-identical blocks for home/archive entry-meta layout (lines 217–260 and lines 613–632). One is the canonical location; the other is likely a copy that was not kept in sync. Both must be updated together or the second one deleted.

### G2 — `{% include syntax-highlighting.css %}` on line 894
This Liquid include tag is embedded inside a `.css` file (not `.scss`/Jekyll-processed). It will be output literally as `{% include syntax-highlighting.css %}` in the browser — this is a bug. If this file actually runs through Jekyll (it has `---\n---` front matter on lines 1–2, so it does), the include will be resolved. Verify this resolves correctly, or move syntax highlighting to a separate `<link>` tag.

### G3 — `body.single div#container` bottom margin gap
Barthelme uses `margin: 0 0 6em -20em` — the `6em` bottom gives breathing room before the footer on single post pages. The current `margin: 0 0 0 -16em` omits this and will cause the footer to appear too close to the last comment on long posts.

### G4 — `body div#wrapper` margin interaction with Barthelme original
The `8em` right margin on `#wrapper` combined with `body div.sidebar { float: left; width: 15em }` creates the two-column layout in Barthelme. The wrapper right margin reserves space for the sidebar even before any content is loaded, preventing layout shift. Restoring this is prerequisite to fixes C1/C4 working correctly.
