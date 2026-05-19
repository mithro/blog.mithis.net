# P3 Findings: Recovery Data for 4 Missing Posts (IDs 15, 35, 84, 92)

**Date:** 2026-05-19
**Branch:** `migration-p3-missing-posts`
**Worktree:** `/home/tim/github/mithro/blog.mithis.net/.worktrees/migration-p3-missing-posts`

---

## Executive Summary

All 4 missing posts are recoverable from the insurance captures (`exports/p3-missing-raw/{15,35,84,92}.html`). The live site returns HTTP 500 for all 4 posts (site root is HTTP 200; the posts themselves trigger a server error). The insurance captures contain the full article HTML (entry-content) but are TRUNCATED at the end — the comment section is cut off mid-tag, making comment content unrecoverable from the insurance captures alone.

Comments were recovered for posts 84 and 92 via Wayback Machine. Posts 15 and 35 have truncated/absent comments: post 15 shows comment-ID 3 in the 2009 Wayback but with no content; post 35 has no Wayback snapshot available. Net result: posts 15 and 35 ship with no comments; posts 84 and 92 get 3 comments each from Wayback (fully extracted below).

---

## A. Per-Post Recovery Data

### Post 15: Thousand Parsec Protocol Overview

**Oracle source:** Insurance capture `exports/p3-missing-raw/15.html` (authoritative content source)
**Live URL:** `https://blog.mithis.net/archives/tp/15-tp-protocol-overview` → HTTP 500 (confirmed)
**`?p=15`:** Redirects 301 → `/archives/tp/15-tp-protocol-overview` then 500
**Wayback (2009-01-07):** `http://web.archive.org/web/20090107105158/http://blog.mithis.net/archives/tp/15-tp-protocol-overview` — no comments in that snapshot

**Extracted metadata:**
- `title:` Thousand Parsec Protocol Overview
- `date:` `2007-02-23T01:21:13+1000`  (from `<abbr class="published" title="...">`)
- `author:` `mithro` (confirmed from `/archives/author/mithro` byline in all 4 captures)
- `wordpress_category:` `tp` (from canonical URL path)
- `categories:` `[tp]` (single entry matching `wordpress_category`, per corpus convention)
- `slug:` `tp-protocol-overview`
- `permalink:` `/archives/tp/15-tp-protocol-overview`
- `wordpress_url:` `https://blog.mithis.net/archives/tp/15-tp-protocol-overview`
- `wordpress_id:` `15`

**Content structure:**
- 5 `<p>` paragraphs
- Three distinct `<dl>` blocks (nested: one `<dl>` contains a sub-`<dl>`)
- No images, no `<pre>`, no `<code>`, no `<ul>`, no `<ol>`, no `<blockquote>`
- Key conversion challenge: nested `<dl>/<dt>/<dd>` must be converted to Markdown definition lists or prose (kramdown supports `<dl>` natively; see body conversion notes §C)
- No inline `<style>` tags in content
- HTML entities: `&#8216;` `&#8217;` `&#8220;` `&#8221;` throughout (smart quotes)

**Excerpt** (live-migrated convention — first ~2 sentences truncated):
```
I've been planning to try and get tp04 into draft stage for a while now. However the
AI competition and RL has kept me really busy so I haven't got time to do the draft yet.....
```

**Comments:** 0 recoverable (insurance capture truncated mid-tag at comment-ID 3 span; Wayback 2009 shows 0 comments). Ship with no `_data/comments/` entries.

---

### Post 35: Using Tailor to go to git

**Oracle source:** Insurance capture `exports/p3-missing-raw/35.html`
**Live URL:** `https://blog.mithis.net/archives/tp/35-using-tailor-to-go-to-git` → HTTP 500
**Wayback:** NOT AVAILABLE (Wayback API returned no snapshot for post 35)

**Extracted metadata:**
- `title:` Using Tailor to go to git
- `date:` `2007-04-21T08:17:42+1000`
- `author:` `mithro`
- `wordpress_category:` `tp`
- `categories:` `[tp]`
- `slug:` `using-tailor-to-go-to-git`
- `permalink:` `/archives/tp/35-using-tailor-to-go-to-git`
- `wordpress_url:` `https://blog.mithis.net/archives/tp/35-using-tailor-to-go-to-git`
- `wordpress_id:` `35`

**Content structure:**
- 9 `<p>` paragraphs with `<a>` links throughout
- No images, no `<pre>`, no `<code>`, no lists, no `<dl>`, no `<blockquote>`
- Straightforward prose; all links are external URLs
- No inline `<style>` tags in content
- HTML entities throughout (smart quotes, `&#8217;`)

