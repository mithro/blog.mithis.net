# P4-FINDINGS — Domain/Deploy triage & plan

**Date:** 2026-05-19
**Phase:** P4 (domain/deploy + 22 R-P4 residual conversion)
**Branch:** migration-p4-domain-deploy
**Oracle:** `https://blog.mithis.net` (TLS cert expired → fetch with `-sk`/unverified context; HTTP 200 confirmed for all reachable posts)
**Worktree:** `/home/tim/github/mithro/blog.mithis.net/.worktrees/migration-p4-domain-deploy`

All oracle fetches performed by `tmp/p4_oracle{2..10}.py` (retained in `tmp/` for the implementer).

---

## A. Core config changes — exact, copy-pasteable

### A.1 `_config.yml` — baseurl and url

**Current state (lines 26–27):**

```yaml
baseurl: "/blog.mithis.net" # the subpath of your site, e.g. /blog
url: "https://mithro.github.io" # the base hostname & protocol for your site
```

**Replacement (exact):**

```yaml
baseurl: "" # custom domain — no subpath prefix
url: "https://blog.mithis.net" # the base hostname & protocol for your site
```

Preserve the inline comment style (trailing `# …` comment on both lines as shown above).

After this change:
- `{{ '/assets/foo.jpg' | relative_url }}` → `/assets/foo.jpg` (empty baseurl → root-relative, identical to plain path)
- `{{ site.url }}` → `https://blog.mithis.net`
- `{{ site.url }}{{ site.baseurl }}/` → `https://blog.mithis.net/`
- All `prepend: site.baseurl | prepend: site.url` patterns → correct absolute `https://blog.mithis.net/…` URLs
- The `relative_url` filter with `baseurl: ""` produces root-relative paths → now identical to plain `/assets/…` paths, making the R-P4 Liquid → plain conversion zero-fidelity-loss

### A.2 `CNAME` — new file

Create `CNAME` in the repo root with exactly this content (one line, single trailing newline):

```
blog.mithis.net
```

GitHub Pages custom-domain format: the file must contain ONLY the bare hostname with no protocol, no trailing slash, and exactly one trailing newline. GitHub Pages reads this file and enforces it as the Pages domain.

### A.3 `.github/workflows/jekyll.yml` — line 47 neutralization

**Current (line 47):**

```yaml
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
```

**Replacement:**

```yaml
        run: bundle exec jekyll build
```

**Justification:** `actions/configure-pages` sets `steps.pages.outputs.base_path` to `/blog.mithis.net` when the repo is named `blog.mithis.net` and no custom domain is configured. Once a custom domain (`CNAME`) is in place, GitHub Pages sets `base_path` to `""` — but this is only guaranteed after the DNS/domain propagation is live in the Pages settings. The safest, cleanest approach is to remove the `--baseurl` flag entirely: `_config.yml` is now authoritative (`baseurl: ""`), and `bundle exec jekyll build` without any flag reads from `_config.yml`. There is no scenario where passing the flag is safer than removing it for a custom-domain deployment.

Do NOT use `--baseurl ""` (empty string argument) — this is unnecessary and error-prone (shell quoting). The `bundle exec jekyll build` alone is correct and minimal.

**Full workflow baseurl/base_path audit:** line 47 is the ONLY location in `.github/workflows/jekyll.yml` that references `base_path` or `baseurl`. No other step uses `steps.pages.outputs.base_path`. The `actions/configure-pages@v5` step (line 43–44) still runs and is still needed — it configures the GitHub Pages deployment environment. Only the `--baseurl` argument to `bundle exec jekyll build` is removed.

### A.4 CRITICAL commit ordering

**The `_config.yml baseurl: ""` change MUST be committed in the SAME commit as — or BEFORE — any R-P4 post conversions.**

Reason: replacing `{{ '/assets/x' | relative_url }}` with plain `/assets/x` in a post is ONLY correct once `baseurl: ""`. Under the old `baseurl: "/blog.mithis.net"`, `relative_url` rendered `/blog.mithis.net/assets/x` but the plain path renders `/assets/x` — which would 404. The two changes are semantically atomic: set baseurl first, then convert posts.

**Recommended commit order (strict):**

1. **Commit 1** (P4-C1): Add `CNAME`, update `_config.yml` (baseurl+url), remove `--baseurl` from workflow — exactly these 3 file changes together. Gate: `bundle3.3 exec jekyll build` clean.
2. **Commit 2** (P4-C2): Convert all 8 posts' R-P4 LIQUID_LEAK lines to plain Markdown/`<img>` — run linter after, must be 0 findings. One commit per post is fine (8 small commits) or batch all 8.
3. **Commit 3** (P4-C3): feed/sitemap verification (custom sitemap.xml categories URL fix — see §C).
4. **Commit 4** (P4-C4): Edge-case URL fixes — rcs-darcs redirect, timvideos-us/hdmi2usb sub-category, Scheme/Sydney/Tailor category pages, 404/search form-action.
5. **Commit 5** (P4-C5): Gemfile + Gemfile.lock update adding `jekyll-redirect-from` (needed by §D redirects).

> **CONTROLLER DECISION (2026-05-19, supersedes the C1/C5 split above):**
> P4-C5's `jekyll-redirect-from` Gemfile/lock/`plugins:` addition was
> deliberately **consolidated into the keystone P4-C1 commit** (`8a1308f`).
> Rationale: it is a one-line, harmless, purely-additive infra prerequisite
> for the later §D redirect work; bundling it with the baseurl/CNAME/workflow
> config keystone keeps all P4 config/infra atomic and avoids a
> disproportionate standalone commit+review cycle for a single gem line. The
> ONLY constraint that is correctness-critical here is the **C1-before-C2**
> ordering (baseurl set before any R-P4 post conversion) — that is preserved.
> The 5-commit split was a suggested granularity, not a correctness contract;
> the functional P4-C1 gate (build clean, zero `/blog.mithis.net/` prefix,
> structure 6/6, corpus still 22) was fully met. Reviewers/P4-Z: treat the
> gem-in-C1 as the sanctioned plan, NOT a deviation/defect.

---

## B. Regenerated 22 R-P4 worklist (current line numbers, exact source text, faithful target)

Regenerated by `tmp/p4_lint.py` (2026-05-19). Exact count: **22 findings = 11 LIQUID_LEAK + 11 MISSING_IMAGE, 0 BLOCK_HTML**. Confirmed: P2 completed cleanly (no BLOCK_HTML residual).

