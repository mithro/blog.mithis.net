# Google Search Console Indexing Fixes — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate the self-inflicted causes of Google Search Console's "pages not indexed" report (sitemap pollution, ~175 distinct site-emitted broken internal links, dead legacy WordPress URLs) and kick off GSC re-validation.

**Architecture:** Three layers of fixes: (1) replace the polluted hand-written `sitemap.xml` with the already-installed `jekyll-sitemap` plugin's clean output; (2) fix link *generation* in layouts/includes so the site stops emitting 404s (template bugs, dead feed links, missing category page); (3) manual GSC console actions (remove stale sitemap submissions, validate fixes). A new internal-link checker script becomes a CI gate so broken internal links can't regress.

**Tech Stack:** Jekyll 4 + GitHub Actions builder (custom plugins DO run), jekyll-sitemap 1.4.0 (vendored, template verified), jekyll-redirect-from, Python via `uv` for the checker script. Local builds use `bundle3.3 exec`, NOT bare `bundle`.

---

## Execution status (2026-07-05)

Tracking issue: **#26**. Executed (with user-directed scope change — feeds are now *generated*, not just cleaned):

- ✅ Task 0 (issue #26 created; baseline scan ran: 175 distinct / 1202 refs)
- ✅ Task 1 — plus the larger change the user requested: `_plugins/feed_pages.rb` now generates ALL RSS feeds (per-category + main `/feed/` RSS2 + `/feed.xml` alias) from `_includes/feed-{category,main}.xml`; 25 hand-written XML files deleted (23 category feeds, root `feed.xml`, `comments/feed.xml`); `jekyll-feed` retired (it served Atom where WP subscribers expect RSS2). Verified byte-identical output (modulo one line of trailing whitespace in 4 files + intentional `/feed/` Atom→RSS2). Closes #6.
- ✅ Task 2 (robots.txt cleaned)
- ✅ Task 4 — **premise correction:** `category/timvideos-us/hdmi2usb.md` already existed at the nested permalink (the earlier audit only globbed top-level `category/*.md`). What was actually missing: `redirect_from` for the flat `/archives/category/hdmi2usb/` URL (added), `/category/timvideos-us/hdmi2usb/` (added), `parent_cat: timvideos-us` marker (added). rcs-darcs + rcs-tailor redirect normalization from Task 8 Step 8.2 landed in the same commit.
- ✅ Task 6 Step 6.4 only (`comments/feed.xml` deleted with the feed work). Steps 6.1–6.3 (footer/sidebar/post-layout link removal) still TODO.
- ✅ CLAUDE.md updated (plugin docs + commit-trailer line, D5).

**Remaining:** Tasks 3, 5, 6 (link removal steps), 7, 8 Step 8.1 (nav), 9, 10, 11 (deploy verify), 12 (GSC console), 13 (conditional).

---

## Background: what Search Console reported (2026-07-05, msg WNC-20237597)

| Reason | Pages | Diagnosis (verified) |
|---|---|---|
| Not found (404) | 82 | ~35 dead WP sitemap XMLs (`sitemap_index.xml` + 34 children incl. `sitemap-archives.xml`, `sitemap-pt-post-*.xml` — all verified 404 live); plus site-emitted broken links (below); plus legacy WP URLs (`/comments/feed/`, date archives, trailing-slash post variants) |
| Page with redirect | 7 | No-trailing-slash internal links (`/feed`, `/archives/tag/x`, `/archives/category/tailor` → stub chain) that 301 on GitHub Pages |
| Server error (5xx) | 4 | Pre-cutover artifacts from the dying WordPress server (April–May 2026). GitHub Pages doesn't 5xx; just needs validation |
| Excluded by 'noindex' | 4 | jekyll-redirect-from stubs (intentionally noindexed) that the polluted sitemap *submits for indexing* |
| Alternative page with proper canonical tag | 2 | Same stubs (they carry `canonical` → target). Benign once no longer in the sitemap |
| Crawled – currently not indexed | 178 | Dead per-post "comments RSS" links (76 — one per post, `post.html:55`) + mangled `/archives-tag-*` URLs (85) + legacy feed/archive cruft |
| Discovered – currently not indexed | 148 | Legacy cruft + Google quality threshold; trend already recovering (indexed 5 → 64 since the 2026-05-30 cutover) |

The coverage zip (`Chart.csv` etc.) contains only summary counts — per-URL lists require drill-down export in the GSC UI (Task 12 Step 12.2).

**Verified root causes in this repo:**

1. **Polluted sitemap** — the hand-written `sitemap.xml` emits 245 URLs including all 26 noindexed `/category/*/` redirect stubs, `/404.html`, `/assets/css/main.css`, `/robots.txt`, `/search.json`, `/redirects.json`, and a duplicate homepage entry. Submitting noindexed/redirecting URLs in a sitemap is precisely what generates the "Excluded by noindex" / "Alternative page with canonical" / "Page with redirect" complaints.
2. **Site-emitted broken links** (from a full `_site` scan: 175 distinct broken internal URLs, 1202 references):
   - `/cgi-bin/gitweb.cgi` — `_includes/sidebar.html:46`, on every page (199 refs). Already tracked as issue #13.
   - `/archives/category/rcs-darcs/` — `_includes/navigation.html:21` ("RCS" nav item), on every page (197 refs). Real page is `/archives/rcs/darcs/`; the fidelity-era decision to leave this 404 is now obsolete.
   - `/comments/feed/` + `/comments/feed` — `_includes/sidebar.html:84` and `_includes/footer.html:10`, on every page (394 refs). No comments feed exists (comments are frozen).
   - `/archives/category/hdmi2usb` — `_includes/sorted-categories.html` link construction + **no hdmi2usb category page exists at all** (43 refs). On live WP, hdmi2usb was a *child* of timvideos-us: a nested feed source exists at `category/timvideos-us/hdmi2usb/feed.xml`, and the polluted sitemap already submits the nested page URL `/archives/category/timvideos-us/hdmi2usb/` — currently a 404 Google was explicitly told to index.
   - `/archives-tag-<slug>` (85 distinct URLs) — `_layouts/category.html:39`, `_layouts/home.html:22`, and `_layouts/author.html:23` apply `slugify` to the whole path (`'/archives/tag/' | append: tag | slugify`), turning slashes into hyphens.
   - `/archives/<cat>/<id>-<slug>/feed` — `_layouts/post.html:55` emits a dead per-post "comments RSS" link on every one of the 76 posts (the singleton broken URLs in the scan). Sum check: 85 tag + 76 per-post feed + 6 dead files + 8 site-wide = 175 distinct double-quoted, plus 2 single-quoted `two-col.html` image URLs only the fixed (dual-quote) checker sees = ~177.
   - Dead in-post file links: 6 posts reference `wp-content/uploads/2007/02–03` files and `/~tim/crosstool-cygwin-gcc336.tar.bz2` that were already 404 in 2007 and are NOT in the Wayback Machine (verified via CDX API — only 404 captures exist).

**Decision points resolved in this plan** (change if you disagree):
- **D1 — Comments-feed links:** *remove* them (footer "& Comments", sidebar "All comments", per-post "comments RSS" span) rather than serve stub feeds, and delete the orphaned `comments/feed.xml` placeholder (it serves at `/comments/feed.xml` — a URL nothing links to; the linked URLs `/comments/feed{,/}` were always 404). Comments are closed site-wide; dead functionality gets removed per the evolved core directive. Visual diff is a few words of footer/sidebar text.
- **D2 — gitweb link:** repoint "My Useful Bits" to `https://github.com/mithro` (the successor home of that content) rather than delete the sidebar item.
- **D3 — Old WP sitemap XML 404s:** leave them 404 (correct signal; Google drops them) and remove any stale submissions in GSC. No stub XML files.
- **D4 — Unrecoverable 2007 file links:** de-link, keep the text, append an em-dash note "*(file lost in a pre-2026 server move)*". No Wayback copies exist to point at.
- **D5 — Commit trailer:** project CLAUDE.md still says `Co-Authored-By: Claude Opus 4.7 (1M context)` — that's stale (migration-era). Use the current model's trailer and update CLAUDE.md in Task 11 Step 11.3.

---

**Note for agentic executors:** several verify gates below use `grep -c … # expect 0`. `grep` exits 1 when it finds nothing — for those gates, printed `0` + exit code 1 IS the pass condition; do not treat the non-zero exit as a failure.

### Task 0: Tracking issue + baseline

**Files:** none (repo state capture)

- [ ] **Step 0.1: Create the tracking issue**

```bash
gh issue create \
  --title "Google Search Console: pages not being indexed (sitemap pollution + site-emitted 404s)" \
  --body "GSC msg WNC-20237597 (2026-07-05): 82x 404, 7x redirect, 4x 5xx, 4x noindex, 2x canonical-alternative, 178x crawled-not-indexed, 148x discovered-not-indexed.

Root causes found: hand-written sitemap.xml submits noindexed redirect stubs + junk; templates emit ~175 distinct broken internal URLs (dead comments feeds, gitweb link, malformed /archives-tag-* links, missing hdmi2usb category page, nav RCS link to intentionally-404 URL); ~35 dead legacy WP sitemap XMLs.

Plan: docs/superpowers/plans/2026-07-05-gsc-indexing-fixes.md"
```

Expected: issue URL printed. Note the number — commits below use `#N` (replace `#GSC` placeholder throughout this plan).

- [ ] **Step 0.2: Baseline build + broken-link scan (the "failing test")**

The checker script is the test harness for every task below — create it FIRST (Task 10 Step 10.1, `scripts/check_internal_links.py`), then:

```bash
cd /home/tim/github/mithro/blog.mithis.net
JEKYLL_ENV=production bundle3.3 exec jekyll build
uv run python scripts/check_internal_links.py > tmp/linkcheck-before.txt ; head -20 tmp/linkcheck-before.txt
```

It exits non-zero while broken links exist; that's the failing-test baseline. (Do NOT wire it into CI yet — that's Task 10 Step 10.3, after the fixes land.)