**Excerpt:**
```
As our code repositories for Thousand Parsec where down anyway (because of the host being
compromised), we decided to do something we had been thinking about for a while.....
```

**Comments:** 0 recoverable (insurance capture truncated mid-tag at comment-ID 9; no Wayback snapshot). Ship with no `_data/comments/` entries.

---

### Post 84: My three weeks on a Mac

**Oracle source:** Insurance capture `exports/p3-missing-raw/84.html` (content) + Wayback `http://web.archive.org/web/20160506070230/https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac` (comments)
**Live URL:** `https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac` → HTTP 500
**Wayback (2016-05-06):** HTTP 200, 76 KB — used for comments only

**Extracted metadata:**
- `title:` My three weeks on a Mac
- `date:` `2008-07-08T14:00:38+1000`
- `author:` `mithro`
- `wordpress_category:` `ubuntu`
- `categories:` `[ubuntu]`
- `slug:` `my-three-weeks-on-a-mac`
- `permalink:` `/archives/ubuntu/84-my-three-weeks-on-a-mac`
- `wordpress_url:` `https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac`
- `wordpress_id:` `84`

**Content structure:**
- 8 `<p>` paragraphs
- Inline bold via `<span style="font-weight: bold">` (NOT `<strong>`) — these must be converted to `**text**` in Markdown (the `style=` attribute is structural HTML that must not appear in committed posts)
- No images, no `<pre>`, no `<code>`, no lists, no `<dl>`, no `<blockquote>`
- No inline `<style>` blocks

**Excerpt:**
```
As everyone knows, I recently started at Google. When I started I was given a MacBook
Pro to use as the company laptop before I had a chance to change it, I had to head off.....
```

**Note on filename:** `2008-07-08-my-three-weeks-on-a-mac.md`. Another post already exists at `2008-07-08-babylon-5-dvd-copy-protection.md` — no collision, different slug.

**Comments:** 3 comments recovered from Wayback. Content source: Wayback. Dates derived from human-readable date text (the `abbr title` attribute incorrectly stores the POST pub date, not the comment date; correct dates parsed from visible text).

| ID | Author | Date (UTC) | Author URL | Message (summary) |
|----|--------|-----------|-----------|-------------------|
| 7023 | Ryan Neufeld | 2008-07-09T01:39:00+00:00 | http://www.hammerofcode.com/ | command-tab tip for switching windows |
| 7024 | mithro | 2008-07-09T08:48:00+00:00 | http://blog.mithis.net/ | reply: alt-tab still requires two keystrokes |
| 7150 | Pierre Phaneuf | 2008-10-17T05:05:00+00:00 | http://pphaneuf.livejournal.com/ | Google-specific slowness + trash quirks |

Full comment HTML messages (as extracted, with HTML entities for YAML storage):

**Comment 7023 message:**
```html
<p>I won&#8217;t go into a big fanboy rant here (since I&#8217;ve been using my mac for a month or two now and lvoe it) but here is a tip: command-tab (alt-tab) cycles between programs, and command-~ cycles between windows of an application.</p>
```

**Comment 7024 message:**
```html
<p>Actually that was exactly what I was complaining about. In Windows/Linux I can just use Alt-Tab to get to any window, with Mac I have to use two keys to do the same thing!</p>
```

**Comment 7150 message:**
```html
<p>The sluggishness of the password box is a Google thing. I also occasionally have to switch to a console and kill off the screen saver dialog box on my Linux workstation, because it goes completely dead on occasion. My Google laptop tends to &#8220;beachball&#8221; a lot more than my other Mac, so while I don&#8217;t really know what&#8217;s up, there&#8217;s definitely something fishy.</p> <p>The trash is also idiotic in other ways, like when you empty it, but it tells you a file is in use. Just unlink the damned thing and forget about it, will you?</p> <p>Weirdly enough, a lot of Unix/Linux hackers are annoyed by the way applications are a first-class entity, rather than windows, but I like the Mac way better. I thought of hacking my window manager to simulate that based on the WM_CLASS property more than once, but I tend to be okay. When I use a Linux box, I often end up using workspaces in that way.</p>
```

---

### Post 92: WTF power scripts went in Intrepid….

**Oracle source:** Insurance capture `exports/p3-missing-raw/92.html` (content) + Wayback `http://web.archive.org/web/20150927085437/http://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid` (comments)
**Live URL:** `https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid` → HTTP 500
**Wayback (2015-09-27):** HTTP 200, 75 KB