**Line numbers HAVE DRIFTED from P2-FINDINGS §4** (P2/P3 commits modified some posts). The table below uses the current (P4 HEAD) line numbers, verified by the linter run.

### 8 distinct posts / 11 edit sites

#### Post 1: `_posts/2007-05-09-almost-there.md` — 1 edit site (line 19)

**Current line 19 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
[<img alt="CFXS Try2 PCB Board" src="{{ '/assets/images/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg' | relative_url }}"/>]({{ '/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg' | relative_url }})
```

**Oracle (LIVE — `https://blog.mithis.net/archives/pcb/40-almost-there`):**

```html
<a href="https://blog.mithis.net/wp-content/uploads/2007/05/cfxs-try2.jpg" title="CFXS Try2 PCB Board">
  <img src="https://blog.mithis.net/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg" alt="CFXS Try2 PCB Board"/>
</a>
```

The original is a linked thumbnail (thumbnail image linking to the full-size image). The Markdown `[<img …/>](…)` form is the faithful representation (it already IS a linked thumbnail — just with `relative_url` that must be replaced).

**Asset existence:** `assets/images/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg` — EXISTS; `assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg` — EXISTS.

**Faithful replacement (pure Markdown):**

```
[![CFXS Try2 PCB Board](/assets/images/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg)](/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg)
```

Note: The original `[<img alt=…/>](…)` Liquid form can become pure Markdown `[![alt](thumb)](full)` — no inline HTML needed. This is the preferred form per spec §7 (Markdown over inline HTML).

---

#### Post 2: `_posts/2007-08-17-resume.md` — 1 edit site (line 18)

**Current line 18 (LIQUID_LEAK only — no co-located MISSING_IMAGE):**

```
Here is a copy of my Resume. You can find it in [PDF]({{ '/assets/images/wp-content/uploads/2007/08/resume.pdf' | relative_url }}) form or plain TXT form.
```

**Oracle (LIVE — `https://blog.mithis.net/archives/uncategorized/48-resume`):**

```html
<a href="http://blog.mithis.net/wp-content/uploads/2007/08/resume.pdf" title="Resume - PDF">PDF</a>
```

Plain PDF link, no image, no thumbnail.

**Asset existence:** `assets/images/wp-content/uploads/2007/08/resume.pdf` — EXISTS.

**Faithful replacement:**

```
Here is a copy of my Resume. You can find it in [PDF](/assets/images/wp-content/uploads/2007/08/resume.pdf) form or plain TXT form.
```

---

#### Post 3: `_posts/2008-02-04-google-patchwork.md` — 2 edit sites (lines 17 and 19)

