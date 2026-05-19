# P2 M1/M2 Category Fidelity Findings

**Date:** 2026-05-19
**Branch:** migration-p2-content-fidelity
**Tasks:** M1 (category internal-link + casing reconciliation) and M2 (category descriptive-prose decision)
**Oracle:** https://blog.mithis.net (TLS cert expired; fetched with `curl -sk`)

---

## Data Collection Notes

- 19 category slugs from `git ls-files | grep -E '^category/[a-z0-9-]+\.md$'`
- All 19 live pages fetched to `tmp/p2-oracle/m12-<slug>.html`
- HTML structure of every live category archive page:
  ```html
  <h2 class="page-title">
    <span class="archive-meta"><span class="meta-sep">{</span> Category Archives <span class="meta-sep">}</span></span>
    DisplayName
  </h2>
  <div class="archive-meta"><p>description text (may be empty)</p></div>
  ```
- `rcs-darcs` slug returns HTTP 404 because WP stored it as a **hierarchical** category `RCS > darcs` at URL `/archives/rcs/darcs`, not `/archives/category/rcs-darcs`.
- Similarly, `timvideos-us` has a sub-category `HDMI2USB` at `/archives/category/timvideos-us/hdmi2usb`. This sub-category is NOT in the Jekyll migration as a separate `category/*.md` file but appears in some live post category links.

---

## 1. Per-Category Oracle Table

| slug | live HTTP | oracle display name | oracle category URL path | current .md title | title match? | oracle description (verbatim; empty = WP stored none) | .md has `description:`? | .md body prose (verbatim or none) | body == faithful desc? |
|---|---|---|---|---|---|---|---|---|---|
| diary | 200 | Diary | /archives/category/diary | Diary | YES | _(empty)_ | NO | none | N/A |
| games | 200 | Games | /archives/category/games | Games | YES | _(empty)_ | NO | Posts about game development and gaming projects. | N/A — invented prose, no faithful desc |
| gaming-miniconf | 200 | Gaming Miniconf | /archives/category/gaming-miniconf | Gaming Miniconf | YES | _(empty)_ | NO | Posts about Gaming Miniconf events and game development. | N/A — invented prose |
| google | 200 | Google | /archives/category/google | Google | YES | _(empty)_ | NO | none | N/A |
| hardware | 200 | Hardware | /archives/category/hardware | Hardware | YES | _(empty)_ | NO | Posts about hardware development, electronics, and open source hardware projects. | N/A — invented prose |
| highlights | 200 | Highlights | /archives/category/highlights | Highlights | YES | _(empty)_ | NO | none | N/A |
| ideas | 200 | Ideas | /archives/category/ideas | Ideas | YES | Proposals which I'll probably never get around to implementing. | NO | none | N/A (no body prose) |
| lca | 200 | linux.conf.au | /archives/category/lca | LCA | **NO** | Linux.conf.au is the best Linux conference I have been too. | NO | Posts related to Linux.conf.au (LCA) conferences and events. | NO — invented prose differs from oracle desc |
| pcb | 200 | PCB | /archives/category/pcb | PCB | YES | _(empty)_ | NO | none | N/A |
| python | 200 | Python | /archives/category/python | Python | YES | _(empty)_ | NO | none | N/A |
| rcs-darcs | **404** | HTTP-404 (hierarchical: slug=`darcs`, parent=`RCS`) | /archives/rcs/darcs (NOT /archives/category/rcs-darcs) | RCS / Darcs | **NO** — no simple mapping | darcs desc: "Darcs is revision control system I use to use before converting to git." | NO | none | N/A |
| sci-fi | 200 | **Sci Fi** (no hyphen) | /archives/category/sci-fi | Sci-Fi | **NO** — hyphen differs | All things Science Fiction (TV, books and even games). | NO | none | N/A |
| summer-of-code | 200 | Summer of Code | /archives/category/summer-of-code | Summer of Code | YES | _(empty)_ | NO | Posts about Google Summer of Code projects and experiences. | N/A — invented prose |
| timvideos-us | 200 | TimVideos.us | /archives/category/timvideos-us | TimVideos.us | YES | TimVideos.us is a group of exciting projects which together create a system for doing both recording and live event streaming for conferences, meetings, user groups and other presentations. | NO | Posts about TimVideos.us project - open source video capture and streaming hardware. | NO — invented prose differs from oracle desc |
| tp | 200 | Thousand Parsec | /archives/category/tp | TP | **NO** | Thousand Parsec is a space empire building framework which I lead. | NO | none | N/A |
| ubuntu | 200 | Ubuntu | /archives/category/ubuntu | Ubuntu | YES | _(empty)_ | NO | Posts about Ubuntu Linux distribution and related technologies. | N/A — invented prose |
| uncategorized | 200 | Uncategorized | /archives/category/uncategorized | Uncategorized | YES | _(empty)_ | NO | none | N/A |
| uni | 200 | Uni | /archives/category/uni | Uni | YES | _(empty)_ | NO | none | N/A |
| useful-bits | 200 | Useful Bits | /archives/category/useful-bits | Useful Bits | YES | _(empty)_ | NO | Useful technical tips, tricks, and helpful information for developers and engineers. | N/A — invented prose |