**Extracted metadata:**
- `title:` `WTF power scripts went in Intrepid….` (HTML-unescaped: `&#8230;` → `…`)
- `date:` `2009-01-19T15:12:19+1000`
- `author:` `mithro`
- `wordpress_category:` `uncategorized`
- `categories:` `[uncategorized]`
- `slug:` `power-scripts-in-intrepid`
- `permalink:` `/archives/uncategorized/92-power-scripts-in-intrepid`
- `wordpress_url:` `https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid`
- `wordpress_id:` `92`

**Content structure:**
- 8 `<p>` paragraphs
- 2 `<blockquote>` blocks, each wrapping a WP-Syntax code block (`<div class="wp_syntax"><table><tr><td class="code"><pre class="bash" ...>`)
- The `<pre>` content is syntax-highlighted bash code (HTML-encoded with `<span>` color tags)
- 0 images, 0 `<ul>/<ol>`, 0 `<dl>`
- Inline `<i>` (italic) tags used for file paths: must convert to `*path*` Markdown
- `<b>` tags: convert to `**text**`

**WP-Syntax code extraction:** The two code blocks (from `<pre class="bash">`) contain:
1. Script 1 (`/etc/acpi/resume.d/99-custom.sh`):
   ```bash
   #! /bin/sh
   # Turn off the CD drive and the bluetooth device
   echo 1 > /sys/devices/platform/sony-laptop/cdpower
   echo 0 > /sys/devices/platform/sony-laptop/cdpower
   
   echo 1 > /sys/devices/platform/sony-laptop/bluetoothpower
   echo 0 > /sys/devices/platform/sony-laptop/bluetoothpower
   ```
2. Script 2 (`/etc/pm/sleep.d/10-custom`):
   ```bash
   #!/bin/sh -e
   case "$1" in
   	resume)
   		# Turn off the CD drive and the bluetooth device
   		echo 1 > /sys/devices/platform/sony-laptop/cdpower
   		echo 0 > /sys/devices/platform/sony-laptop/cdpower
   
   		echo 1 > /sys/devices/platform/sony-laptop/bluetoothpower
   		echo 0 > /sys/devices/platform/sony-laptop/bluetoothpower
   	;;
   esac
   ```

These must be converted from WP-Syntax HTML (`<pre class="bash">` with `<span>` color tags) to fenced Markdown code blocks (` ```bash ... ``` `). The `<blockquote>` wrappers around the WP-Syntax divs must be dropped (they are a WP quirk, not semantic blockquotes). The `<span>` color-coding tags must be stripped to plain text. The `&nbsp;` empty lines within code should become blank lines.

**Excerpt:**
```
On previous versions of Ubuntu, the scripts which are called after a resume from suspend
have been found in /etc/acpi/resume.d directory. I used this functionality to turn off.....
```

**Note on filename:** `2009-01-19-power-scripts-in-intrepid.md`. Two posts already exist on 2009-01-19 (`utf-8-in-python` and `firefox3-cookies-in-python`) — no slug collision, different slugs.

**Comments:** 3 comments recovered from Wayback. Dates parsed from human-readable text (same `abbr title` bug — shows post pub date).

| ID | Author | Date (UTC) | Author URL | Message (summary) |
|----|--------|-----------|-----------|-------------------|
| 7164 | David Adam | 2009-01-21T18:55:00+00:00 | http://zanchey.ucc.asn.au/ | Thanks for the explanation |
| 7212 | paul | 2009-05-21T05:11:00+00:00 | (none) | cheers, exactly what i needed |
| 7224 | Jon | 2009-10-28T23:27:00+00:00 | http://jmtd.net/ | rant about undocumented change |

Full comment HTML messages:

**Comment 7164 message:**
```html
<p>Awesome. This was frustrating me too &#8211; thanks for your explanation.</p>
```

**Comment 7212 message:**
```html
<p>cheers for this, exactly what i needed.</p>
```

**Comment 7224 message:**
```html
<p>What an absolute pain in the arse this is. Someone had to go and convert the maintainer-supplied stuff in acpi.d across to the pm.d, it would not have been much trouble to put a check in the package postinst script to see if there was stuff lying around and inform the administrator if so, let alone document it in the release notes.</p>
```

---

## B. Target Format (exact)

### B1. Front-matter shape — live-migrated post (canonical)