**Current line 17 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
[<img alt="Google patchwork." src="{{ "/assets/images/wp-content/uploads/2008/02/map-patchwork.png" | relative_url }}"/>
```

**Current line 19 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
[<img alt="Google Transsision" src="{{ "/assets/images/wp-content/uploads/2008/02/map-change.png" | relative_url }}"/>
```

**Oracle (LIVE — `https://blog.mithis.net/archives/google/67-google-patchwork`):**

```html
<a href="https://blog.mithis.net/wp-content/uploads/2008/02/map-patchwork.png" title="Google patchwork.">
  <img src="https://blog.mithis.net/wp-content/uploads/2008/02/map-patchwork.png" alt="Google patchwork."/>
</a>
…
<a href="https://blog.mithis.net/wp-content/uploads/2008/02/map-change.png" title="Google Transsision">
  <img src="https://blog.mithis.net/wp-content/uploads/2008/02/map-change.png" alt="Google Transsision"/>
</a>
```

Both are linked images (same URL for both href and src — WP lightbox pattern: clicking the image opens the same full-size image). Note: Both current source lines have UNCLOSED `[<img …/>` Markdown links (the `](`…`)` closing is missing). P2-FINDINGS §4 noted "repair the two unclosed `[<img …` md-links".

**Asset existence:** `assets/images/wp-content/uploads/2008/02/map-patchwork.png` — EXISTS; `assets/images/wp-content/uploads/2008/02/map-change.png` — EXISTS.

**Faithful replacement for lines 17–19 block:**

```markdown
[![Google patchwork.](/assets/images/wp-content/uploads/2008/02/map-patchwork.png)](/assets/images/wp-content/uploads/2008/02/map-patchwork.png)
If you zoom out one more level, the map data totally change,
[![Google Transsision](/assets/images/wp-content/uploads/2008/02/map-change.png)](/assets/images/wp-content/uploads/2008/02/map-change.png)
```

The linked-image form `[![alt](src)](href)` where `src == href` is the faithful WP-lightbox pattern. The prose on line 18 (between the two images) stays unchanged.

---

#### Post 4: `_posts/2008-02-18-cfxs-free.md` — 1 edit site (line 27, NOTE: drifted from P2-FINDINGS line 22)

**Current line 27 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt="" src="{{ "/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg" | relative_url }}"/>
```

**Oracle (LIVE — `https://blog.mithis.net/archives/ideas/72-cfxs-free`):**

```html
<img src="https://blog.mithis.net/wp-content/uploads/2007/05/cfxs-try2.jpg" alt=""/>
```

Standalone image, no link wrapper, empty alt attribute. This uses the same full-size board photo. The original used an inline `<img>` (not a Markdown image).

**Asset existence:** `assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg` — EXISTS.

**Faithful replacement:** The original had an empty alt. Markdown `![](/assets/…)` produces `<img alt="">` which is faithful. Use pure Markdown:

```markdown
![](/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg)
```

---

#### Post 5: `_posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md` — 1 edit site (line 22)

**Current line 22 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt="Tulip - The ship from Starhunter"  height="219" src="{{ "/assets/images/wp-content/uploads/2009/05/screenshot.png" | relative_url }}" title="Tulip - The ship from Starhunter" width="300"/>
```

**Oracle:** This post returns HTTP 500 on the live site and Wayback returned HTTP 429 (rate-limited). The post was recovered from Wayback (front matter has `wayback_recovered: true`). The inline `<img>` with `height=`, `width=`, and `title=` attributes cannot be expressed in Markdown without losing the attributes. The LIQUID_LEAK pattern is clear and unambiguous regardless of the oracle response.

**Asset existence:** `assets/images/wp-content/uploads/2009/05/screenshot.png` — EXISTS.

**Faithful replacement:** Per spec §7, a minimal inline `<img>` is allowed where Markdown cannot express it. This `<img>` has `height`, `width`, and `title` attributes Markdown cannot express. Keep as minimal inline HTML (replacing only the `relative_url` Liquid):

```html
<img alt="Tulip - The ship from Starhunter" height="219" src="/assets/images/wp-content/uploads/2009/05/screenshot.png" title="Tulip - The ship from Starhunter" width="300"/>
```

(Remove the double-space before `height=`; normalize to single space. The linter permits inline `<img>` — only structural block-level HTML is flagged as BLOCK_HTML.)

**Note for linter:** This line produces a LIQUID_LEAK because `{{` is in `src=`. After replacing `{{ … | relative_url }}` with `/assets/…`, the `<img>` itself is an inline element, NOT flagged as BLOCK_HTML (confirmed: `BLOCK_HTML` check is block-level detection; `<img>` standalone on its own line may be BLOCK_HTML if the linter treats it as block — verify post-edit that no BLOCK_HTML finding appears for this line). If it does appear, a `<!-- fidelity-allow: BLOCK_HTML necessary-embed — inline img with attributes Markdown cannot express -->` sentinel may be required.

---

#### Post 6: `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md` — 2 edit sites (lines 133 and 135, NOTE: drifted from P2-FINDINGS lines 125/127)

**Current line 133 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt="Error: Import of the VPN settings failed." class="alignnone size-full wp-image-1835" height="265" sizes="(max-width: 745px) 100vw, 745px" src="{{ "/assets/images/wp-content/uploads/2013/10/VPN-error.png" | relative_url }}" srcset="/assets/images/wp-content/uploads/2013/10/VPN-error.png 745w, https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error-300x106.png 300w" width="745"/>
```

**Current line 135 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt="Export VPN settings" class="alignnone size-full wp-image-1836" height="306" sizes="(max-width: 442px) 100vw, 442px" src="{{ "/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png" | relative_url }}" srcset="/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png 442w, https://blog.mithis.net/wp-content/uploads/2013/10/VPN-encrypt-300x207.png 300w" width="442"/>
```

**Oracle (LIVE — `https://blog.mithis.net/archives/useful-bits/1835-connecting-to-a-fritzbox-under-linux-using-vpnc`):**

- Line 133: VPN-error.png is shown as a linked image: `<a href="…/VPN-error.png" title="Fritz!Box VPN Error" rel="attachment"><img … src="…/VPN-error.png" … /></a>`
- Line 135: VPN-encrypt.png is shown as a linked thumbnail to a WP attachment page (non-faithful URL structure), OR as a full image

Both images have `height`, `width`, `class`, `sizes`, `srcset` attributes that Markdown cannot express. These MUST remain as minimal inline `<img>` (per spec §7).

**Asset existence:** `assets/images/wp-content/uploads/2013/10/VPN-error.png` — EXISTS; `assets/images/wp-content/uploads/2013/10/VPN-encrypt.png` — EXISTS.

**Faithful replacement for line 133** (replace `{{ … | relative_url }}` with plain path; strip the `srcset` references to the old WP URL since they reference `blog.mithis.net/wp-content/…` not the migrated asset path):

```html
<img alt="Error: Import of the VPN settings failed." class="alignnone size-full wp-image-1835" height="265" sizes="(max-width: 745px) 100vw, 745px" src="/assets/images/wp-content/uploads/2013/10/VPN-error.png" srcset="/assets/images/wp-content/uploads/2013/10/VPN-error.png 745w" width="745"/>
```

**Faithful replacement for line 135:**

```html
<img alt="Export VPN settings" class="alignnone size-full wp-image-1836" height="306" sizes="(max-width: 442px) 100vw, 442px" src="/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png" srcset="/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png 442w" width="442"/>
```

Note: The `srcset` second entry (`https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error-300x106.png`) references a WP upload URL, not a migrated asset. The 300w resized thumbnail is NOT in `assets/`. Drop the external WP URL from `srcset`; keep only the local asset reference. This is the correct faithful migration posture (the missing thumbnail sizes are a pre-existing gap, not introduced by this fix).

---

#### Post 7: `_posts/2014-07-25-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.md` — 2 edit sites (lines 21 and 23)

**Current line 21 (2× LIQUID_LEAK + 3× MISSING_IMAGE — the linter counts 2 LIQUID_LEAK and 2 MISSING_IMAGE here; plus 1 MISSING_IMAGE on line 23):**

```
<img alt="Numato HDMI2USB Prototype driving 2 screens" … src="{{ "/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg" | relative_url }}" srcset="…" width="225"/>  <img alt="HDMI2USB weird image artifact" … src="{{ "/assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg" | relative_url }}" srcset="…" width="400"/>
```

**Current line 23 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt="HDMI2USB - Rohit's VGA Capture board" … src="{{ "/assets/images/wp-content/uploads/2014/07/IMG_20140725_010725-225x300.jpg" | relative_url }}" srcset="…" width="225"/>
```

**Oracle (LIVE — `https://blog.mithis.net/archives/timvideos-us/1995-hdmi2usb-production-board-bring-up-day-4-24th-july-2014`):**

- Line 21, image 1: `<a href="…/IMG_20140725_0029322.jpg"><img … src="…/IMG_20140725_0029322-225x300.jpg" alt="Numato HDMI2USB Prototype driving 2 screens" width="225" height="300" srcset="…" /></a>`
- Line 21, image 2: `<img … src="…/IMG_20140725_003008-300x225.jpg" alt="HDMI2USB weird image artifact" width="400" height="300" srcset="…" />` (no link wrapper for this one)
- Line 23: `<a href="…/IMG_20140725_010725.jpg"><img … src="…/IMG_20140725_010725-225x300.jpg" alt="HDMI2USB - Rohit's VGA Capture board" width="225" height="300" srcset="…" /></a>`

**Asset existence:**
- `assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg` — EXISTS
- `assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg` — NOT FOUND in `assets/` (only `IMG_20140725_003008-300x225.jpg` — confirmed NOT in the listing; only `IMG_20140725_0029322-225x300.jpg` and `IMG_20140725_0029322.jpg` and `IMG_20140725_010725-225x300.jpg` and `IMG_20140725_010725.jpg` are present)
- `assets/images/wp-content/uploads/2014/07/IMG_20140725_010725-225x300.jpg` — EXISTS

Wait — re-check asset listing for `IMG_20140725_003008`:

From the `ls` run earlier: `IMG_20140725_003008-300x225.jpg` IS in the directory listing. It IS present.

All three image files exist:
- `IMG_20140725_0029322-225x300.jpg` — EXISTS
- `IMG_20140725_003008-300x225.jpg` — EXISTS
- `IMG_20140725_010725-225x300.jpg` — EXISTS
- `IMG_20140725_0029322.jpg` — EXISTS (for the linked-image href)
- `IMG_20140725_010725.jpg` — EXISTS (for the linked-image href)

**Faithful replacement for line 21** (both images on one line; keep on one line or split — preserve original line grouping):

```html
<a href="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322.jpg"><img alt="Numato HDMI2USB Prototype driving 2 screens" class="alignnone wp-image-1997 size-medium" height="300" sizes="(max-width: 225px) 100vw, 225px" src="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg" srcset="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg 225w" width="225"/></a>  <img alt="HDMI2USB weird image artifact" class="alignnone wp-image-1998" height="300" sizes="(max-width: 400px) 100vw, 400px" src="/assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg" srcset="/assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg 300w" width="400"/>
```

**Faithful replacement for line 23:**

```html
<a href="/assets/images/wp-content/uploads/2014/07/IMG_20140725_010725.jpg"><img alt="HDMI2USB - Rohit's VGA Capture board" class="aligncenter wp-image-2000 size-medium" height="300" sizes="(max-width: 225px) 100vw, 225px" src="/assets/images/wp-content/uploads/2014/07/IMG_20140725_010725-225x300.jpg" srcset="/assets/images/wp-content/uploads/2014/07/IMG_20140725_010725-225x300.jpg 225w" width="225"/></a>
```

The `srcset` WP-origin URLs (`https://blog.mithis.net/wp-content/uploads/…/IMG_…-768x1024.jpg`, `…-900x1200.jpg`) are NOT in `assets/`. Drop them from `srcset`; keep only the local asset reference. Same posture as §B-post6.

---

#### Post 8: `_posts/2015-07-05-first-v2-hdmi2usb-production-board-constructed.md` — 1 edit site (line 17)

**Current line 17 (LIQUID_LEAK + co-located MISSING_IMAGE):**

```
<img alt='HDMI2USB "Production Board" Version 2' class="wp-image-2046" height="436" sizes="(max-width: 661px) 100vw, 661px" src="{{ "/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg" | relative_url }}" srcset="/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg 1024w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-300x197.jpg 300w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-900x593.jpg 900w" width="661"/>
```

**Oracle (LIVE — `https://blog.mithis.net/archives/timvideos-us/2045-first-v2-hdmi2usb-production-board-constructed`):**

```html
<div id="attachment_2046" style="width: 671px" class="wp-caption aligncenter">
  <a href="https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2.jpg">
    <img class="wp-image-2046" src="…/HDMI2USB-Prod-V2-1024x675.jpg" alt='HDMI2USB "Production Board" Version 2' width="661" height="436" srcset="…" sizes="…"/>
  </a>
  <p class="wp-caption-text">HDMI2USB "Production Board" Version 2</p>
</div>
```

The original was wrapped in a `<div class="wp-caption aligncenter">` with a caption. The Jekyll migration dropped the `wp-caption` wrapper. The current source line 17 does NOT have the wrapper — the pre-existing migration posture is to show the image without the WP caption div. This is a pre-existing fidelity gap outside P4's scope. P4 only strips the `relative_url` Liquid.

**Asset existence:** `assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg` — EXISTS; `HDMI2USB-Prod-V2.jpg` — EXISTS (for the linked-image href).

**Faithful replacement for line 17:**

```html
<img alt='HDMI2USB "Production Board" Version 2' class="wp-image-2046" height="436" sizes="(max-width: 661px) 100vw, 661px" src="/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg" srcset="/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg 1024w" width="661"/>
```

Drop the WP-origin `srcset` URLs (`/wp-content/uploads/…-300x197.jpg`, `…-900x593.jpg`) — not in `assets/`. Keep the local asset reference only.

---

### R-P4 finding count summary

| Post | LIQUID_LEAK | MISSING_IMAGE | Edit sites |
|---|---|---|---|
| `2007-05-09-almost-there.md` | 1 (line 19) | 1 (line 19) | 1 |
| `2007-08-17-resume.md` | 1 (line 18) | 0 | 1 |
| `2008-02-04-google-patchwork.md` | 2 (lines 17, 19) | 2 (lines 17, 19) | 2 |
| `2008-02-18-cfxs-free.md` | 1 (line 27) | 1 (line 27) | 1 |
| `2009-05-26-starhunter-…-cousin.md` | 1 (line 22) | 1 (line 22) | 1 |
| `2013-10-06-connecting-to-a-fritzbox-….md` | 2 (lines 133, 135) | 2 (lines 133, 135) | 2 |
| `2014-07-25-hdmi2usb-…-day-4-….md` | 2 (lines 21, 23) | 3 (lines 21×2, 23) | 2 |
| `2015-07-05-first-v2-hdmi2usb-….md` | 1 (line 17) | 1 (line 17) | 1 |
| **TOTAL** | **11** | **11** | **11** |

End state after all edits: `uv run python -m scripts.fidelity.run` (or `uv run python tmp/p4_lint.py`) reports **0 findings**.

---

## C. feed/sitemap absolute URLs

### C.1 First-party `feed.xml` (root-level)

Located at `/home/tim/github/mithro/blog.mithis.net/.worktrees/migration-p4-domain-deploy/feed.xml`. This is a **custom feed template** (not the jekyll-feed plugin output). It already uses the correct patterns:

```liquid
<link>{{ site.url }}{{ site.baseurl }}/</link>
<atom:link href="{{ "/feed.xml" | prepend: site.baseurl | prepend: site.url }}" …/>
<link>{{ post.url | prepend: site.baseurl | prepend: site.url }}</link>
<guid>{{ post.url | prepend: site.baseurl | prepend: site.url }}</guid>
```

After `url: "https://blog.mithis.net"` + `baseurl: ""`:
- `{{ site.url }}{{ site.baseurl }}/` → `https://blog.mithis.net/` ✓
- `{{ post.url | prepend: site.baseurl | prepend: site.url }}` → `https://blog.mithis.net/archives/…` ✓

No template changes needed for `feed.xml`.

### C.2 Category feeds (`category/*/feed.xml` — 19 files)

Each uses the same correct pattern:

```liquid
<link>{{ site.url }}{{ site.baseurl }}/</link>
<atom:link href="{{ page.url | prepend: site.baseurl | prepend: site.url }}" …/>
<link>{{ post.url | prepend: site.baseurl | prepend: site.url }}</link>
<guid>{{ post.url | prepend: site.baseurl | prepend: site.url }}</guid>
```

After the config change these will emit correct absolute `https://blog.mithis.net/archives/category/<slug>/feed/` URLs. No template changes needed.

### C.3 Custom `sitemap.xml` (root-level)

Has one problematic line:

```liquid
<loc>{{ site.url }}{{ site.baseurl }}/category/{{ category | slugify }}/</loc>
```

This will emit `https://blog.mithis.net/category/<slug>/` — the OLD URL space. After M1/M2 (P2), category pages were moved to `/archives/category/<slug>/`. **This line MUST be updated in P4** to:

```liquid
<loc>{{ site.url }}{{ site.baseurl }}/archives/category/{{ category | slugify }}/</loc>
```

All other `sitemap.xml` URL patterns (`{{ page.url | prepend: … }}`, `{{ post.url | prepend: … }}`) are already correct (they use the page/post URLs which were updated by M1).

### C.4 Dead `_includes/category-feed.xml`

This file exists but has no callers (per FOLLOWUPS.md). It uses stale `/category/<slug>/` URLs internally. Per FOLLOWUPS it is dead code — no action in P4 (cleanup deferred to P5). Do NOT wire it in.

### C.5 Dead `sitemap_index.xml`

Located at root. This is a WP-era artifact (the `xml/` exclusion in `_config.yml` correctly excludes the `xml/` directory; `sitemap_index.xml` in root is a different file). Inspect: this file is a static WP-era sitemap index pointing to `blog.mithis.net/sitemap-*.xml` entries. Jekyll generates its own `sitemap.xml` via the `jekyll-sitemap` gem AND the custom `sitemap.xml` template. The `sitemap_index.xml` in root will be copied to `_site/sitemap_index.xml` and is misleading (it points to old WP sitemap fragments). **Recommendation:** add `sitemap_index.xml` to the `exclude:` list in `_config.yml` (alongside the other WP artifacts). This is a P4 task.

### C.6 Verification commands (post-build)

```bash
# After bundle3.3 exec jekyll build:

# Verify feed.xml has correct absolute URLs
grep -E '<link>|<atom:link|<guid' _site/feed/index.xml | head -5
# Expected: all start with https://blog.mithis.net/

# Verify category feed
grep -E '<link>|<atom:link|<guid' _site/archives/category/hardware/feed/index.html | head -3
# Expected: https://blog.mithis.net/archives/category/hardware/feed/

# Verify sitemap.xml
grep '<loc>' _site/sitemap.xml | grep -v 'blog.mithis.net' | head -5
# Expected: zero lines (all locs must be absolute blog.mithis.net URLs)

# Verify no /blog.mithis.net prefix leaked into built HTML
grep -r '"/blog\.mithis\.net/' _site/*.html _site/archives/ 2>&1|cat | head -5
# Expected: zero (the old baseurl must not appear anywhere in _site)
```

---

## D. Deferred URL-structure edge cases — faithful resolution + 301 redirects

### D.1 `jekyll-redirect-from` gem — MUST ADD

`jekyll-redirect-from` is NOT in the current `Gemfile` or `Gemfile.lock`. It is listed in the `CLAUDE.md` technical stack as an available gem, and it is listed in `_config.yml` comments but absent from `plugins:`.

**Action (P4-C5):**

1. Add to `Gemfile`:
   ```ruby
   gem "jekyll-redirect-from"
   ```
2. Add to `_config.yml` `plugins:` list:
   ```yaml
   plugins:
     - jekyll-feed
     - jekyll-sitemap
     - jekyll-paginate
     - jekyll-redirect-from
   ```
3. Run `bundle3.3 install` to update `Gemfile.lock`.

`jekyll-redirect-from` generates HTML redirect stubs for every `redirect_from:` front-matter entry. It is the standard GitHub Pages compatible redirect mechanism.

---

### D.2 `rcs-darcs` hierarchical URL

**Oracle facts (LIVE):**
- `https://blog.mithis.net/archives/rcs/darcs` → HTTP 200, display name "darcs", desc "Darcs is revision control system I use to use before converting to git."
- `https://blog.mithis.net/archives/category/rcs-darcs` → HTTP 404 (WP never registered this flat slug)
- The category page at `https://blog.mithis.net/archives/rcs/darcs` shows two posts: "Using Tailor to go to git" (ID 35) and "darcs almost perfect." (ID 19)
- Post `2007-02-26-darcs-almost-perfect.md` has `permalink: /archives/rcs/darcs/19-darcs-almost-perfect` (correct, WP-faithful) and `categories: [rcs-darcs]`
- Post `2007-02-25-tailor-darcs2svn-tp.md` has `categories: [tp, ...]` and `permalink: /archives/tp/16-tailor-darcs2svn-tp` — but on the live WP it shows category links `darcs` + `Thousand Parsec`. This post was filed under `tp` in Jekyll but the live oracle shows it under `rcs/darcs` too.
- Post `2007-04-21-using-tailor-to-go-to-git.md` (`wordpress_category: tp`) shows HTTP 500 on live, but the `rcs/darcs` category page lists ID 35 = "Using Tailor to go to git" (which is P3's recovered post at `tp/35-using-tailor-to-go-to-git`) — this is a *missing* post (ID 35 was one of P3's 4, already snapshotted)

**The M1/M2 state:** `category/rcs-darcs.md` has `permalink: /archives/category/rcs-darcs/` and `title: darcs`. This is the Jekyll-side category page. The category page at `/archives/rcs/darcs` is the WP-faithful URL.

**Faithful resolution (recommended):**

Change `category/rcs-darcs.md` permalink from `/archives/category/rcs-darcs/` to `/archives/rcs/darcs/`. This makes the Jekyll category page serve at the WP-faithful URL. Add a `redirect_from: [/archives/category/rcs-darcs/]` to handle any links that use the flat slug URL.

```yaml
# category/rcs-darcs.md front matter
layout: category
title: darcs
cat_slug: rcs-darcs
permalink: /archives/rcs/darcs/
description: 'Darcs is revision control system I use to use before converting to git.'
redirect_from:
  - /archives/category/rcs-darcs/
```

Also update `category/rcs-darcs/feed.xml` permalink from `/archives/category/rcs-darcs/feed/` to `/archives/rcs/darcs/feed/`.

Sidebar entry for `rcs-darcs` in `_includes/sidebar.html` currently reads `>RCS (3)</option>` — the faithful label is "RCS" (the parent category label shown in WP sidebar). No label change needed; the URL `option value` should be updated to `/archives/rcs/darcs/` (to match the new permalink).

**Note on tailor-darcs2svn (ID 16):** The live oracle shows `categories: [darcs, Thousand Parsec]` for this post. The current Jekyll post (`2007-02-25-tailor-darcs2svn-tp.md`) has `categories: [tp]` only. To be fully faithful, add `rcs-darcs` to its `categories:` array so it appears on the darcs category page. Similarly for `2007-04-21-using-tailor-to-go-to-git.md` if that is recovered in P3 (ID 35 — already captured in `exports/p3-missing-raw/35.html`).

---

### D.3 `timvideos-us/hdmi2usb` sub-category

**Oracle facts (LIVE):**
- `https://blog.mithis.net/archives/category/timvideos-us/hdmi2usb` → HTTP 200, display "HDMI2USB", desc "HDMI2USB is a device to capture HDMI and DVI (and Displayport with cheap active adapters) and send it on USB port as UVC video. The device attaches computer as a standard webcam so there is no need of installing additional drivers."
- All 8 hdmi2usb posts show `HDMI2USB` category on the live site (confirmed oracle, all HTTP 200):
  - `2014-07-21-hdmi2usb…-snippets-prep-work.md` (WP ID 1980) — cats: HDMI2USB, TimVideos.us
  - `2014-07-22-hdmi2usb…-day-1-….md` (WP ID 1985) — cats: HDMI2USB, TimVideos.us
  - `2014-07-23-hdmi2usb…-day-2-….md` (WP ID 1988) — cats: HDMI2USB, TimVideos.us
  - `2014-07-24-hdmi2usb…-day-3-….md` (WP ID 1993) — cats: HDMI2USB, TimVideos.us
  - `2014-07-25-hdmi2usb…-day-4-….md` (WP ID 1995) — cats: HDMI2USB, TimVideos.us
  - `2014-07-28-hdmi2usb…-day-5-6-7-….md` (WP ID 2003) — cats: HDMI2USB, TimVideos.us
  - `2014-07-29-hdmi2usb…-day-8-….md` (WP ID 2009) — cats: HDMI2USB, TimVideos.us
  - `2015-07-05-first-v2-hdmi2usb-….md` (WP ID 2045) — cats: Hardware, HDMI2USB, TimVideos.us

All 8 hdmi2usb posts currently have `categories: [timvideos-us]` only in Jekyll (missing `hdmi2usb`).

**Faithful resolution:**

1. Create `category/timvideos-us/hdmi2usb.md` (note: must be in a `timvideos-us/` subdirectory to match the URL hierarchy `/archives/category/timvideos-us/hdmi2usb/`):

   ```yaml
   ---
   layout: category
   title: HDMI2USB
   cat_slug: hdmi2usb
   permalink: /archives/category/timvideos-us/hdmi2usb/
   description: 'HDMI2USB is a device to capture HDMI and DVI (and Displayport with cheap active adapters) and send it on USB port as UVC video. The device attaches computer as a standard webcam so there is no need of installing additional drivers.'
   ---
   ```

   Note: the `_layouts/category.html` uses `page.cat_slug` to filter posts (`site.posts | where_exp: "post", "post.categories contains page.cat_slug"`). The `cat_slug` must match the value in post `categories:` arrays. Use `cat_slug: hdmi2usb` (the value to add to post front matter).

   Also create `category/timvideos-us/hdmi2usb/feed.xml` matching the pattern of other category feeds with `permalink: /archives/category/timvideos-us/hdmi2usb/feed/`.

2. Add `hdmi2usb` to `categories:` in all 8 hdmi2usb posts' front matter:

   ```yaml
   categories:
   - timvideos-us
   - hdmi2usb
   ```

   For `2015-07-05-first-v2-hdmi2usb-….md`: add both `hardware` and `hdmi2usb` (oracle shows `Hardware, HDMI2USB, TimVideos.us`):

   ```yaml
   categories:
   - timvideos-us
   - hdmi2usb
   - hardware
   ```

3. Also add `category/timvideos-us/hdmi2usb/` to the sidebar dropdown in `_includes/sidebar.html` at an appropriate position (after `timvideos-us`) with display text "HDMI2USB".

---

### D.4 Scheme/Sydney/Tailor categories

**Oracle facts (LIVE):**

- **Scheme** (`https://blog.mithis.net/archives/category/scheme`): HTTP 200, display "Scheme", desc "(empty)". Post "Skimpy, Scheme in Python" (WP ID 45, `2007-07-23-schemepy.md`) shows live oracle categories `Python, Scheme, Thousand Parsec`. Current Jekyll `categories: [tp]` only.
- **Sydney** (`https://blog.mithis.net/archives/category/sydney`): HTTP 200, display "Sydney", desc "(empty)". Post "Packing your bags…" (WP ID 79, `2008-04-27-going-to-sydney.md`) shows HTTP 500 on live. Oracle unreachable for this post. Current Jekyll `categories: [google]`. The FOLLOWUPS §6 says "google for sydney…were collapsed during migration". Based on the live category page existing + the oracle confirming the category was "Sydney", `2008-04-27-going-to-sydney.md` should have `categories: [google, sydney]`. **However**, since the post itself is HTTP 500 on live and we cannot confirm all categories oracle-side — this is a best-evidence recommendation, not oracle-confirmed.
- **Tailor** (`https://blog.mithis.net/archives/rcs/tailor`): HTTP 200, display "Tailor", desc "A cool tool for converting from one SCM tool to another." Post "Using Tailor to go to git" (WP ID 35) is a P3-recovered post (already captured in `exports/p3-missing-raw/35.html`). Live oracle shows WP post 35 at this path; permalink in the currently committed `2007-04-21-using-tailor-to-go-to-git.md` is `/archives/tp/35-using-tailor-to-go-to-git` (oracle-confirmed category: `tp`). The tailor category page at `/archives/rcs/tailor` exists but has HTTP 500 for the listed post in P3. Note: `tailor` is at `/archives/rcs/tailor` (hierarchical, under RCS parent like darcs).

**Faithful resolution:**

**Scheme:** Create `category/scheme.md`:

```yaml
---
layout: category
title: Scheme
cat_slug: scheme
permalink: /archives/category/scheme/
description: ""
---
```

Create `category/scheme/feed.xml` following the feed pattern.

Add `scheme` to `_posts/2007-07-23-schemepy.md` categories:

```yaml
categories:
- tp
- scheme
- python
```

(Oracle: `Python, Scheme, Thousand Parsec` → slugs `python, scheme, tp`.)

Add sidebar entry for `scheme` in `_includes/sidebar.html`.

**Sydney:** Create `category/sydney.md`:

```yaml
---
layout: category
title: Sydney
cat_slug: sydney
permalink: /archives/category/sydney/
description: ""
---
```

Add sidebar entry. Add `sydney` to `_posts/2008-04-27-going-to-sydney.md` categories (best-evidence: oracle category page exists at `/archives/category/sydney` listing this post; description empty). Flag: **ORACLE-UNREACHABLE for the post itself** (HTTP 500). Best-evidence recommendation: add `sydney` to `categories: [google, sydney]`.

**Tailor:** The live category is at `/archives/rcs/tailor` (hierarchical under RCS). Create:

```yaml
# category/rcs-tailor.md (slug: rcs-tailor, but WP URL uses rcs/tailor hierarchy)
---
layout: category
title: Tailor
cat_slug: tailor
permalink: /archives/rcs/tailor/
description: 'A cool tool for converting from one SCM tool to another.'
redirect_from:
  - /archives/category/tailor/
---
```

The `cat_slug: tailor` is used to filter posts. The post currently linked (ID 35, "Using Tailor to go to git") needs `tailor` in its `categories:`. That post's current Jekyll file (`2007-04-21-using-tailor-to-go-to-git.md`) has `categories: [tp]`. Add `tailor` (and `rcs-darcs` per §D.2): `categories: [tp, rcs-darcs, tailor]`. This is consistent with the WP live oracle which showed ID 16 (`tailor-darcs2svn-tp`) with `categories: [darcs, tp]` and the rcs/darcs category page listing ID 35.

Also add `category/rcs-tailor/feed.xml` (or `category/tailor/feed.xml` at `/archives/rcs/tailor/feed/`).

**USER-DECISION for Sydney:** The live post for "going-to-sydney" is HTTP 500 and cannot be oracle-confirmed. The recommendation above (add `sydney` to categories) is best-evidence based on the live WP category page listing this post. If the user wants to verify before touching the post, the committed `2008-04-27-going-to-sydney.md` file is the place to check content. Implementer should add a note to verify once the live WP server can serve ID 79.

---

### D.5 404/search form-action

**Current state:**

`404.html` line 14:
```liquid
<form id="error404-searchform" method="get" action="{{ site.url }}">
```

After `url: "https://blog.mithis.net"`, this renders `action="https://blog.mithis.net"` — a GET to the homepage root with `?s=…`. The Barthelme `404.php` posted `?s=` to WP home (WP handles `?s=` server-side). On a static Jekyll site, GET `/?s=foo` does nothing (no server-side search).

**Faithful-vs-functional decision (per FOLLOWUPS §P4/P5/P6 from P1-T7):** Point the 404 form at the working client-side `/search.html?s=…` so it actually works. This is the same decision as the sidebar search widget (which already uses `action="{{ '/search.html' | relative_url }}"` per search.html).

**Exact fix (line 14 of `404.html`):**

```liquid
<form id="error404-searchform" method="get" action="{{ '/search.html' | relative_url }}">
```

After `baseurl: ""`, this renders `action="/search.html"`, which routes to the working client-side search page.

**Sidebar search:** Per FOLLOWUPS (P2/P5), `_includes/sidebar.html` has dead `search-input`/`search-results` IDs with no form. The FOLLOWUPS item says convert to a real form. If not already done in P2, add to P4 scope:

```liquid
<form method="get" action="{{ '/search.html' | relative_url }}">
  <input name="s" id="sidebar-s" type="text" placeholder="Search…"/>
  <input type="submit" value="Search"/>
</form>
```

Verify in `_includes/sidebar.html` whether this was already addressed; if not, include it in P4-C4.

---

### D.6 Complete changed-URL spaces needing 301 redirects

All redirects use `jekyll-redirect-from` `redirect_from:` front matter (see §D.1 for gem setup).

| From (old URL) | To (new URL) | Location in source | Mechanism |
|---|---|---|---|
| `/category/<slug>/` (19 slugs, all) | `/archives/category/<slug>/` | Each `category/<slug>.md` (already has correct permalink from M1) — add `redirect_from: [/category/<slug>/]` | `jekyll-redirect-from` |
| `/category/<slug>/feed/` (19 slugs) | `/archives/category/<slug>/feed/` | Each `category/<slug>/feed.xml` — add `redirect_from: [/category/<slug>/feed/]` | `jekyll-redirect-from` |
| `/archives/category/rcs-darcs/` | `/archives/rcs/darcs/` | `category/rcs-darcs.md` (permalink change) + `redirect_from` | `jekyll-redirect-from` |
| `/archives/rcs/darcs/` | _(already the new permalink)_ | `category/rcs-darcs.md` has this as permalink | N/A |

**Notes:**
- The `mithro.github.io/blog.mithis.net/…` → `blog.mithis.net/…` redirect is handled by GitHub Pages automatically when a custom domain is configured (GitHub serves a 301 from the `github.io` URL to the custom domain). No extra configuration needed.
- The `/archives/category/rcs-darcs/` → `/archives/rcs/darcs/` redirect is the most important faithful redirect (the old M1 permalink was wrong; the faithful WP URL is `/archives/rcs/darcs/`).
- The `/category/<slug>/` → `/archives/category/<slug>/` redirect is the full M1 changed-URL space. All 19 `category/<slug>.md` files need `redirect_from: [/category/<slug>/]` added, and all 19 `category/<slug>/feed.xml` files need `redirect_from: [/category/<slug>/feed/]`.

**Practical approach:** For the 19 `/category/<slug>/` redirects, add a `redirect_from:` key to each `category/<slug>.md` front matter (one YAML key, one entry):

```yaml
redirect_from:
  - /category/hardware/
```

And each `category/<slug>/feed.xml`:

```yaml
redirect_from:
  - /category/hardware/feed/
```

---

## E. DNS records for the user

`blog.mithis.net` is a **subdomain** (not an apex/root domain). GitHub Pages custom-domain DNS for a subdomain = **CNAME DNS record** (NOT A/AAAA records, which are only for apex domains).

**Exact DNS record to create:**

| Type | Name (host) | Value (target) | TTL |
|---|---|---|---|
| `CNAME` | `blog` | `mithro.github.io.` | 3600 (or lowest your registrar allows, e.g. 300 for fast propagation) |

**Reading:**
- Type: `CNAME`
- Name/Host: `blog` (relative to your domain `mithis.net`, so it resolves as `blog.mithis.net`)
- Value/Target: `mithro.github.io` (your GitHub Pages host — note: no trailing dot needed in most registrar UIs, but technically the full qualified name is `mithro.github.io.`)
- TTL: 3600 seconds (1 hour) is standard; use 300 during cutover for faster propagation

**GitHub repo Pages settings steps (user performs):**

1. In the repo settings → Pages, set "Custom domain" to `blog.mithis.net` and click Save.
2. GitHub will verify the DNS record. Once verified, enable "Enforce HTTPS" (requires the CNAME DNS record to be propagated and GitHub's TLS cert to be issued — usually within minutes to a few hours).
3. The `CNAME` file in the repo root (`blog.mithis.net`) confirms the custom domain to GitHub Pages on every deploy.

**Apex consideration:** `mithis.net` itself is NOT being configured here — only the `blog` subdomain. No A/AAAA records are needed for the `mithis.net` apex. No `www.blog.mithis.net` record is needed unless you want it (not standard for a blog subdomain setup).

**After propagation:** `https://blog.mithis.net` will serve the Jekyll site. The old `https://mithro.github.io/blog.mithis.net/` URL will redirect to `https://blog.mithis.net/` (GitHub Pages handles this automatically).

---

## F. Gates & sequencing

### Strict task sequencing

```
P4-C1: _config.yml + CNAME + workflow (ATOMIC — must be one commit)
  Gate: bundle3.3 exec jekyll build exits 0; no /blog.mithis.net prefix in _site

P4-C2a..h: 8 posts × R-P4 LIQUID_LEAK conversion (one commit per post)
  Gate per post: uv run python tmp/p4_lint.py shows N-2 findings (N decreasing by 2 per post)
  Final gate: 0 findings

P4-C3: sitemap.xml categories URL fix; sitemap_index.xml exclusion
  Gate: grep '<loc>' _site/sitemap.xml shows no /category/ paths; all absolute blog.mithis.net

P4-C4: Edge cases — 404 form, rcs-darcs permalink, timvideos-us/hdmi2usb, Scheme/Sydney/Tailor, redirect_from additions
  Gate: bundle3.3 exec jekyll build clean; structure_check 6/6

P4-C5: Gemfile + jekyll-redirect-from
  Gate: bundle3.3 install succeeds; bundle3.3 exec jekyll build emits redirect stubs for /category/ → /archives/category/

P4-Z: P4 exit gate (see below)
```

### P4 EXIT GATE (all must hold before merging)

1. **Content linter: 0 findings** — `uv run python tmp/p4_lint.py` (or `uv run python -m scripts.fidelity.run`) reports 0 findings across all `_posts/*.md`
2. **structure_check 6/6** — `uv run python -m scripts.fidelity.run` reports all 6 archetypes pass
3. **`bundle3.3 exec jekyll build` clean** — zero errors, zero warnings
4. **feed.xml/sitemap.xml emit absolute `https://blog.mithis.net/…`** — verified by grep (see §C.6)
5. **Every post's WP permalink resolves in `_site`** — all 72+ posts have their `permalink:` path as a built file in `_site/archives/…`
6. **No visual/content fidelity regression vs oracle** — spot-check: `almost-there` linked thumbnail renders, `google-patchwork` map images render, `fritzbox` VPN-error + VPN-encrypt images render, `first-v2-hdmi2usb` board photo renders
7. **Redirects in place** — `_site/category/hardware/index.html` exists and contains a redirect to `/archives/category/hardware/`
8. **`_config.yml`/CNAME/workflow exactly per §A** — verify via `git show HEAD:_config.yml` after P4-C1
9. **pytest 45 green** — `uv run python -m pytest tests/ -q` passes all 45 tests

### Harness note

With `baseurl: ""`, the local serve/render URLs now resolve at `http://localhost:4000/` (not `/blog.mithis.net/`). The Playwright/visual render layer becomes viable after P4 — per FOLLOWUPS, the `FIDELITY_SKIP_RENDER=1` flag can be removed and `capture_all("http://localhost:4000")` will correctly capture all archetypes. This is a P6 activation (P4 does not run the Playwright visual layer). `structure_check` checks `_site` archetype paths and is fully baseurl-independent — it continues to work correctly throughout P4.

---

## G. Blockers and user decisions

### Blockers (none hard — all have best-evidence paths)

- `jekyll-redirect-from` not in Gemfile: addressable in P4-C5 (add gem).
- Starhunter post is HTTP 500 (oracle-unreachable for content): not a blocker for R-P4 conversion — the Liquid-to-plain-path edit is unambiguous regardless of oracle content. The stray `height`/`width`/`title` attributes require a minimal inline `<img>` which is spec-allowed.
- Sydney post ("going-to-sydney") is HTTP 500: see USER-DECISION below.

### USER-DECISION items

1. **Sydney post categories:** `2008-04-27-going-to-sydney.md` currently has `categories: [google]`. The live WP category page `/archives/category/sydney` lists this post. Best-evidence: add `sydney` to `categories: [google, sydney]`. However, the post itself is HTTP 500 on live — cannot oracle-confirm all categories. **User decision: confirm `sydney` should be added to this post's categories, or defer until the live WP server serves ID 79.**

2. **Tailor post categories (ID 35 = P3 post):** `2007-04-21-using-tailor-to-go-to-git.md` has `categories: [tp]`. The `/archives/rcs/tailor` category page lists this post; also `/archives/rcs/darcs` lists it. Best-evidence: add `rcs-darcs` and `tailor` to its `categories:`. However, this post's WP oracle is HTTP 500 (same P3 issue). The committed post content (snapshotted in P3) can be verified against the P3 raw snapshot at `exports/p3-missing-raw/35.html` — implementer should check that file's `cat-links` to confirm. **Implementer action: check `exports/p3-missing-raw/35.html` for category links before modifying the post.**

3. **`tailor-darcs2svn-tp.md` (ID 16):** Currently `categories: [tp]`. Live oracle shows `darcs + Thousand Parsec` categories. To restore `darcs` (= `rcs-darcs` slug) faithfully, add `rcs-darcs` to `categories: [tp, rcs-darcs]`. This is oracle-confirmed (HTTP 200 on live). Implementer can act on this without user decision.

---

## Appendix: Tmp script inventory (retained for implementer)

All scripts in `tmp/` are retained (gitignored):
- `tmp/p4_lint.py` — linter runner; re-run post-conversion to verify 0 findings
- `tmp/p4_oracle{2..10}.py` — oracle fetch scripts; re-run any if additional verification needed