### Summary Counts

- **Live archive 200:** 18 slugs
- **Live archive 404:** 1 slug (rcs-darcs — hierarchical WP category, see edge cases below)
- **Current .md title differs from oracle:** 3 slugs (lca, sci-fi, tp) + 1 edge-case (rcs-darcs)
- **Slugs with faithful non-empty oracle description to restore:** 5 (ideas, lca, sci-fi, timvideos-us, tp) + rcs-darcs (see edge case)
- **Slugs with invented Jekyll-era body prose to remove:** 8 (games, gaming-miniconf, hardware, lca, summer-of-code, timvideos-us, ubuntu, useful-bits)
- **Slugs with `description:` in current front matter:** 0 (none of the 19 have it)

---

## 2. Analysis: M1 Decision — URL Space and Category Link Reconciliation

### M1 Decision

**The faithful category URL space is `/archives/category/<slug>`.** This is baseurl-independent (no baseurl prefix is needed in the permalink value; Jekyll `relative_url` filter handles baseurl at render time). The current `/category/<slug>/` permalink space is wrong and produces 404s against the live WP URL structure.

**Reconciliation required:**

1. **Every `category/<slug>.md`:** change `permalink: /category/<slug>/` → `permalink: /archives/category/<slug>/` (keep trailing slash for directory-style URLs, matching WP's 301 → trailing-slash redirect pattern observed from `curl -sk -I`).

2. **`_layouts/home.html` line 34:** The href already uses `/archives/category/` (faithful path) but the display uses `{{ category | replace: '-', ' ' | title }}` — a lossy slug-filter. Replace display with the category page's `page.title` by looking up `site.pages | where: "category", category | first` OR simplest: use a site data lookup. **The one rule: display = the stored `title:` from `category/<slug>.md` (no slug filter).** The href already correct at line 34 but it links against `category | slugify` which may lose capitalization in slugs — confirm `lca` slugifies correctly (it does since the slug is already lowercase).

3. **`_layouts/post.html` line 48:** Currently links to `/category/<raw>` — must change to `/archives/category/<category | slugify>` and display `{{ category }}`. But `category` in post front matter is the raw slug string (e.g. `lca`, `timvideos-us`), not the display name. To display the faithful display name without a filter, the implementer must either:
   - Look up `site.pages | where: "category", category | first` and use that page's `.title`, OR
   - Keep the raw slug as display (unfaithful for `lca`, `sci-fi`, `tp`) — NOT acceptable.
   - **Recommended:** Use Jekyll page lookup: `{% assign cat_page = site.pages | where: "category", category | first %}` and output `{{ cat_page.title | default: category }}`.

4. **`_layouts/category.html` line 35 (within-category cross-links):** Currently links to `/category/<cat>` with `| replace: '-', ' ' | capitalize` display — both wrong. Fix href to `/archives/category/<cat | slugify>`, display to page lookup title.

5. **`_includes/sidebar.html` lines 34–51:** All category dropdown `value=` URLs use `/category/<slug>/` — must change to `/archives/category/<slug>/`. Display names (option text) are already manually authored correctly (e.g. "linux.conf.au", "Sci Fi") in the sidebar — but should be verified against oracle after title fixes.

6. **Category feed permalinks `category/<slug>/feed.xml`:** Currently `permalink: /category/<slug>/feed/`. Must change to `permalink: /archives/category/<slug>/feed/`. The live WP site uses `/archives/category/lca/feed` (HTTP 301 to no-trailing-slash confirmed). Check: all 19 `category/*/feed.xml` files share same pattern.

### Edge Cases for rcs-darcs

**`rcs-darcs` is a hierarchical WP category `RCS > darcs`.** Key facts:
- Live WP: `/archives/category/rcs-darcs` → **HTTP 404** (WP never registered this slug)
- Live WP actual URL: `/archives/rcs/darcs` → HTTP 200, display name "darcs", description "Darcs is revision control system I use to use before converting to git."
- Parent category `RCS` lives at `/archives/rcs` (no `/archives/category/` prefix — WP hierarchical URL structure)
- The darcs post permalink is `/archives/rcs/darcs/19-darcs-almost-perfect` (confirmed in post front matter)
- The Jekyll migration flattened this to slug `rcs-darcs`, which has no valid WP URL

**P2 vs P4 scope:** The hierarchical URL structure (`/archives/rcs/darcs` vs `/archives/category/rcs-darcs`) is fundamentally a URL-structure/redirect problem. **Recommend: defer the URL of the `rcs-darcs` category page itself to P4.** In P2, set `permalink: /archives/category/rcs-darcs/` with a note that P4 must create a redirect from `/archives/rcs/darcs` → `/archives/category/rcs-darcs/` (or, alternatively, change the permalink to `/archives/rcs/darcs/` and treat it as a faithful restoration). Either way, the display name (`title:`) should be updated to "darcs" (the faithful oracle sub-category name) and parent "RCS" acknowledged. The current title "RCS / Darcs" is a Jekyll-invented compound. For P2 correctness, **set title to "darcs"** (the actual WP sub-category name displayed on the page at `/archives/rcs/darcs`); flag for P4 to handle the hierarchical URL.

**`timvideos-us/hdmi2usb` sub-category:** This sub-category exists on the live site at `/archives/category/timvideos-us/hdmi2usb` (HTTP 200, display name "HDMI2USB"). Several live posts show `<a href="https://blog.mithis.net/archives/category/timvideos-us/hdmi2usb" rel="category tag">HDMI2USB</a>` in their `cat-links`. In the Jekyll migration, no `category/hdmi2usb.md` (or `category/timvideos-us/hdmi2usb.md`) exists, and no post in `_posts/` has `hdmi2usb` in its `categories:` array. **Recommend: defer to P4** (URL-structure phase) since this requires creating a new sub-category page AND adding `hdmi2usb` back to the affected post `categories:` arrays — that touches post content and is out of M1/M2 scope. Flag clearly for P4.

---

## 3. Analysis: M2 Decision — Category Descriptive Prose

### M2 Decision

**The live original WP site rendered `category_description()` in `<div class="archive-meta">` for every category page.** The faithful resolution is:

1. **Add `description:` front matter** to each `category/<slug>.md` set to the verbatim oracle value (empty string `""` where the oracle `<div class="archive-meta">` is empty, since `category.html` already handles empty gracefully with `{% if page.description and page.description != "" %}`).
2. **Remove all invented Jekyll-era body prose** (content after the second `---`). The `category.html` layout reads `page.description`, not `page.content`, so the body is dead code and unfaithful.
3. **Do NOT add `description:` for categories where the oracle description is empty** — or add it as `description: ""` explicitly. Both are equivalent; the layout already handles absence. For explicitness, recommend adding `description: ""` to all 14 empty-description categories so the data model is uniform.

### Per-Slug Exact Values to Set

#### Faithful `title:` (oracle display name) — changes from current

| slug | CURRENT title | SET title to | YAML note |
|---|---|---|---|
| diary | Diary | Diary | no change |
| games | Games | Games | no change |
| gaming-miniconf | Gaming Miniconf | Gaming Miniconf | no change |
| google | Google | Google | no change |
| hardware | Hardware | Hardware | no change |
| highlights | Highlights | Highlights | no change |
| ideas | Ideas | Ideas | no change |
| **lca** | **LCA** | **linux.conf.au** | use `title: linux.conf.au` (unquoted OK; lowercase, no special chars) |
| pcb | PCB | PCB | no change |
| python | Python | Python | no change |
| **rcs-darcs** | **RCS / Darcs** | **darcs** | use `title: darcs`; flag P4 for URL/hierarchy |
| **sci-fi** | **Sci-Fi** | **Sci Fi** | use `title: "Sci Fi"` (no hyphen; double-quote to be safe) |
| summer-of-code | Summer of Code | Summer of Code | no change |
| timvideos-us | TimVideos.us | TimVideos.us | no change |
| **tp** | **TP** | **Thousand Parsec** | use `title: Thousand Parsec` |
| ubuntu | Ubuntu | Ubuntu | no change |
| uncategorized | Uncategorized | Uncategorized | no change |
| uni | Uni | Uni | no change |
| useful-bits | Useful Bits | Useful Bits | no change |

**4 title changes required:** lca, rcs-darcs, sci-fi, tp.

#### Faithful `description:` to set (verbatim oracle; YAML-safe format)

> **CORRECTION (2026-05-19, post-implementation review):** the `ideas`
> description's apostrophe is the typographic RIGHT SINGLE QUOTATION MARK
> **U+2019** (the live oracle emits `&#8217;` — WordPress auto-curly-quote),
> NOT the ASCII `'` (U+0027) that the tables/code-blocks in this doc render
> at lines 37/148/208/416. The implementation (commit `b747390`) correctly
> uses U+2019 and byte-matches the oracle; the ASCII shown below is a
> doc-rendering artifact only. Treat the oracle (U+2019) as authoritative
> for `ideas`.

| slug | SET `description:` to | YAML-quoting note |
|---|---|---|
| diary | `""` | empty |
| games | `""` | empty |
| gaming-miniconf | `""` | empty |
| google | `""` | empty |
| hardware | `""` | empty |
| highlights | `""` | empty |
| ideas | `"Proposals which I'll probably never get around to implementing."` | **HAS APOSTROPHE → must use double-quotes** |
| lca | `'Linux.conf.au is the best Linux conference I have been too.'` | single-quote OK |
| pcb | `""` | empty |
| python | `""` | empty |
| rcs-darcs | `'Darcs is revision control system I use to use before converting to git.'` | single-quote OK (description from `/archives/rcs/darcs`) |
| sci-fi | `'All things Science Fiction (TV, books and even games).'` | single-quote OK |
| summer-of-code | `""` | empty |
| timvideos-us | `'TimVideos.us is a group of exciting projects which together create a system for doing both recording and live event streaming for conferences, meetings, user groups and other presentations.'` | single-quote OK; long line |
| tp | `'Thousand Parsec is a space empire building framework which I lead.'` | single-quote OK |
| ubuntu | `""` | empty |
| uncategorized | `""` | empty |
| uni | `""` | empty |
| useful-bits | `""` | empty |

**5 non-empty descriptions to add:** ideas, lca, sci-fi, timvideos-us, tp (+ rcs-darcs as edge case).
**14 empty-string descriptions to add** (or omit — layout handles absence; recommend adding explicitly for uniformity).

---

## 4. Exact Remediation Worklist

### 4A. `category/<slug>.md` changes — all 19 files

For each file: (a) update `permalink:`, (b) update `title:` if changed, (c) add `description:` front matter, (d) remove body prose if present.

**Files requiring NO title change (15 slugs):**

```
category/diary.md
  permalink: /archives/category/diary/
  description: ""
  [no body to remove]

category/games.md
  permalink: /archives/category/games/
  description: ""
  REMOVE body: "Posts about game development and gaming projects."

category/gaming-miniconf.md
  permalink: /archives/category/gaming-miniconf/
  description: ""
  REMOVE body: "Posts about Gaming Miniconf events and game development."

category/google.md
  permalink: /archives/category/google/
  description: ""
  [no body to remove]

category/hardware.md
  permalink: /archives/category/hardware/
  description: ""
  REMOVE body: "Posts about hardware development, electronics, and open source hardware projects."

category/highlights.md
  permalink: /archives/category/highlights/
  description: ""
  [no body to remove]

category/ideas.md
  permalink: /archives/category/ideas/
  description: "Proposals which I'll probably never get around to implementing."
  [no body to remove]

category/pcb.md
  permalink: /archives/category/pcb/
  description: ""
  [no body to remove]

category/python.md
  permalink: /archives/category/python/
  description: ""
  [no body to remove]

category/summer-of-code.md
  permalink: /archives/category/summer-of-code/
  description: ""
  REMOVE body: "Posts about Google Summer of Code projects and experiences."

category/timvideos-us.md
  permalink: /archives/category/timvideos-us/
  description: 'TimVideos.us is a group of exciting projects which together create a system for doing both recording and live event streaming for conferences, meetings, user groups and other presentations.'
  REMOVE body: "Posts about TimVideos.us project - open source video capture and streaming hardware."

category/ubuntu.md
  permalink: /archives/category/ubuntu/
  description: ""
  REMOVE body: "Posts about Ubuntu Linux distribution and related technologies."

category/uncategorized.md
  permalink: /archives/category/uncategorized/
  description: ""
  [no body to remove]

category/uni.md
  permalink: /archives/category/uni/
  description: ""
  [no body to remove]

category/useful-bits.md
  permalink: /archives/category/useful-bits/
  description: ""
  REMOVE body: "Useful technical tips, tricks, and helpful information for developers and engineers."
```

**Files requiring title change (4 slugs):**

```
category/lca.md
  title: linux.conf.au           # WAS: "LCA"
  permalink: /archives/category/lca/
  description: 'Linux.conf.au is the best Linux conference I have been too.'
  REMOVE body: "Posts related to Linux.conf.au (LCA) conferences and events."

category/sci-fi.md
  title: "Sci Fi"                # WAS: Sci-Fi  (remove hyphen)
  permalink: /archives/category/sci-fi/
  description: 'All things Science Fiction (TV, books and even games).'
  [no body to remove]

category/tp.md
  title: Thousand Parsec         # WAS: TP
  permalink: /archives/category/tp/
  description: 'Thousand Parsec is a space empire building framework which I lead.'
  [no body to remove]

category/rcs-darcs.md
  title: darcs                   # WAS: "RCS / Darcs" — P4 FLAG for hierarchy
  permalink: /archives/category/rcs-darcs/  # P4 must add redirect /archives/rcs/darcs → here
  description: 'Darcs is revision control system I use to use before converting to git.'
  [no body to remove]
```

### 4B. `category/*/feed.xml` changes — all 19 feed files

Each `category/<slug>/feed.xml` has `permalink: /category/<slug>/feed/`.
Change ALL to `permalink: /archives/category/<slug>/feed/`.

Example for lca: `permalink: /archives/category/lca/feed/`

(19 feed files: diary, games, gaming-miniconf, google, hardware, highlights, ideas, lca, pcb, python, rcs-darcs, sci-fi, summer-of-code, timvideos-us, tp, ubuntu, uncategorized, uni, useful-bits)

### 4C. `_layouts/home.html` — line 34

**Current (line 34):**
```liquid
<a href="{{ '/archives/category/' | append: category | slugify | relative_url }}" rel="category tag">{{ category | replace: '-', ' ' | title }}</a>
```

**Problems:**
1. Display: `category | replace: '-', ' ' | title` is a lossy slug-transform (gives "Lca" not "linux.conf.au", "Tp" not "Thousand Parsec").
2. Href: uses `category | slugify` — since category values in post front matter are already slugs (e.g. `lca`, `timvideos-us`), `slugify` is idempotent — href is correct.

**Fix (replace display with faithful page title lookup):**
```liquid
{% assign _cat_page = site.pages | where: "category", category | first %}
<a href="{{ '/archives/category/' | append: category | relative_url }}" rel="category tag">{{ _cat_page.title | default: category }}</a>
```

Note: `| slugify` is NOT needed since post `categories:` values are already lowercase slugs. Removing it avoids any edge-case mangling.

### 4D. `_layouts/post.html` — line 48

**Current (line 48):**
```liquid
<a href="{{ '/category/' | append: category | relative_url }}">{{ category }}</a>
```

**Problems:**
1. Href: `/category/<raw>` — wrong URL space (should be `/archives/category/<slug>`).
2. Display: raw `{{ category }}` — outputs the slug (`lca`, `tp`, `sci-fi`) not the faithful display name.

**Fix:**
```liquid
{% assign _cat_page = site.pages | where: "category", category | first %}
<a href="{{ '/archives/category/' | append: category | relative_url }}" rel="category tag">{{ _cat_page.title | default: category }}</a>
```

### 4E. `_layouts/category.html` — line 35

**Current (line 35):**
```liquid
<span class="entry-category">{% for cat in post.categories %}{% unless cat == category_key %}<a href="{{ '/category/' | append: cat | relative_url }}" rel="category tag">{{ cat | replace: '-', ' ' | capitalize }}</a>{% endunless %}{% endfor %}</span>
```

**Problems:**
1. Href: `/category/<cat>` — wrong URL space.
2. Display: `| replace: '-', ' ' | capitalize` — lossy (gives "Linux.conf.au" → "Linux conf au", "Thousand parsec").

**Fix:**
```liquid
<span class="entry-category">{% for cat in post.categories %}{% unless cat == category_key %}{% assign _cat_page = site.pages | where: "category", cat | first %}<a href="{{ '/archives/category/' | append: cat | relative_url }}" rel="category tag">{{ _cat_page.title | default: cat }}</a>{% endunless %}{% endfor %}</span>
```

### 4F. `_includes/sidebar.html` — lines 34–51

All 19 `<option value="{{ '/category/<slug>/' | relative_url }}">` must change to `<option value="{{ '/archives/category/<slug>/' | relative_url }}">`

The display text (option label) for `lca` currently reads "linux.conf.au" (already correct), `sci-fi` reads "Sci Fi" (already correct), `tp` reads "Thousand Parsec" (check — currently shows "TP" based on sidebar line 48 grep). Sidebar line 44 shows `">RCS (3)</option>` — should be changed to match sidebar faithful label; since this is a flat dropdown and `rcs-darcs` maps to the `darcs` sub-category, decide at P4 what label to use.

**Specific sidebar changes needed:**
- Line 34: `'/category/diary/'` → `'/archives/category/diary/'`
- Line 35: `'/category/games/'` → `'/archives/category/games/'`
- Line 36: `'/category/gaming-miniconf/'` → `'/archives/category/gaming-miniconf/'`
- Line 37: `'/category/google/'` → `'/archives/category/google/'`
- Line 38: `'/category/hardware/'` → `'/archives/category/hardware/'`
- Line 39: `'/category/highlights/'` → `'/archives/category/highlights/'`
- Line 40: `'/category/ideas/'` → `'/archives/category/ideas/'`
- Line 41: `'/category/lca/'` → `'/archives/category/lca/'` (display label already correct: "linux.conf.au")
- Line 42: `'/category/pcb/'` → `'/archives/category/pcb/'`
- Line 43: `'/category/python/'` → `'/archives/category/python/'`
- Line 44: `'/category/rcs-darcs/'` → `'/archives/category/rcs-darcs/'` (P4: redirect from /archives/rcs/darcs needed)
- Line 45: `'/category/sci-fi/'` → `'/archives/category/sci-fi/'` (display label already "Sci Fi" — correct)
- Line 46: `'/category/summer-of-code/'` → `'/archives/category/summer-of-code/'`
- Line 47: `'/category/timvideos-us/'` → `'/archives/category/timvideos-us/'`
- Line 48: `'/category/ubuntu/'` → `'/archives/category/ubuntu/'`
- Line 49: `'/category/uncategorized/'` → `'/archives/category/uncategorized/'`
- Line 50: `'/category/uni/'` → `'/archives/category/uni/'`
- Line 51: `'/category/useful-bits/'` → `'/archives/category/useful-bits/'`

Also update display labels in sidebar where they differ from oracle:
- `tp` currently shows "Thousand Parsec" in sidebar (confirmed from live site). Verify sidebar line 47 — currently says `">Thousand Parsec (16)</option>` — **ALREADY CORRECT** in sidebar, just URL needs fixing.
- `rcs-darcs` sidebar shows "RCS (3)" — this is the WP parent category label. **Leave as "RCS (3)"** for P2; P4 handles hierarchy.

---

## 5. Implementation Gates

The implementer must verify all of the following after applying remediation:

1. **`bundle3.3 exec jekyll build` exits clean** — zero errors, zero warnings.
2. **`structure_check` passes 6/6** — all 6 structural tests green.
3. **Content-linter corpus stays exactly 22** — no post files modified (only category/*.md and layout/_include files changed).
4. **Every category archive page builds at `/archives/category/<slug>/`** — confirm `_site/archives/category/*/index.html` exists for all 18 non-404 slugs; plus `_site/archives/category/rcs-darcs/index.html` exists.
5. **Page-title faithful:** every `_site/archives/category/<slug>/index.html` contains `{ Category Archives } <oracle-display-name>` — spot-check lca ("linux.conf.au"), tp ("Thousand Parsec"), sci-fi ("Sci Fi").
6. **Archive-meta faithful:** every category page with a non-empty oracle description has the exact verbatim text in `<div class="archive-meta">`. Spot-check: ideas, lca, timvideos-us, tp, sci-fi.
7. **Category links in home/post/category layouts resolve (no 404)** — all `href="/archives/category/<slug>/"` must match a built page.
8. **Category links display faithful names** — no slug-filter output like "Lca" or "Tp"; must see "linux.conf.au" and "Thousand Parsec".
9. **Feed permalinks correct:** `_site/archives/category/lca/feed/index.html` (and all 19 slug feeds) exist at new paths.
10. **Sidebar dropdown URLs updated:** confirm `_site` HTML contains `/archives/category/lca/` not `/category/lca/` in sidebar option values.

---

## 6. Deferred to P4 (URL-Structure Phase)

1. **`rcs-darcs` hierarchical URL:** WP stored as `RCS > darcs` at `/archives/rcs/darcs`. P4 must create a redirect from `/archives/rcs/darcs` → `/archives/category/rcs-darcs/` (or change the permalink to the canonical WP path `/archives/rcs/darcs/` and remove the `/category/` prefix). Also `rcs/darcs` sub-category `Tailor` exists (`/archives/rcs/tailor`) — not represented in Jekyll at all; P4 defers decision on whether to create it.

2. **`timvideos-us/hdmi2usb` sub-category:** Live posts reference `href="/archives/category/timvideos-us/hdmi2usb"` with display "HDMI2USB". No `category/hdmi2usb.md` exists in Jekyll. P4 must: (a) create `category/timvideos-us/hdmi2usb.md` (or equivalent), (b) restore the `hdmi2usb` category entry in the affected posts' `categories:` arrays, (c) set up URL at `/archives/category/timvideos-us/hdmi2usb/`.

3. **Additional WP categories not migrated to Jekyll:** The live WP sidebar shows `Scheme` (1 post), `Sydney` (1 post), `Tailor` (1 post, sub-category of RCS) — these have posts in `_posts/` but their category slugs (`tp` for scheme, `google` for sydney) were collapsed during migration. P4 to decide whether to restore.

---

## 7. Baseurl Confirmation

The `_config.yml` sets `baseurl: "/blog.mithis.net"`. The permalink values in `category/<slug>.md` are **site-root-relative** (e.g. `/archives/category/lca/`) — Jekyll applies baseurl automatically at build time via `relative_url`. Category link hrefs in layouts use `| relative_url` filter, which prepends baseurl. This is correct and NOT P4-coupled — the baseurl-independent permalink values `/archives/category/<slug>/` are correct as written.

---

## Appendix: Raw Oracle Data Summary

| slug | HTTP | oracle display name | oracle description (first 60 chars) |
|---|---|---|---|
| diary | 200 | Diary | _(empty)_ |
| games | 200 | Games | _(empty)_ |
| gaming-miniconf | 200 | Gaming Miniconf | _(empty)_ |
| google | 200 | Google | _(empty)_ |
| hardware | 200 | Hardware | _(empty)_ |
| highlights | 200 | Highlights | _(empty)_ |
| ideas | 200 | Ideas | Proposals which I'll probably never get around to... |
| lca | 200 | linux.conf.au | Linux.conf.au is the best Linux conference I have... |
| pcb | 200 | PCB | _(empty)_ |
| python | 200 | Python | _(empty)_ |
| rcs-darcs | **404** | HTTP-404 | (fetched from /archives/rcs/darcs: "Darcs is revi...") |
| sci-fi | 200 | Sci Fi | All things Science Fiction (TV, books and even gam... |
| summer-of-code | 200 | Summer of Code | _(empty)_ |
| timvideos-us | 200 | TimVideos.us | TimVideos.us is a group of exciting projects which... |
| tp | 200 | Thousand Parsec | Thousand Parsec is a space empire building framewor... |
| ubuntu | 200 | Ubuntu | _(empty)_ |
| uncategorized | 200 | Uncategorized | _(empty)_ |
| uni | 200 | Uni | _(empty)_ |
| useful-bits | 200 | Useful Bits | _(empty)_ |

Scraped HTML files retained in `tmp/p2-oracle/` for implementer verification.