Key order (alphabetical as used in corpus — YAML dump default):
```yaml
---
author: mithro
categories:
- <wp_category_slug>
date: <ISO-8601-with-offset-no-colon>
excerpt: '<first sentence(s), ~200 chars, ending with .....>'
layout: post
permalink: /archives/<category>/<id>-<slug>
title: <title string>
wordpress_category: <slug>
wordpress_id: <integer>
wordpress_url: https://blog.mithis.net/archives/<category>/<id>-<slug>
---
```

**Rules confirmed by corpus inspection:**
- Keys are in alphabetical order (author, categories, date, excerpt, layout, permalink, title, wordpress_category, wordpress_id, wordpress_url)
- `categories:` contains ONE entry matching `wordpress_category` (all 72 existing posts follow this — WordPress display-name categories like "Highlights" or "Thousand Parsec" are NOT stored; only the URL-slug category is)
- `date:` format for 2007–2009 era: unquoted ISO 8601 with `+NNNN` offset (no colon): e.g. `2007-02-23T01:21:13+1000` — matches peers like `2007-04-14T05:48:54+1000`, `2007-04-25T21:36:04+1000`, `2008-07-08T14:43:04+1000`, `2009-01-19T12:58:28+1000`
- `excerpt:` single-quoted string (needed when excerpt contains apostrophes) or unquoted; truncated at ~200 chars ending with `.....` (5 dots)
- `layout: post` always
- `title:` unquoted if no YAML-special chars; smart quotes and em-dashes are literal UTF-8 (decoded from HTML entities)
- No `wayback_recovered:` key for insurance-capture-sourced posts

### B2. Front-matter shape — Wayback-recovered post

```yaml
---
author: mithro
categories:
- <slug>
date: <ISO-8601-with-offset>
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/<category>/<id>-<slug>
title: <title>
wayback_recovered: true
wordpress_category: <slug>
wordpress_id: <integer>
wordpress_url: https://blog.mithis.net/archives/<category>/<id>-<slug>
---
```

**Key difference:** `excerpt: Recovered from Wayback Machine archive` (literal, no quotes) and `wayback_recovered: true` inserted between `permalink`/`title` and `wordpress_category` (alphabetical order).

**P3 DECISION:** All 4 posts have their article content from the insurance captures (not Wayback), so they use the **live-migrated shape** (no `wayback_recovered: true`, no "Recovered from Wayback Machine archive" excerpt). Posts 84 and 92 use Wayback only for comments, not content — this does not change the post front-matter shape. The excerpt is derived from the post's actual opening text.

### B3. Comments — both forms

**Aggregate file** `_data/comments/<id>-<slug>.yml`:
```yaml
- date: 2008-07-09 01:39:00 +0000
  id: '7023'
  message: '<p>I won&#8217;t go into ...</p>'
  name: Ryan Neufeld
  wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac#comment-7023
```

Schema keys (in order): `date`, `id`, `message`, `name`, `wordpress_url`
- `date:` space-separated `YYYY-MM-DD HH:MM:SS +0000` (UTC, NOT ISO-8601 with T)
- `id:` quoted string `'NNNN'`
- `message:` HTML string (may be block scalar or flow; single-quoted if contains `<p>` tags with no interior quotes, or plain if no special chars)
- `name:` plain string (author display name)
- `wordpress_url:` URL with `#comment-NNNN` fragment

**Per-comment directory** `_data/comments/<id>-<slug>/comment-<id>-<YYYYMMDD>-<HHMMSS>.yml`:
```yaml
date: 2008-07-09 01:39:00 +0000
id: '7023'
message: <p>I won&#8217;t go into ...</p>
name: Ryan Neufeld
wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac#comment-7023
```

Same keys, same values, but singular object (no leading `- `). Filename format: `comment-<id>-<YYYYMMDD>-<HHMMSS>.yml` where date is the comment date in UTC.

**NOTE:** If a comment has no URL (like paul/post-92 comment 7212), omit `wordpress_url` from the per-comment file and aggregate list, OR set it to just the post URL without fragment — follow the existing pattern (existing comments always have `wordpress_url` with fragment; for no-URL authors the name-link is absent, but `wordpress_url` still points to the post). Recommend including the post URL + fragment regardless.

### B4. Filename convention

`_posts/YYYY-MM-DD-<slug>.md` where `YYYY-MM-DD` is derived from the post date (local date, +1000 timezone):
- Post 15: `2007-02-23-tp-protocol-overview.md`
- Post 35: `2007-04-21-using-tailor-to-go-to-git.md`
- Post 84: `2008-07-08-my-three-weeks-on-a-mac.md`
- Post 92: `2009-01-19-power-scripts-in-intrepid.md`

### B5. Faithful-structure mandate (CRITICAL for P3)