Expected: ~177 distinct broken internal URLs, ~1210 total references (the checker's dual-quote regex also catches the two single-quoted `two-col.html` image URLs — `board.png`, `eagle2geda.png` — on top of the 175 double-quoted ones; ±small drift).

---

### Task 1: Replace the polluted sitemap with jekyll-sitemap output

The vendored plugin template (`vendor/bundle/ruby/3.3.0/gems/jekyll-sitemap-1.4.0/lib/sitemap.xml`) was verified to: include all posts with `<lastmod>` from post date; include only `site.html_pages` with `sitemap != false`; exclude `/404.html` by URL; and exclude jekyll-redirect-from stubs (the plugin marks them `sitemap: false` automatically). Non-HTML pages (`robots.txt`, `search.json`, `main.css`, `redirects.json`) are excluded because they're not `html_pages`. jekyll-sitemap only generates when no source `sitemap.xml` exists — so deleting ours activates it.

**Files:**
- Delete: `sitemap.xml`
- Modify: `search.html:1-5` (frontmatter)

- [ ] **Step 1.1: Delete the hand-written sitemap**

```bash
git rm sitemap.xml
```

- [ ] **Step 1.2: Exclude the search page from the sitemap**

In `search.html`, add `sitemap: false` to the frontmatter:

```yaml
---
layout: default
title: "Search"
permalink: /search.html
sitemap: false
---
```

(Rationale: it's a client-side search shell with no indexable content; WP equivalents are conventionally noindexed.)

- [ ] **Step 1.3: Build and verify the generated sitemap**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -c "<loc>" _site/sitemap.xml
grep -c "<lastmod>" _site/sitemap.xml
grep "<loc>" _site/sitemap.xml | grep -E "net/category/|net/tag/|404\.html|\.css|\.json|search\.html" ; echo "exit=$?"
```

Expected: ~200 `<loc>` entries (76 posts + ~86 tag pages + ~23 category pages + author + home + contact + paginated listing pages + a handful of static PDFs); `<lastmod>` on every post entry; the final grep finds NOTHING (`exit=1`). The pattern `net/category/` is anchored so it matches only root-level redirect stubs — the real category pages at `/archives/category/*` and `/archives/rcs/*` SHOULD be present.

- [ ] **Step 1.4: Commit**

```bash
git add -A && git commit -m "Replace hand-written sitemap.xml with jekyll-sitemap output

The hand-written sitemap submitted 245 URLs to Google including all 26
noindexed jekyll-redirect-from stubs (/category/*/), /404.html, CSS and
JSON files, and a duplicate homepage entry. Submitting noindexed and
redirecting URLs is what triggered GSC's 'Excluded by noindex',
'Alternative page with proper canonical tag' and 'Page with redirect'
complaints (msg WNC-20237597). jekyll-sitemap 1.4.0 (already in the
Gemfile and plugin list) generates a clean sitemap: posts with lastmod,
html pages only, redirect stubs and 404.html excluded automatically.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Clean up robots.txt

**Files:**
- Modify: `robots.txt`

- [ ] **Step 2.1: Rewrite robots.txt**

Replace the body (keep the frontmatter) with:

```
---
layout: none
---
User-agent: *
Allow: /

Sitemap: {{ '/sitemap.xml' | absolute_url }}

# Legacy WordPress paths — nothing is served here anymore; keep crawlers out
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/
Disallow: /admin/
```

Changes: drop `Sitemap: /feed.xml` (a 10-item RSS adds nothing next to a complete sitemap and muddies GSC's sitemap report); drop the `Allow: /category/ /tag/ /about/ /search/` lines (`Allow` is only meaningful to carve exceptions out of a `Disallow`; `/category/` and `/tag/` are now redirect stubs / 404s anyway).

- [ ] **Step 2.2: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build && cat _site/robots.txt
git add robots.txt && git commit -m "robots.txt: drop no-op Allow lines and feed-as-sitemap

Allow: lines without a broader Disallow are no-ops, and the ones listed
(/category/, /tag/) now point at redirect stubs or 404s. The RSS feed
adds nothing as a sitemap next to the complete sitemap.xml and shows up
as a confusing second entry in GSC's sitemap report.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: rendered robots.txt shows `Sitemap: https://blog.mithis.net/sitemap.xml` only.

---

### Task 3: Fix category-link construction in `sorted-categories.html`

Every post's "Filed under" links are built as `'/archives/category/' | append: slug` — no trailing slash (301s), and wrong for nested categories (`rcs-darcs` lives at `/archives/rcs/darcs/`, `tailor` at `/archives/rcs/tailor/`) and for `hdmi2usb` (no page — Task 4). The include already looks up the category page for the title; use its URL too.

**Files:**
- Modify: `_includes/sorted-categories.html` (final `for` loop)

- [ ] **Step 3.1: Use the category page's real URL**

Replace the last loop's anchor line:

```liquid
{%- for _sc_pair in _sc_pairs -%}
  {%- assign _sc_parts = _sc_pair | split: "|" -%}
  {%- assign _sc_slug2 = _sc_parts | last -%}
  {%- assign _sc_page2 = site.pages | where: "cat_slug", _sc_slug2 | first -%}
  {%- assign _sc_title2 = _sc_page2.title | default: _sc_slug2 -%}
  {%- if _sc_page2 -%}
    {%- assign _sc_href = _sc_page2.url -%}
  {%- else -%}
    {%- assign _sc_href = '/archives/category/' | append: _sc_slug2 | append: '/' -%}
  {%- endif -%}
  <a href="{{ _sc_href | relative_url }}" rel="category tag">{{ _sc_title2 }}</a>{%- unless forloop.last %}{{ include.separator }}{% endunless -%}
{%- endfor -%}
```

- [ ] **Step 3.2: Build and spot-check**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -o 'rel="category tag"' _site/archives/tp/16-tailor-darcs2svn-tp.html | wc -l
grep -o 'href="[^"]*" rel="category tag"' _site/archives/tp/16-tailor-darcs2svn-tp.html
```

Expected: category links now read `/archives/rcs/darcs/`, `/archives/rcs/tailor/`, `/archives/tp/` etc. — trailing slashes, real permalinks, no `/archives/category/rcs-darcs`.

- [ ] **Step 3.3: Commit**

```bash
git add _includes/sorted-categories.html && git commit -m "Post category links: use the category page's real permalink

sorted-categories.html hardcoded /archives/category/<slug> (no trailing
slash), which 301s for normal categories, 404s for the nested rcs-darcs
(/archives/rcs/darcs/) and tailor (/archives/rcs/tailor/) categories,
and 404s for hdmi2usb (page missing entirely). The include already
looks up the category page for its title — use its url too.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Create the missing HDMI2USB category page

Posts filed under `hdmi2usb` link to a category page that never existed (43 refs). On live WP, hdmi2usb was a *child* of timvideos-us: its real URL was `/archives/category/timvideos-us/hdmi2usb/` (the nested feed source already exists at `category/timvideos-us/hdmi2usb/feed.xml`), and the old hand-written sitemap even submitted that nested URL to Google as a 404. Create the page at the live-WP nested permalink; NO new feed is needed.

**Files:**
- Create: `category/timvideos-us/hdmi2usb.md`
- Check-only: `category/timvideos-us.md` (model), `category/timvideos-us/hdmi2usb/feed.xml` (existing nested feed)

- [ ] **Step 4.1: Check the model page and how many posts qualify**

```bash
cat category/timvideos-us.md; head -8 category/timvideos-us/hdmi2usb/feed.xml
grep -l "hdmi2usb" _posts/*.md | wc -l
```

- [ ] **Step 4.2: Create `category/timvideos-us/hdmi2usb.md`**

```yaml
---
layout: category
title: HDMI2USB
cat_slug: hdmi2usb
permalink: /archives/category/timvideos-us/hdmi2usb/
description: ""
redirect_from:
  - /category/timvideos-us/hdmi2usb/
  - /archives/category/hdmi2usb/
---
```

(The `/archives/category/hdmi2usb/` redirect_from covers the flat URL the old `sorted-categories.html` emitted for years; after Task 3, generated links go straight to the nested page via `cat_slug` lookup.)

- [ ] **Step 4.3: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
ls _site/archives/category/timvideos-us/hdmi2usb/
grep -o 'noindex' _site/archives/category/hdmi2usb/index.html
git add category/timvideos-us/hdmi2usb.md
git commit -m "Add missing HDMI2USB category page at its live-WP nested URL

Posts filed under hdmi2usb emitted 43 'Filed under HDMI2USB' links,
but no category page was ever created during the migration — every
click and crawl was a 404, and the old hand-written sitemap even
submitted the nested /archives/category/timvideos-us/hdmi2usb/ URL to
Google. The nested feed already existed; only the page was missing.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: `index.html` exists under `_site/archives/category/timvideos-us/hdmi2usb/`; the flat `/archives/category/hdmi2usb/` path now holds a noindex redirect stub. The sidebar categories dropdown and tags cloud pick the page up automatically (they iterate `site.pages`).

---

### Task 5: Fix tag-link generation (slugify-order bug + trailing slashes)

**Files:**
- Modify: `_layouts/category.html:39`, `_layouts/home.html:22`, `_layouts/author.html:23` (slugify-order bug)
- Modify: `_layouts/post.html:50`, `_layouts/tag.html:66` (trailing slash), `_layouts/post.html:38` (author link)

- [ ] **Step 5.1: Fix `_layouts/category.html:39`, `_layouts/home.html:22`, and `_layouts/author.html:23`** — all three apply `slugify` to the whole path, mangling it into `/archives-tag-<slug>`. Replace each tag loop with:

```liquid
{%- for tag in post.tags %} <a href="{{ tag | remove: '.' | slugify | prepend: '/archives/tag/' | append: '/' | relative_url }}" rel="tag">{{ tag }}</a>{% unless forloop.last %},{% endunless %}{% endfor -%}
```

(Also adds the `remove: '.'` normalisation that `post.html` already applies, so both layouts produce identical URLs.)

- [ ] **Step 5.2: Fix `_layouts/post.html:50` and `_layouts/tag.html:66`** — these two have the correct order already, just append the trailing slash to avoid a 301 per tag click (post.html variant shown; tag.html uses `other_tags`):

```liquid
{%- for tag in page.tags %} <a href="{{ tag | remove: '.' | slugify | prepend: '/archives/tag/' | append: '/' | relative_url }}" rel="tag">{{ tag }}</a>{% unless forloop.last %},{% endunless %}{% endfor -%}
```

- [ ] **Step 5.3: Fix `_layouts/post.html:38`** — author link `'/archives/author/mithro'` → `'/archives/author/mithro/'` (real page is at the slashed URL; unslashed 301s).

- [ ] **Step 5.4: Sweep other layouts for the same two patterns**

```bash
grep -n "archives/tag\|archives/author" _layouts/*.html _includes/*.html
```

Fix any remaining no-slash or mis-slugified instances the same way.

- [ ] **Step 5.5: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -ro 'href="/archives-tag-[^"]*"' _site/ | wc -l   # expect 0
git add _layouts/ _includes/ && git commit -m "Fix tag/author link generation (slugify order + trailing slashes)

category.html, home.html and author.html applied slugify to the whole
'/archives/tag/<tag>' path, so every slash became a hyphen: 85 distinct
/archives-tag-<slug> 404 URLs emitted from listing pages. post.html and
tag.html had the right order but no trailing slash, costing a 301 per
tag/author click and 'Page with redirect' noise in Search Console.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Remove dead comments-feed links (decision D1)

Comments are frozen site-wide ("Comments are closed for this post."). Three templates still link to feeds that don't exist: `/comments/feed{,/}` on every page (394 refs) and `<post-url>/feed` on all 76 posts. Also delete the orphaned `comments/feed.xml` placeholder — it serves at `/comments/feed.xml`, a URL nothing links to (the links point at `/comments/feed{,/}`, which 404).

**Files:**
- Modify: `_includes/footer.html:10`
- Modify: `_includes/sidebar.html:84` (the "All comments" `<li>`)
- Modify: `_layouts/post.html:55` (the `entry-rsslink` span)
- Delete: `comments/feed.xml`

- [ ] **Step 6.1: `_includes/footer.html:10`** — drop the Comments half:

```html
<span id="footer-rss"> RSS <a href="{{ '/feed/' | relative_url }}" title="{{ site.title | escape }} RSS 2.0 Feed" rel="alternate" type="application/rss+xml">Posts</a></span>
```

(Note `/feed` → `/feed/` while here — kills a site-wide 301.)

- [ ] **Step 6.2: `_includes/sidebar.html:84`** — delete the `<li>…All comments…</li>` line. Check the surrounding widget: if "All posts" remains, keep the widget; fix its href to `/feed/` if it lacks the slash.

- [ ] **Step 6.3: `_layouts/post.html:55`** — delete the whole `entry-rsslink` span (the "Follow any responses to this post with its comments RSS feed." sentence). The adjacent "Comments are closed for this post." span stays.

- [ ] **Step 6.4: Delete the orphaned placeholder feed**

```bash
git rm comments/feed.xml
```

- [ ] **Step 6.5: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -rlo 'comments/feed' --include='*.html' _site/ | wc -l    # expect 0
grep -rlo 'entry-rsslink' --include='*.html' _site/ | wc -l    # expect 0
git add -A
git commit -m "Remove dead comments-RSS links (site-wide + per-post)

Comments are frozen; no working comments feed exists. The footer and
sidebar linked /comments/feed{,/} from every page (394 refs — both 404;
only the never-linked /comments/feed.xml placeholder was served, now
deleted) and post.html emitted a per-post '<url>/feed' comments-RSS
link on all 76 posts — every one a 404. These dead per-post feed URLs
feed GSC's 'Crawled - currently not indexed' bucket (178 pages).

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Fix the gitweb sidebar link (decision D2, Closes #13)

**Files:**
- Modify: `_includes/sidebar.html:46`

- [ ] **Step 7.1: Repoint "My Useful Bits"**

```html
<li><a href="https://github.com/mithro" rel="me" title="Useful code snippets and other juicy tidbits.">My Useful Bits</a></li>
```

- [ ] **Step 7.2: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build && grep -rc "cgi-bin/gitweb" _site/search.html
git add _includes/sidebar.html && git commit -m "Sidebar: repoint 'My Useful Bits' from dead gitweb to GitHub

blog.mithis.net/cgi-bin/gitweb.cgi died with the old server; the link
404'd on every page (199 refs). GitHub is where that code lives now.

Closes #13. Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: grep count 0.

---

### Task 8: Fix nav "RCS" link + add legacy redirect for `/archives/category/rcs-darcs/`

**Files:**
- Modify: `_includes/navigation.html:21`
- Modify: `category/rcs-darcs.md` (frontmatter)

- [ ] **Step 8.1: `_includes/navigation.html:21`** — point at the real page:

```html
<li class="page_item"><a href="{{ '/archives/rcs/darcs/' | relative_url }}">RCS</a></li>
```

- [ ] **Step 8.2: `category/rcs-darcs.md`** — supersede the fidelity-era "intentionally NOT redirected" decision; old post bodies still link the URL (8 in-content refs):

```yaml
redirect_from:
  - /category/rcs-darcs/
  - /archives/category/rcs-darcs/
```

Also replace the stale frontmatter comment with: `# /archives/category/rcs-darcs/ 404'd on live WP; post-cutover we redirect it (GSC cleanup, #GSC).`

- [ ] **Step 8.3: Build, verify, commit**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -o 'href="/archives/rcs/darcs/"' _site/search.html | head -1
ls _site/archives/category/rcs-darcs/
git add _includes/navigation.html category/rcs-darcs.md
git commit -m "Nav: point RCS at /archives/rcs/darcs/; redirect legacy category URL

The nav linked /archives/category/rcs-darcs/ on every page (197 refs)
— a URL that 404'd even on live WordPress (nested category). The
fidelity-era decision to preserve that 404 is obsolete; old post bodies
still link it, so give it a redirect stub too.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Expected: nav href updated; `_site/archives/category/rcs-darcs/index.html` redirect stub exists.

---

### Task 9: De-link unrecoverable 2007 file references (decision D4)

Seven posts link files dead since ~2007; Wayback has only 404 captures (verified via CDX API). De-link, keep text, add the note "*(file lost in a pre-2026 server move)*" — inline `<em>`/plain text only, no block HTML (content lint).

**Scope guard:** only *internal* references (site-relative `/wp-content/...`, `/~tim/...`, or absolute `blog.mithis.net/...`) are in scope. External URLs that happen to contain `wp-content` (e.g. `lunapark6.com/wp-content/...` in `2007-03-11-i-want-a-cool-desktop.md`) and the external `thousandparsec.net/~tim/crosstool...` link inside migrated comment HTML must NOT be touched.

**Files (each: find the URL, replace the markdown/HTML link with plain text + note):**
- Modify: `_posts/2007-03-07-eagle-for-pcb.md` + `_posts/2007-03-07-eagle2geda-symbol-converter.md` — `board.png`, `eagle2geda.png` (`<img>`/`<a>` pairs)
- Modify: `_posts/2007-02-20-compiling-tpserver-cpp-under-windows-part-2.md` — `running-on-windows.png`
- Modify: `_posts/2007-02-21-compiling-tpserver-cpp-under-windows-part-3.md` — `tpserver-standalone.zip`
- Modify: `_posts/2007-02-25-tailor-darcs2svn-tp.md` — `darcs2svn-start.sh`
- Modify: `_posts/2007-03-24-liferea-bug.md` — `liferea.png`
- Modify: `_posts/2009-01-27-xcompiling-cygwin-on-linux-for-windows.md` — the site-relative `/~tim/crosstool-cygwin-gcc336.tar.bz2` link (leave the external thousandparsec.net one in the comments HTML alone)

- [ ] **Step 9.1: Enumerate the exact internal references**

```bash
grep -rnE '(\]\(|href="|src=")(https?://blog\.mithis\.net)?/(wp-content/uploads/2007/0[23]|~tim/)' _posts/
```

- [ ] **Step 9.2: Edit each post.** Markdown image links: replace `[![alt](img-url)](link-url "title")` with `*[Screenshot lost in a pre-2026 server move]*` keeping any caption text. Download links: replace `[filename](url)` with `` `filename` `` + " *(file lost in a pre-2026 server move)*". **The two eagle posts are different:** they pass the dead URLs as `col1_href=`/`col1_src=` parameters to `{% include two-col.html %}`. Don't hand-write block HTML (content lint) — the include supports markdown text columns: drop the image column's `colN_href/src/alt/title/width/height` params (col1 in `eagle-for-pcb.md`, col2 in `eagle2geda-symbol-converter.md`) and pass that column's `colN_md` with a captured loss-note instead (see the existing `eagle_right`/`eagle2geda_prose` capture patterns in the same posts).

- [ ] **Step 9.3: Lint, build, verify, commit**

```bash
uv run python -m scripts.fidelity.lint_content _posts --asset-root .
JEKYLL_ENV=production bundle3.3 exec jekyll build
grep -rloE '(href|src)=["'"'"'](https?://blog\.mithis\.net)?/(wp-content/uploads/2007/0[23]|~tim/)' --include='*.html' _site/archives/ | wc -l   # expect 0 (both quote styles: two-col.html emits single-quoted src/href)
git add _posts/ && git commit -m "De-link files dead since 2007 (seven posts)

board.png, eagle2geda.png, running-on-windows.png, liferea.png,
darcs2svn-start.sh, tpserver-standalone.zip and the /~tim/ crosstool
tarball have been 404 since ~2007 (Wayback CDX has only 404 captures).
Keep the prose, drop the links, note the loss inline.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 10: Promote the internal-link checker to `scripts/` + CI gate

**Files:**
- Create: `scripts/check_internal_links.py`
- Modify: `.github/workflows/jekyll.yml` (add step after "Build with Jekyll")

- [ ] **Step 10.1: Create `scripts/check_internal_links.py`**

```python
"""Fail if _site HTML links to internal URLs that don't resolve to built files.

Checks href/src values that are site-relative (/...) or absolute to
blog.mithis.net against files in _site/, mimicking GitHub Pages
resolution (directory index.html/index.xml, extensionless -> .html).
Scheme-relative (//host/...) and external URLs are ignored.
"""

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE = Path("_site")
# Both quote styles: _includes/two-col.html emits single-quoted href/src.
ATTR_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")

# Known-dead URLs intentionally left in place (add sparingly, with a reason).
ALLOWLIST: set[str] = set()


def target_exists(path: str) -> bool:
    path = unquote(path.split("#")[0].split("?")[0])
    if not path or path == "/":
        return True
    rel = path.lstrip("/")
    p = SITE / rel
    if p.is_file():
        return True
    if p.is_dir() and ((p / "index.html").is_file() or (p / "index.xml").is_file()):
        return True
    if (SITE / (rel.rstrip("/") + ".html")).is_file():
        return True
    return False


def main() -> int:
    broken: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for html in SITE.rglob("*.html"):
        text = html.read_text(errors="replace")
        for m in ATTR_RE.finditer(text):
            url = m.group(1)
            if url.startswith(("http://blog.mithis.net", "https://blog.mithis.net")):
                path = urlparse(url).path
            elif url.startswith("//"):
                continue
            elif url.startswith("/"):
                path = url
            else:
                continue
            if path in ALLOWLIST or target_exists(path):
                continue
            broken[path] += 1
            examples.setdefault(path, str(html.relative_to(SITE)))

    print(f"{len(broken)} distinct broken internal URLs "
          f"({sum(broken.values())} total references)")
    for path, count in broken.most_common():
        print(f"{count:5d}  {path}   (e.g. in {examples[path]})")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 10.2: Run against the current build — expect CLEAN after Tasks 1–9**

```bash
JEKYLL_ENV=production bundle3.3 exec jekyll build
uv run python scripts/check_internal_links.py
```

Expected: `0 distinct broken internal URLs (0 total references)`, exit 0. If anything remains, it's a real straggler — fix it (repeat the relevant task pattern) before wiring CI.

- [ ] **Step 10.3: Add the CI step** in `.github/workflows/jekyll.yml`, after the "Build with Jekyll" step:

```yaml
      - name: Check internal links
        run: uv run python scripts/check_internal_links.py
```

- [ ] **Step 10.4: Commit**

```bash
git add scripts/check_internal_links.py .github/workflows/jekyll.yml
git commit -m "CI: fail the build on broken internal links

The GSC cleanup found the site emitting ~177 distinct broken internal
URLs (~1216 references) — dead feed links, a mangled tag-link pattern,
a missing category page. This gate keeps them from coming back.

Part of #GSC

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 11: Deploy and verify live

- [ ] **Step 11.1: Push and watch CI** (per [[check-ci-and-deployment]] — green CI is necessary, not sufficient)

```bash
git push origin main
gh run watch --exit-status "$(gh run list --commit "$(git rev-parse HEAD)" --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run list --limit 1
```

(If the `--commit` lookup returns empty, the run hasn't registered yet — re-run the lookup after a few seconds rather than grabbing `--limit 1` blind, which can race onto the *previous* run.)

(Foreground `sleep` is blocked in this environment; `gh run watch` blocks until the run finishes and exits non-zero on failure.)

Expected: `completed success`.

- [ ] **Step 11.2: Verify the deployed fixes**

```bash
curl -s https://blog.mithis.net/sitemap.xml | grep -c "<loc>"                     # ~200
curl -s https://blog.mithis.net/sitemap.xml | grep -cE "net/category/|404\.html"  # 0 (real pages are /archives/...)
curl -s -o /dev/null -w "%{http_code}\n" https://blog.mithis.net/archives/category/timvideos-us/hdmi2usb/  # 200
curl -s -o /dev/null -w "%{http_code}\n" https://blog.mithis.net/archives/category/hdmi2usb/   # 200 (stub)
curl -s -o /dev/null -w "%{http_code}\n" https://blog.mithis.net/archives/category/rcs-darcs/  # 200 (stub)
curl -s https://blog.mithis.net/ | grep -c "comments/feed"                        # 0
curl -s https://blog.mithis.net/ | grep -c "gitweb"                               # 0
```

- [ ] **Step 11.3: Update CLAUDE.md** — commit-trailer line (D5) and the "Galleries are PINNED" / linting notes stay; adjust the "Commit messages" bullet to the current model attribution. Commit.

---

### Task 12: Search Console actions (manual, in the GSC UI)

- [ ] **Step 12.1: Sitemaps section** (`https://search.google.com/search-console/sitemaps?resource_id=https://blog.mithis.net/`): delete any stale submissions (`sitemap_index.xml`, `sitemap.xml.gz`, `feed.xml` if present); ensure `https://blog.mithis.net/sitemap.xml` is submitted and reads "Success".
- [ ] **Step 12.2: Export per-reason URL lists** (open each reason under Indexing → Pages → click the reason → Export). The zip attached to the alert only has summary counts. Cross-check the 404 list against this plan's inventory; anything not explained by (a) dead WP sitemap XMLs, (b) the now-fixed emitted links, (c) `/comments/feed/`-style legacy endpoints, (d) date archives / trailing-slash variants, gets triaged into Task 13.
- [ ] **Step 12.3: Click "Validate Fix"** on: Not found (404), Page with redirect, Server error (5xx), Excluded by 'noindex', Alternative page with proper canonical tag. (The 5xx entries are pre-cutover WordPress artifacts; GitHub Pages will serve 200/404 and validation will clear them.)
- [ ] **Step 12.4: URL Inspection → Request Indexing** for the homepage and the top ~10 posts (pick from GSC's Performance report).
- [ ] **Step 12.5: Expectations note:** "Crawled/Discovered – currently not indexed" clears over weeks, not days. The trend is already right: indexed pages 5 → 64 since the 2026-05-30 cutover; Google's known-URL backlog shrank 1324 → 425. Most of the remaining 326 URLs are legacy feed/archive cruft that *should* stay unindexed; success is the count shrinking, not reaching zero. Re-check in 2–3 weeks.

---

### Task 13 (conditional — only if the Step 12.2 export shows them in volume):

- **Trailing-slash post variants** (`/archives/<cat>/<id>-<slug>/`, currently 404 while the canonical no-slash URL is 200): add a small `_plugins/` generator that emits a jekyll-redirect-from-style stub `index.html` (meta refresh + canonical) at `<post-url>/` for every post. Custom plugins run — the site uses the GitHub Actions builder.
- **Date archives** (`/archives/date/YYYY/MM`, listed in the old `sitemap-archives.xml`): if Google keeps hammering them, add stub pages redirecting to `/` (or a real yearly archive page if ever wanted). Otherwise let them 404 and age out.
- **`?p=NNN` shortlinks**: GitHub Pages ignores query strings and serves the homepage, whose canonical tag points at `/` — Google folds these correctly. No action possible or needed.

---

## Cleanup

- [ ] `rm -rf tmp/gsc-coverage tmp/check_wayback.py tmp/check_missing_term_pages.py tmp/check_internal_links.py tmp/linkcheck-before.txt` (the checker lives in `scripts/` now; per convention, tmp files get cleaned).
- [ ] Close the tracking issue once Task 12 validations are underway; GitHub auto-close only catches the FIRST `#N` per commit — `gh issue close` the rest manually if needed.