These 4 posts are authored FRESH in P3. Unlike the pre-existing 72 migrated posts (whose systemic flat-list/blank-line divergence is deferred to P6/SYSTEMIC), P3-authored posts:

1. **MUST faithfully reproduce the oracle's rendered structure** in Markdown: correct paragraph separation (blank lines between `<p>` elements → blank lines between paragraphs), correct nesting of `<dl>` content (use Markdown definition list syntax or convert to prose/bold pattern), correct `<blockquote>`/`<pre>` → fenced code blocks
2. **MUST be content-linter clean (0 BLOCK_HTML, 0 LIQUID_LEAK, 0 MISSING_IMAGE findings)** for the 4 new files
3. **MUST NOT contain hardcoded structural HTML** (`<div>`, `<dl>`, `<dt>`, `<dd>`, `<span>`, `<table>`, etc.) in the committed Markdown body
4. The `<span style="font-weight: bold">` in post 84 MUST become `**text**` (inline bold, not block HTML)
5. The `<i>` italic tags in post 92 MUST become `*text*`
6. The WP-Syntax `<pre class="bash">` code blocks MUST become fenced ` ```bash ... ``` ` blocks
7. No images exist in any of the 4 posts, so no image-path decisions needed (no R-P4 convention required for these posts)

**Definition list handling for post 15:** kramdown supports definition lists via `term\n: definition` syntax. However the existing corpus has NO `<dl>` posts (post 15 would be first). Options: (a) use kramdown DL syntax (`term\n: definition`) which renders as `<dl>/<dt>/<dd>` and satisfies the linter (no block HTML); (b) convert each `<dt>/<dd>` to bold heading + paragraph (`**Term**\n\nDefinition text`). Option (b) is simpler and guaranteed linter-clean. Option (a) is more faithful but requires confirming kramdown DL syntax doesn't trigger the linter. **Recommendation:** use bold-term + paragraph pattern for simplicity and guaranteed linter compliance.

---

## C. Recovery Pipeline and Worklist

### C1. Existing tooling analysis

- **`scripts/html_to_markdown.py`:** Batch HTML→Markdown converter for existing post bodies. It removes `<div>` wrappers, converts `<p>`, `<strong>`, `<em>`, `<i>`, `<b>`, `<a>`, `<ul>`, `<ol>`, `<li>`, `<h1>`–`<h6>`, `<blockquote>`, `<code>`, `<pre>` (with language detection), `<span>` tags. **Pitfalls:** (1) strips `<dl>/<dt>/<dd>` incompletely (removes `<div>` but not `<dl>/<dt>/<dd>` tags); (2) `<blockquote>` conversion `r'> \1'` on multiline doesn't prefix every line; (3) no WP-Syntax `<div class="wp_syntax">` handling (would leave the table structure as stray HTML); (4) the `<ol>` counter is defined but `replace_ol_item` is never wired to `re.sub`. **Do NOT run this script on the 4 new posts — it would produce the same artifacts that plagued the 72.**

- **`scripts/extract_missing_posts.py`:** Scrapes live WP pages. Not applicable (posts return 500; content is already in insurance captures).

- **`scripts/wayback_extractor.py`:** Fetches Wayback Machine snapshots. Useful for fetching comment data (already done above). Not needed for post content (insurance captures are complete).

- **`exports/scripts/full_site_scraper.py`:** Full-site scraper. Not needed.

- **`scripts/fidelity/lint_content.py`:** The content linter. MUST be run against each new file before commit. Target: 0 findings per new file.

### C2. Recommended conversion pipeline

For each of the 4 posts:

1. **Content source:** `exports/p3-missing-raw/<id>.html` — extract `<div class="entry-content">` section (use the extraction pattern from `tmp/p3/extract_final_content.py` which correctly identifies the last `entry-content` occurrence as the actual article, not the CSS references in `<style>`)

2. **Convert HTML → Markdown manually (or with the script as starting point, hand-finishing):**
   - `<p>...</p>` → paragraph text + blank line
   - `<a href="URL">text</a>` → `[text](URL)`
   - `<strong>text</strong>` or `<b>text</b>` or `<span style="font-weight: bold">text</span>` → `**text**`
   - `<em>text</em>` or `<i>text</i>` → `*text*`
   - `<dl>/<dt>term</dt><dd>def</dd></dl>` → `**term**\n\ndefinition text\n`
   - `<blockquote>` wrapping WP-Syntax divs → strip the blockquote; extract code from `<pre class="bash">` after stripping all `<span>` tags and unescaping `&gt;`/`&lt;`/`&amp;`/`&nbsp;` → fenced ` ```bash\n...\n``` `
   - HTML entities: `&#8216;`/`&#8217;` → `'`; `&#8220;`/`&#8221;` → `"`; `&#8211;` → `–`; `&#8212;` → `—`; `&#8230;` → `…`; `&gt;` → `>`; `&lt;` → `<`; `&amp;` → `&`

3. **Write the `_posts/YYYY-MM-DD-<slug>.md`** file with correct front matter (see §B1 templates below)

4. **Run linter:** `uv run python -m scripts.fidelity.lint_content <file> --asset-root .` → must be 0 findings

5. **Create comments** (posts 84 and 92 only):
   - Aggregate: `_data/comments/<id>-<slug>.yml`
   - Per-comment dir: `_data/comments/<id>-<slug>/comment-<cid>-<YYYYMMDD>-<HHMMSS>.yml`

### C3. Per-post exact worklist (copy-pasteable front matter)

#### Post 15: `_posts/2007-02-23-tp-protocol-overview.md`

```yaml
---
author: mithro
categories:
- tp
date: 2007-02-23T01:21:13+1000
excerpt: "I've been planning to try and get tp04 into draft stage for a while now.\
  \ However the AI competition and RL has kept me really busy so I haven't got time\
  \ to do the draft yet...."
layout: post
permalink: /archives/tp/15-tp-protocol-overview
title: Thousand Parsec Protocol Overview
wordpress_category: tp
wordpress_id: 15
wordpress_url: https://blog.mithis.net/archives/tp/15-tp-protocol-overview
---
```

**Body conversion notes:**
- 5 paragraphs → 5 Markdown paragraphs separated by blank lines
- Three `<dl>` blocks with many `<dt>/<dd>` pairs, including one nested `<dl>` inside a `<dd>`
- Strategy: `**term**` on its own line, followed by blank line, then definition text as paragraph, then blank line before next term
- Nested `<dl>` inside "Dynamic Objects" `<dd>`: treat inner terms as sub-items with indentation or as sub-bold terms under the parent paragraph
- NO images, no code, no lists

**Comments:** None (no comment data recoverable).

---

#### Post 35: `_posts/2007-04-21-using-tailor-to-go-to-git.md`

```yaml
---
author: mithro
categories:
- tp
date: 2007-04-21T08:17:42+1000
excerpt: "As our code repositories for Thousand Parsec where down anyway (because\
  \ of the host being compromised), we decided to do something we had been thinking\
  \ about for a while...."
layout: post
permalink: /archives/tp/35-using-tailor-to-go-to-git
title: Using Tailor to go to git
wordpress_category: tp
wordpress_id: 35
wordpress_url: https://blog.mithis.net/archives/tp/35-using-tailor-to-go-to-git
---
```

**Body conversion notes:**
- 9 paragraphs with external links → 9 Markdown paragraphs with `[text](url)` links
- Simple prose; no special elements
- One internal link to `http://blog.mithis.com/2007/02/25/using-tailor-creating-subversion-repository-for-thousand-parsec/` (old blog URL) — preserve as-is
- One link to `http://www.thousandparsec.net/~tim/tailor/tpclient-pywx-dev.tailor` — may be dead; preserve as-is

**Comments:** None (no comment data recoverable).

---

#### Post 84: `_posts/2008-07-08-my-three-weeks-on-a-mac.md`

```yaml
---
author: mithro
categories:
- ubuntu
date: 2008-07-08T14:00:38+1000
excerpt: "As everyone knows, I recently started at Google. When I started I was given\
  \ a MacBook Pro to use as the company laptop before I had a chance to change it,\
  \ I had to head off to Mountain View for training...."
layout: post
permalink: /archives/ubuntu/84-my-three-weeks-on-a-mac
title: My three weeks on a Mac
wordpress_category: ubuntu
wordpress_id: 84
wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac
---
```

**Body conversion notes:**
- 8 paragraphs → 8 Markdown paragraphs with blank lines
- 5 paragraphs begin with `<span style="font-weight: bold">BOLD TEXT</span>` — convert to: `**BOLD TEXT**` inline (leading the paragraph)
- No images, no code, no lists
- HTML entities throughout (smart quotes)

**Comments:** 3 comments. Must create both `_data/comments/` forms.

`_data/comments/84-my-three-weeks-on-a-mac.yml`:
```yaml
- date: 2008-07-09 01:39:00 +0000
  id: '7023'
  message: <p>I won&#8217;t go into a big fanboy rant here (since I&#8217;ve been
    using my mac for a month or two now and lvoe it) but here is a tip: command-tab
    (alt-tab) cycles between programs, and command-~ cycles between windows of an
    application.</p>
  name: Ryan Neufeld
  wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac#comment-7023
- date: 2008-07-09 08:48:00 +0000
  id: '7024'
  message: <p>Actually that was exactly what I was complaining about. In Windows/Linux
    I can just use Alt-Tab to get to any window, with Mac I have to use two keys to
    do the same thing!</p>
  name: mithro
  wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac#comment-7024
- date: 2008-10-17 05:05:00 +0000
  id: '7150'
  message: <p>The sluggishness of the password box is a Google thing. I also occasionally
    have to switch to a console and kill off the screen saver dialog box on my Linux
    workstation, because it goes completely dead on occasion. My Google laptop tends
    to &#8220;beachball&#8221; a lot more than my other Mac, so while I don&#8217;t
    really know what&#8217;s up, there&#8217;s definitely something fishy.</p> <p>The
    trash is also idiotic in other ways, like when you empty it, but it tells you
    a file is in use. Just unlink the damned thing and forget about it, will you?</p>
    <p>Weirdly enough, a lot of Unix/Linux hackers are annoyed by the way applications
    are a first-class entity, rather than windows, but I like the Mac way better.
    I thought of hacking my window manager to simulate that based on the WM_CLASS
    property more than once, but I tend to be okay. When I use a Linux box, I often
    end up using workspaces in that way.</p>
  name: Pierre Phaneuf
  wordpress_url: https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac#comment-7150
```

Per-comment files in `_data/comments/84-my-three-weeks-on-a-mac/`:
- `comment-7023-20080709-013900.yml`
- `comment-7024-20080709-084800.yml`
- `comment-7150-20081017-050500.yml`

Each file has the same schema as the aggregate entry but singular (no leading `- `).

---

#### Post 92: `_posts/2009-01-19-power-scripts-in-intrepid.md`

```yaml
---
author: mithro
categories:
- uncategorized
date: 2009-01-19T15:12:19+1000
excerpt: 'On previous versions of Ubuntu, the scripts which are called after a resume
  from suspend have been found in /etc/acpi/resume.d directory. I used this functionality
  to turn off....'
layout: post
permalink: /archives/uncategorized/92-power-scripts-in-intrepid
title: WTF power scripts went in Intrepid….
wordpress_category: uncategorized
wordpress_id: 92
wordpress_url: https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid
---
```

**Body conversion notes:**
- 8 paragraphs with blank lines between each
- File paths in `<i>` → `*path*` italic
- `<b>` → `**text**`
- 2 `<blockquote>` blocks each wrapping a `<div class="wp_syntax">` WP-Syntax table — strip the blockquote and wp_syntax wrapper entirely; extract code text from `<pre class="bash">` with all `<span>` tags stripped; unescape HTML entities (`&gt;` → `>`, `&lt;` → `<`, `&amp;` → `&`, `&nbsp;` → blank line or space); emit as ` ```bash\n...\n``` `
- Code block 1 (script at `/etc/acpi/resume.d/99-custom.sh`): 6 lines + 1 blank line separator
- Code block 2 (script at `/etc/pm/sleep.d/10-custom`): 11 lines case/esac structure
- `&#8220;`/`&#8221;` smart double-quotes → `"` in prose; `&#8216;`/`&#8217;` → `'`

**Comments:** 3 comments. Must create both `_data/comments/` forms.

`_data/comments/92-power-scripts-in-intrepid.yml`:
```yaml
- date: 2009-01-21 18:55:00 +0000
  id: '7164'
  message: <p>Awesome. This was frustrating me too &#8211; thanks for your explanation.</p>
  name: David Adam
  wordpress_url: https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid#comment-7164
- date: 2009-05-21 05:11:00 +0000
  id: '7212'
  message: <p>cheers for this, exactly what i needed.</p>
  name: paul
  wordpress_url: https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid#comment-7212
- date: 2009-10-28 23:27:00 +0000
  id: '7224'
  message: <p>What an absolute pain in the arse this is. Someone had to go and convert
    the maintainer-supplied stuff in acpi.d across to the pm.d, it would not have
    been much trouble to put a check in the package postinst script to see if there
    was stuff lying around and inform the administrator if so, let alone document it
    in the release notes.</p>
  name: Jon
  wordpress_url: https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid#comment-7224
```

Per-comment files in `_data/comments/92-power-scripts-in-intrepid/`:
- `comment-7164-20090121-185500.yml`
- `comment-7212-20090521-051100.yml`
- `comment-7224-20091028-232700.yml`

---

## D. Per-Post Source Summary

| ID | Slug | Category | Content Source | Comments Source | Has Comments | Concern |
|----|------|----------|---------------|-----------------|--------------|---------|
| 15 | `tp-protocol-overview` | `tp` | Insurance capture (200 OK content) | Wayback 2009 (no comments in archive) | 0 | Comment ID 3 exists but content unrecoverable; nested `<dl>` structure needs careful Markdown rendering |
| 35 | `using-tailor-to-go-to-git` | `tp` | Insurance capture (200 OK content) | N/A (no Wayback) | 0 | Comment ID 9 unrecoverable; no Wayback snapshot available |
| 84 | `my-three-weeks-on-a-mac` | `ubuntu` | Insurance capture | Wayback 2016-05-06 | 3 | `<span style="font-weight: bold">` must become `**...**`; both comment forms required |
| 92 | `power-scripts-in-intrepid` | `uncategorized` | Insurance capture | Wayback 2015-09-27 | 3 | WP-Syntax `<pre>` blocks need entity-decoding + span-stripping; both comment forms required; title has `…` entity |

---

## E. P3 Acceptance Gates

1. `_posts` count: 72 → **76** (4 new files added)
2. Content linter (`uv run python -m scripts.fidelity.lint_content` over all `_posts/*.md`): the 4 new files contribute **0 new findings** (corpus stays at the documented 22 R-P4 deferred findings; the 4 new posts are clean)
3. Structure check: `uv run python -m scripts.fidelity.structure_check` → **6/6 PASS** (adding new posts does not affect structural archetypes, but build must succeed)
4. `bundle3.3 exec jekyll build` → **0 errors, 0 warnings**
5. Each new post's permalink resolves to a built `_site` page:
   - `_site/archives/tp/15-tp-protocol-overview.html` exists
   - `_site/archives/tp/35-using-tailor-to-go-to-git.html` exists
   - `_site/archives/ubuntu/84-my-three-weeks-on-a-mac.html` exists
   - `_site/archives/uncategorized/92-power-scripts-in-intrepid.html` exists
6. Comments for posts 84 and 92 present in both forms:
   - `_data/comments/84-my-three-weeks-on-a-mac.yml` (3 entries)
   - `_data/comments/84-my-three-weeks-on-a-mac/` directory (3 files)
   - `_data/comments/92-power-scripts-in-intrepid.yml` (3 entries)
   - `_data/comments/92-power-scripts-in-intrepid/` directory (3 files)
7. No new `wayback_recovered: true` keys in the 4 posts (content from insurance captures, not Wayback)

---

## F. Key Technical Notes

### F1. Live site status
- `https://blog.mithis.net/` → HTTP 200 (TLS cert expired, verify-disabled fetch required; site is up)
- All 4 posts → HTTP 500 (server error; the 500 is the original migration-skip cause documented in FOLLOWUPS.md §P3)
- `?p=<id>` → HTTP 301 redirect to canonical URL → then HTTP 500

### F2. Insurance capture truncation
The `exports/p3-missing-raw/*.html` files are truncated approximately 210 bytes into the `<ol class="commentlist">` section. The files end mid-tag at `<span class="comment-author vcard">`. This is a capture artifact. The article body (entry-content) is fully captured and authoritative.

### F3. Wayback rate limiting
The Wayback Machine API at `http://archive.org/wayback/available` returns HTTP 429 (Too Many Requests) if called in rapid succession. Allow 5–10 seconds between requests. Post 35 has no Wayback snapshot available at all.

### F4. Comment date bug in WP captures
The `<abbr class="comment-published" title="...">` in the Barthelme theme stores the **post's publication date** in the title attribute, not the comment date. The actual comment dates are in the human-readable text inside the abbr element ("July 9, 2008 at 1:39 am") and also in the `<li>` CSS classes (`c-y2008 c-m07 c-d09 c-h11`). Use the human-readable text for exact hour/minute; the class for year/month/day. Dates stored in `_data/comments/` are UTC.

### F5. Recommended pipeline (1-2 lines)
Write each post file directly by hand: copy content from `tmp/p3/<id>-content.html`, convert HTML→Markdown mentally (all 4 posts have simple structure), apply front-matter from §C3 templates. Run `uv run python -m scripts.fidelity.lint_content _posts/YYYY-MM-DD-<slug>.md` after each file to confirm 0 findings. For posts 84 and 92, create both `_data/comments/` forms from the exact YAML in §C3.
