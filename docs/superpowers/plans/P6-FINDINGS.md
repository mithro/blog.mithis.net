# P6-FINDINGS — Triage: Autonomous-Doable vs USER-DECISION vs Deferred

**Phase:** P6 Final Acceptance (pixel-level visual fidelity signoff)
**Triage date:** 2026-05-20
**Branch:** `migration-p6-final-signoff`
**Worktree head:** `5aa4109` (PSL results + 6 PSL FOLLOWUPS)
**Design acceptance bar:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md` §11, item #3 (user final visual signoff after structural+Playwright and Wayback pixel pass)

---

## §A — Sources Inventoried

1. `docs/superpowers/plans/FOLLOWUPS.md` (654 lines) — canonical living follow-ups list; all cross-phase items accumulated P0→PSL.
2. `docs/superpowers/plans/PSL-RESULTS.md` §4 — "Handoff — P6 next" section: curated WP-artifact inline-HTML candidates list + remaining verification items.
3. `docs/superpowers/plans/P5-RESULTS.md` §4 — Handoff notes; P5 polish bundle (5 Minors); Wayback pixel sweep + user signoff as outstanding.
4. `FOLLOWUPS.md` §"PSL polish" (lines 630–654) — 6 PSL cosmetic non-blockers added in commit `5aa4109`.
5. `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md` §10–§11 — acceptance bar: all three methods (structural+Playwright, Wayback pixel, user signoff) must hold; plus objective gates (green build, 76/76 posts, linter 0, custom-domain correct, hardcoded-HTML guard active).
6. `pyproject.toml` + `.gitignore` — `uv.lock` is gitignored (verified). Lock file present in worktree pins `greenlet==3.5.0` (the version that has Linux x86_64 wheels). The task description notes that a future worktree's `uv` re-resolution could pick `greenlet 3.5.1` if it has no Linux wheels — pin `tool.uv.required-environments` in `pyproject.toml` to prevent this.

---

## §B — Queue A: Autonomous-Doable in P6-EXEC-auto

Items that can be completed without user input. Each has a bounded scope and a concrete acceptance gate. Ordered low-risk-first.

---

### A-1: P5 polish bundle — 5 Minors from P5-EXEC code review
**Scope:** Four source files; zero render impact.

1. `scripts/fidelity/lint_content.py` line 42 comment: reword to `# \b removed — sentinel values are controlled; no corpus text matches BLOCK_HTML_* variants`.
2. `tests/test_new_post.py` lines 10–18: delete dead `run_new_post()` helper (never called; all 5 tests use `subprocess.run` via `post_env` fixture).
3. `docs/AUTHORING.md` §8: reword lead-in to resolve self-contradiction (says "MUST create BOTH forms" but P5-D made include list-fallback-robust). New wording: "If a post will have comments, create the aggregate `<id>-<slug>.yml`. The per-comment directory form is optional (the include handles both)."
4. `scripts/new_post.py` `--slug`: add input guard — reject or auto-normalize spaces/uppercase via `re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-")`; add test asserting the behavior.
5. `.github/workflows/jekyll.yml` lint step: add inline note that `uv` is pre-installed on ubuntu-latest since 2024, with a `pip install uv` fallback comment for future runner-image changes.

**Acceptance gate:** `uv run python -m pytest tests/ -q` stays green (54+ passed); linter 0; build clean.
**Complexity:** S

---

### A-2: PSL polish items 1–2 and 5 — trailing whitespace + hr linter gap
**Scope:** Post source files + `lint_content.py`.

1. **Trailing whitespace** (PSL polish item 1): strip trailing whitespace from 10 lines across 6 posts — `2007-03-01-graphical-programming.md` lines 16,18,20,22,24; `2007-03-24-liferea-bug.md` line 16; `2008-03-18-gsoc2008.md` line 19; `2008-04-27-going-to-sydney.md` line 24; `2008-11-15-in-the-land-of-the-sheep.md` line 21; `2016-03-15-timvideos-us-and-google-summer-of-code-2016.md` line 21. One mechanical commit. No linter impact.

2. **`<hr>` / `<hr/>` linter coverage** (PSL polish item 5): add `r"<hr\s*/?>"` to `_BLOCK_HTML` in `lint_content.py`. Then the surviving `<hr/>` in `_posts/2016-01-15-timvideos-us-2016-new-years-resolutions.md` line 22 will be flagged. Resolution: replace `<hr/>` with `---` (Markdown thematic break) OR add a `<!-- fidelity-allow: BLOCK_HTML -->` sentinel. The `<hr/>` is inside a `>` blockquote-prefixed line; verify kramdown renders `> ---` as a thematic break before committing the `---` form (if not, use the sentinel).

3. **PSL polish item 2 — NBSP in `hdmi2usb-day-8` line 20** (`Was\xc2\xa0able to view`): verify against the live oracle first (`curl -sk https://blog.mithis.net/archives/timvideos-us/2019-hdmi2usb-production-board-bring-up-day-8` — TLS expired, use `-sk`). If the oracle has a regular space, replace U+00A0 with ASCII space. If the oracle also has NBSP (intentional line-break suppression), add a comment and leave it. Commit result either way.

**Acceptance gate:** linter 0; `uv run python -m pytest tests/ -q` green; `bundle3.3 exec jekyll build` clean.
**Complexity:** S

---

### A-3: uv platform pinning for Linux x86_64
**Scope:** `pyproject.toml` only.

Add:
```toml
[tool.uv]
required-environments = ["sys_platform == 'linux' and platform_machine == 'x86_64'"]
```

This pins future `uv` lock resolution to Linux x86_64 wheel availability, preventing a new worktree from picking a `greenlet` release that lacks pre-built Linux wheels and failing with a build-from-source or missing-wheel error. The current `uv.lock` (gitignored) has `greenlet==3.5.0` which has Linux wheels; this setting ensures future re-resolutions stay bounded.

**Acceptance gate:** `uv run python -m pytest tests/ -q` green; `uv sync` in a clean venv produces no wheel-build warning for greenlet.
**Complexity:** S

---

### A-4: R-E region-3 fence cosmetic (fritzbox source nit)
**Scope:** One blank line addition in `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`.

The region-3 closing fence (the `IPSec gateway …` vpnc.conf template, ending at line ~95) is immediately followed by the `As this file contains usernames…` paragraph with no blank line. Region-4's closing fence has one blank line before its following heading. CommonMark/kramdown require neither; rendered output is byte-correct vs oracle. This is pure source-style uniformity — add one blank line after the region-3 closing fence.

**Acceptance gate:** `bundle3.3 exec jekyll build` clean; rendered HTML byte-identical to pre-change (spot-check the paragraph immediately following the fence in `_site/`).
**Complexity:** S

---

### A-5: Wayback pixel-sample sweep proof (verification — not a fix)
**Scope:** New committed document `docs/superpowers/plans/P6-WAYBACK-SAMPLE.md`.

This is a VERIFICATION item, not a code change. The EXEC agent should:
1. Select ~10 representative posts spanning all archetypes: at minimum one post from each of home/post/category/page/404/search + 3–4 content posts with varying structure (a plain post, a list-heavy post, a post with images, a post with comments).
2. For each, fetch the Wayback snapshot: `https://web.archive.org/web/2*/blog.mithis.net<permalink>` — pick the most recent pre-2026 capture.
3. Perform a structural HTML comparison: count `<p>`, `<ul>`, `<li>`, `<h2>`, `<blockquote>` in the Wayback snapshot vs the built `_site/` equivalent. Note any delta.
4. Where Playwright/browser is available: take screenshots of both the built site and the Wayback snapshot (or Wayback's archived HTML rendered in browser) and compare visually. Where not available: the structural comparison is the fallback.
5. Produce a per-post table in `P6-WAYBACK-SAMPLE.md`: `slug | oracle-source | wayback-URL | struct-delta | visual-status | PASS/FAIL`.

**Note:** The Wayback sweep must normalize feed `pubDate`/`lastBuildDate` (which vary per build; see FOLLOWUPS M1) to avoid spurious feed deltas. The sweep covers HTML pages only, not feeds.

**Acceptance gate:** `P6-WAYBACK-SAMPLE.md` committed with all sampled posts showing PASS or a documented/accepted delta; any FAIL items added to Queue B for user decision.
**Complexity:** M

---

### A-6: CSS micro-deltas verification
**Scope:** Read-only comparison + committed note.

Compare `assets/css/main.css` (the built CSS) against `theme_analysis/barthelme/style.css` and `theme_analysis/barthelme/print.css`. Document any divergences. Key known item from FOLLOWUPS: `_layouts/page.html` title class was corrected from `page-title` to `entry-title` (P1-T6); the net effect on margin is neutral (`div#content .entry-title` overrides base margin). The P6 pixel sweep must confirm the page archetype's title margin renders identically to the original (no vertical-rhythm shift visible).

Also verify: `div#nav-below`/`div.navigation` float-children clearfix behavior. FOLLOWUPS notes the theme CSS has no clearfix — this is faithful to Barthelme's own CSS. The pixel sweep must confirm it matches the original (do NOT add a non-Barthelme clearfix unless the original visibly differs from the built rendering).

Produce a brief `## CSS audit` section appended to `P6-WAYBACK-SAMPLE.md` (or a separate `P6-CSS-AUDIT.md` if the content warrants it) listing each delta and its disposition.

**Acceptance gate:** Audit committed with PASS/FAIL or "faithful-divergence" disposition for each delta found.
**Complexity:** M

---

### A-7: Functional category sweep verification
**Scope:** Read-only verification + note. No code changes expected.

FOLLOWUPS §"P1/P6 — structure_check gate-coverage" notes that `structure_check` checks one representative per archetype and did NOT catch multi-word category pages rendering "No posts found" (fixed in P1-T5). P6 final acceptance MUST include a functional sweep: every one of the 22+1 category pages lists its posts; no page contains "No posts found" or empty content.

EXEC agent action: after `bundle3.3 exec jekyll build`, scan `_site/category/*/index.html` for the string "No posts found" or an empty `<div class="archive-meta">` with no following posts. Report results. If all pass, note as verified in `P6-WAYBACK-SAMPLE.md` or a dedicated entry.

**Acceptance gate:** Zero category pages containing "No posts found" in `_site/`; documented.
**Complexity:** S

---

### A-8: P3 pre-existing comment-data fidelity spot-check (3 posts)
**Scope:** Read-only verification against oracle. No post files modified (unless a discrepancy is found; then add to Queue B).

FOLLOWUPS §"P6 — verify pre-existing comment-data fidelity" notes that only the 4 P3-recovered posts' comment data was oracle-verified verbatim in P3. The 6 pre-existing comment posts' comment DATA fidelity was out of P3 scope. Key concern: `82-techtalk-gamingforfreedom` comment 7236 renders its author "name" as a blog-post title — this is almost certainly a WordPress pingback/trackback (faithful behavior).

Action: For 3 of the 6 pre-existing comment posts (prioritize `82-techtalk-gamingforfreedom` as the anomalous case), fetch the Wayback snapshot and compare stored `name`/`message` fields against the rendered comment in the Wayback HTML. Report discrepancies. If the pingback/trackback rendering is confirmed faithful, note it and close.

**Acceptance gate:** Spot-check result committed to `P6-WAYBACK-SAMPLE.md`. Any found-discrepancies escalated to Queue B or a new commit if trivially fixable.
**Complexity:** S

---

### A-9: Picasa header byte-fidelity confirmation
**Scope:** Read-only comparison against oracle.

FOLLOWUPS §"P1 phantom-ignore justification" (Picasa header note) confirms `_includes/header.html` contains the Picasa photo-gallery strip unchanged from its creation commit (`8d0ada8`); the decision is "replicate the Picasa strip EXACTLY (literal fidelity) for now." The P6 pixel sweep must confirm the built header HTML is byte-identical to the Barthelme original's Picasa strip markup. If Wayback captures pre-date the broken thumbnail state, compare vs those.

Action: fetch a Wayback snapshot of `blog.mithis.net` (homepage, pre-2026); extract the Picasa gallery `div` from the rendered HTML; compare against `_includes/header.html`. Note whether lh3.ggpht.com thumbnails are broken in both the oracle and the built rendering (if so, the broken state is faithful — no action needed).

**Acceptance gate:** Comparison result noted in `P6-WAYBACK-SAMPLE.md` with a "byte-faithful" or "documented-divergence" conclusion.
**Complexity:** S

---

## §C — Queue B: USER-DECISION (visual signoff items)

These items require an explicit choice: **restore** (add minimal inline HTML with `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->` sentinel per design §7) OR **accept divergence** (document and ship current Markdown rendering). Neither option is automatically applied; the user decides per item.

---

### B-1: `fritzbox-vpnc` — final section wrapped in `<blockquote>` (oracle)
- **Affected post:** `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`
- **WP artifact:** The live oracle wraps the final major section ("Fritz!Box encrypted VPN configuration files" heading + following paragraphs + images) in a `<blockquote>` element. The oracle structure is `<blockquote><h2>Fritz!Box encrypted VPN…</h2><p>…</p><p><img …/></p>…</blockquote>`.
- **Oracle source URL:** `https://blog.mithis.net/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc` (TLS expired; use `-sk`)
- **Current built rendering:** `## Fritz!Box encrypted VPN configuration files` renders as a standalone heading (not inside a blockquote). The paragraphs and images follow as regular content. Structurally DIVERGES from oracle.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <blockquote>

  ## Fritz!Box encrypted VPN configuration files

  … (all content through end of post)

  </blockquote>
  ```
- **Accept-divergence option:** The final section renders as a normal heading + body section (not visually indented/blockquoted). The difference is visible (blockquote typically adds left-indent + border).
- **Recommended:** restore (the blockquote is a significant visual element; the original blog used it to visually set apart this explanatory section)

---

### B-2: `fritzbox-vpnc` — `<pre><strong>` bold emphasis in code blocks
- **Affected post:** `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`
- **WP artifact:** Three of the four `<pre>` code blocks in the live oracle embed `<strong>` for bold emphasis on key lines: pre-1 bolds `iphone = 1;` and `xauth_key = "xxxxx";`; pre-2 bolds `key_id` and the `use_xauth = yes; xauth { … }` block; pre-3 bolds all 5 replace-me placeholders (`ip address or DNS name…`, `[username entered…]`, `[shared secret key…]`, `[username…]`, `[password…]`). pre-4 (the shell script) has no bold.
- **Oracle source URL:** `https://blog.mithis.net/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc`
- **Current built rendering:** Four fenced ```` ``` ```` code blocks with plain text (bold stripped to inner text). No emphasis. The P2-R-E decision chose plain text as the closest faithful no-HTML representation — kramdown CANNOT put `<strong>` inside `<pre><code>`.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <pre>…
  <strong>iphone = 1;</strong>
  …</pre>
  ```
  (One per affected code block; replaces the fenced block with raw `<pre><strong>` HTML — violates "no hardcoded HTML in posts" rule but is §7-sanctioned with the sentinel.)
- **Accept-divergence option:** Ship the 4 plain fenced code blocks. The "replace-me" placeholders in pre-3 are still readable; they just aren't bold. Readers lose the visual guidance to the key lines.
- **Recommended:** either (genuinely difficult tradeoff: bold is useful, but raw `<pre>` HTML is the most invasive BLOCK_HTML type; the linter finding is harder to suppress cleanly for multi-line `<pre>` than for a single `<blockquote>`)

---

### B-3: `hdmi2usb-day-3` — post-PRE orphan `<ul><ul>` (Markdown-inexpressible structure)
- **Affected post:** `_posts/2014-07-24-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014.md`
- **WP artifact:** The oracle has a nested `<ul>` immediately after a `<pre>` block, without an enclosing `<li>`. The structure is `<pre>…</pre><ul><ul><li>…</li></ul></ul>`. Markdown cannot express a `<ul>` without an enclosing `<li>`; any attempt produces a single-level list (the two separate `<ul>` blocks also merge into one in the built rendering).
- **Oracle source URL:** `https://blog.mithis.net/archives/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014`
- **Current built rendering:** Lists after the `<pre>` section render as a flat single-level `<ul>` (no nested orphan structure). Structurally diverges from oracle; the content text is preserved.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <ul><ul>
  <li>…</li>
  </ul></ul>
  ```
  (After the `<pre>` block, replace the Markdown list with raw `<ul><ul>` HTML.)
- **Accept-divergence option:** Flat list renders readably; the nested-without-li structure is a WP artifact that arguably never rendered correctly in all browsers. Visual impact is mild (one indentation level missing).
- **Recommended:** accept (the orphan `<ul><ul>` is a WP quirk; flat list is semantically equivalent and more correct HTML)

---

### B-4: `hdmi2usb-day-4` — `<blockquote>`-wrapped images + `&nbsp;` spacer
- **Affected post:** `_posts/2014-07-25-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.md`
- **WP artifact:** Oracle has images wrapped in `<blockquote><p style="text-align: center">…</p></blockquote>` AND a `<p>&nbsp;</p>` spacer paragraph. The PSL phase accepted these as WP artifacts with ±1 P-count tolerance.
- **Oracle source URL:** `https://blog.mithis.net/archives/timvideos-us/1982-hdmi2usb-production-board-bring-up-day-4-24th-july-2014`
- **Current built rendering:** Images render as plain Markdown `![alt](src)` (no blockquote wrapper, no center alignment, no spacer). The spacer paragraph is absent.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <blockquote><p style="text-align: center"><img alt="…" src="…"/></p></blockquote>
  <p>&nbsp;</p>
  ```
- **Accept-divergence option:** Images display inline without centering or blockquote frame; the visual layout differs (centered framed images vs left-aligned inline images).
- **Recommended:** restore (centered image presentation is a meaningful visual element; `<blockquote>` framing with centered image is a recognizable WP layout pattern)

---

### B-5: `hdmi2usb-snippets` — 4 `<p>&nbsp;</p>` spacer paragraphs
- **Affected post:** `_posts/2014-07-21-hdmi2usb-production-board-bring-up-snippets-prep-work.md`
- **WP artifact:** Oracle has 4 `<p>&nbsp;</p>` spacer paragraphs between sections, creating visual whitespace between topic clusters.
- **Oracle source URL:** `https://blog.mithis.net/archives/timvideos-us/1976-hdmi2usb-production-board-bring-up-snippets-prep-work`
- **Current built rendering:** No spacer paragraphs; sections run together with standard paragraph spacing only.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <p>&nbsp;</p>
  ```
  (4 instances, one at each oracle spacer location.)
- **Accept-divergence option:** Standard paragraph spacing between sections; no extra visual gap. Functionally equivalent for reading; visually the sections are less separated.
- **Recommended:** accept (empty NBSP paragraphs are a WP layout hack; standard paragraph spacing is semantically cleaner; the content is unaffected)

---

### B-6: `hdmi2usb-day-5-6-7` — 3 `<p>&nbsp;</p>` spacer paragraphs
- **Affected post:** `_posts/` (search `hdmi2usb-production-board-bring-up-day-5-6-7`)
- **WP artifact:** Oracle has 3 `<p>&nbsp;</p>` spacer paragraphs, same pattern as B-5.
- **Oracle source URL:** `https://blog.mithis.net/archives/timvideos-us/` (slug: `hdmi2usb-production-board-bring-up-day-5-6-7`)
- **Current built rendering:** No spacer paragraphs.
- **Restoration option (§7 inline HTML):** Same as B-5 — 3 `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance --><p>&nbsp;</p>` instances.
- **Accept-divergence option:** Same as B-5.
- **Recommended:** accept (same reasoning as B-5)

---

### B-7: `epiphany2firefox` — centered `<p style="text-align: center">` screenshot
- **Affected post:** `_posts/2008-04-10-epiphany2firefox.md`
- **WP artifact:** Oracle wraps the screenshot image in `<p style="text-align: center">` for centered presentation. The WP source used Wayback-archived image URL (the post's `<img>` currently points to a Wayback URL due to prior migration).
- **Oracle source URL:** `https://blog.mithis.net/archives/linux/71-epiphany2firefox`
- **Current built rendering:** The screenshot renders as an `<img>` tag (inline HTML, already present in the post as `<img alt="Screenshot of my Firefox" src="http://web.archive.org/web/…" …/>`) without center alignment. The image is left-aligned.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <p style="text-align: center"><img alt="Screenshot of my Firefox" src="…"/></p>
  ```
- **Accept-divergence option:** Left-aligned screenshot. The image is already inline HTML (with fidelity-allow sentinel handling its `<img>` tags via the existing linter allowance); only the centering wrapper is missing.
- **Recommended:** restore (centering is a meaningful layout choice; `<p style="text-align: center">` is minimal inline HTML per §7 and matches the oracle exactly)

---

### B-8: 3 linked-thumbnail `<a title="…">` hover-tooltips — `almost-there`, `google-patchwork` (×2)
- **Affected posts:**
  - `_posts/2007-05-09-almost-there.md` — `title="CFXS Try2 PCB Board"` on linked thumbnail `<a>`
  - `_posts/2008-02-04-google-patchwork.md` — `title="Google patchwork."` and `title="Google Transsision"` on two linked thumbnails
- **WP artifact:** Original WP `<a>` elements carrying `title=` attributes for hover tooltips. The alt text, image, and thumb→full link are faithfully preserved; only the `<a>` tooltip attribute is lost.
- **Oracle source URLs:**
  - `https://blog.mithis.net/archives/pcb/40-almost-there`
  - `https://blog.mithis.net/archives/google/53-google-patchwork`
- **Current built rendering:** Pure Markdown `[![alt](thumb)](full)` — renders correctly with alt text and link, but produces `<a href="full"><img alt="alt" src="thumb"/></a>` with no `title=` on the `<a>`. Hover tooltip lost.
- **Restoration option (§7 inline HTML):**
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <a href="/assets/images/…/cfxs-try2.jpg" title="CFXS Try2 PCB Board"><img alt="CFXS Try2 PCB Board" src="/assets/images/…/cfxs-try2.thumbnail.jpg"/></a>
  ```
  (One per affected image-link; Markdown's `[![](thumb)](full)` syntax cannot carry a link `title=`.)
- **Accept-divergence option:** Ship pure Markdown — current state. The hover tooltip (a small UX nicety) is lost; the image, alt text, and link functionality are intact.
- **Recommended:** either (the tooltip is tiny user-visible delta; both options are §7-compliant; pure Markdown is simpler)

---

### B-9: `starhunter` — inline `<img>` with `title=` attribute (possible linked-thumbnail wrapper)
- **Affected post:** `_posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md`
- **WP artifact:** Post contains an inline `<img … title="Tulip - The ship from Starhunter" …/>` — the `title=` attribute is an img hover-tooltip. FOLLOWUPS PSL item 6 notes "oracle has an empty `<div>` thumbnail wrapper (probably the linked-thumbnail tooltip case already in the P6 USER-DECISION list)". Verify against oracle: does the live page wrap this `<img>` in an additional `<div>` container?
- **Oracle source URL:** `https://blog.mithis.net/archives/sci-fi/102-starhunter-fireflys-little-known-older-cousin`
- **Current built rendering:** The `<img>` is inline HTML (already has a `fidelity-allow` sentinel via the existing linter pass or is covered by the `<img>` exception). The `title=` is preserved on the `<img>`. If oracle also has a `<div>` wrapper, that wrapper is absent.
- **Restoration option (§7 inline HTML):** If oracle wraps in a `<div>`, add:
  ```html
  <!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
  <div class="…"><img … title="Tulip - The ship from Starhunter" …/></div>
  ```
- **Accept-divergence option:** `<img>` renders without the `<div>` wrapper. Visual difference depends on whether the `<div>` carried alignment/sizing CSS.
- **Recommended:** verify oracle first; if the `<div>` is present and carries visible styling, restore; otherwise accept.

---

## §D — Queue C: Deferred / Non-Issues

Items recorded in FOLLOWUPS that are either out of P6 scope, require a future dedicated pass, or have been confirmed as non-issues.

### C-1: Multi-category UNDER-IMPORT systemic pass
The FOLLOWUPS §"SYSTEMIC/HIGH — corpus-wide multi-category UNDER-IMPORT" documents that 11+ categories have post counts lower than the live WP oracle (gaming-miniconf 1 vs 7; summer-of-code 1 vs 8; etc.) due to the original WP→Jekyll migration importing posts with only their primary category. This is a HIGH-priority gap, but it requires its OWN dedicated oracle-driven systemic pass (brainstorm→spec→plan→subagent cycle) with:
(a) corpus completeness audit vs live WP, (b) per-post multi-category restoration, (c) P3-style re-import of any genuinely-missing posts, (d) sidebar count correction. Gate: every category page's post set == live WP oracle's. This is NOT a P6-EXEC-auto item (too large; needs a dedicated spec); it is the NEXT major phase after P6.

### C-2: flat WP→MD list/paragraph structure (PSL COMPLETED)
The FOLLOWUPS §"P6/SYSTEMIC — flat WP→MD lists" systemic gap has been RESOLVED by the PSL phase (19 commits; 76/76 posts; structural shape oracle-by-oracle). PSL-RESULTS confirms the exit gate was met. This item is CLOSED; no further action.

### C-3: P5-era `build.py` and `run.py` hardening items
Multiple FOLLOWUPS items note `build.py` regex anchoring (`\bwarning:\s` could match Ruby warnings; `Conflict:` unanchored; no explicit `encoding=` in `subprocess.run`); `run.py` robustness (no top-level try/except; `proc.wait()` after kill; renderer deduplication). These are fail-safe hardening items (false-positive → noisy block, never false-negative → missed error). They do not affect P6 fidelity; deferred to a future maintenance pass.

### C-4: PSL polish items 3 and 4 (commit metadata cosmetics)
- PSL Phase 3 fix commit `96ecd0b` Co-Authored-By says `Claude Sonnet 4.6` instead of `Claude Opus 4.7 (1M context)`. Cosmetic; no functional impact. Recorded; no action needed (the commit is on `main`; amending is not worthwhile for a trailer mismatch).
- PSL Phase 2 commit subjects >72 chars (4 commits: `0e955ee` 82c, `34ff90c` 80c, `e6e3998` 75c, `32b0d27` 75c). Cosmetic; commits are on `main`; not worth rewriting history for a guideline overage. Recorded.

### C-5: Search form `action=` and `aria-live` for accessibility
FOLLOWUPS §"P2/P5/P6 — from P1-T8 (search) review" notes `_includes/sidebar.html` search widget has stale ids and the search results list has no `aria-live="polite"`. These are UX/a11y improvements, not fidelity gaps. Deferred beyond P6.

### C-6: `_layouts/category.html` `barthelme_author_link()` gap
FOLLOWUPS §"P1/P6 — structure_check gate-coverage" notes `archive.php` L42 `barthelme_author_link()` is absent from `category.html`. Acceptable for a single-author blog; deferred.

### C-7: P4/P6 build-determinism nuance (feed pubDate)
FOLLOWUPS §"P4/P6 — build-determinism nuance" notes the only cross-build byte difference is `{{ site.time }}` in feed `pubDate`/`lastBuildDate` — normal Jekyll/RSS behavior. The Wayback sweep MUST normalize these (not flag as deltas). This is a CONSTRAINT on the A-5 sweep methodology, not a separate action item.

### C-8: `xml/` sitemaps excluded from build
FOLLOWUPS M2 notes `_config.yml` excludes `xml/` (WordPress-era sitemap fragments). This is correct; the note is "don't treat exclusion as a regression during P4/P6 sitemap work." No action; confirmed correct.

### C-9: `404.html` `div#content` missing `class="hfeed"` — confirmed faithful
FOLLOWUPS §"P4/P5/P6 — from P1-T7 (notfound) review" notes the 404 page's `div#content` has no `class="hfeed"` — this is FAITHFUL to Barthelme's `404.php`. Do NOT flag as a defect in the P6 audit. Recorded as a confirmed-faithful exception.

### C-10: `_includes/comments.html` whitespace cosmetic
FOLLOWUPS §"P5 — comment-system follow-ups" notes the comment include emits ~2 blank lines of HTML whitespace before `<div class="comments-section">`. Optional `{%- -%}` whitespace-control in a future pass. Not a visible/render defect; deferred.

### C-11: P0→P5 build harness minor improvements backlog
Including: `_split_front_matter` edge cases (CRLF, EOF without trailing newline); `_check_image`/`lint_paths` type annotations (M1/M2); `lint_paths` and `asset_root=None` unit tests (M3/M4); `barthelme.py` inline comment and `anchors_in_html` unit test. All pre-existing; all non-gating. Deferred to a future maintenance pass.

### C-12: Wayback resolver call-site hardening
FOLLOWUPS §"P3/P6 — wayback resolver call-site hardening" notes `scripts/fidelity/wayback.py` callers should wrap in try/except for network failures and add rate-limiting. P6-EXEC-auto's Wayback sweep (A-5) should implement this discipline in its sweep script; the `wayback.py` module itself is unchanged.

---

## §E — Recommended P6-EXEC-auto Sequencing

Execute in this order to keep each commit green and reviewable:

1. **A-3** (uv platform pin) — smallest, no test impact, prevents future environment breakage.
2. **A-1** (P5 polish bundle) — 5 cosmetic source fixes; one commit; tests stay green.
3. **A-2a** (trailing whitespace strip across 6 posts) — mechanical; one commit; linter 0 confirmed.
4. **A-2b** (`<hr>` linter coverage + resolve surviving `<hr/>` in timvideos-2016) — linter change + one post fix; one commit; test the new finding fires and is suppressed correctly.
5. **A-2c** (NBSP in hdmi2usb-day-8 — oracle-verify first, then fix-or-document) — one commit.
6. **A-4** (fritzbox region-3 blank line) — trivial cosmetic; one commit; build clean confirmed.
7. **A-7** (functional category sweep — script scan, no code changes) — verification commit to `P6-WAYBACK-SAMPLE.md`.
8. **A-9** (Picasa header byte-fidelity) — Wayback fetch + compare; note committed.
9. **A-8** (P3 comment-data spot-check — 3 posts) — Wayback fetch + compare; note committed.
10. **A-5** (Wayback pixel-sample sweep — ~10 posts) — the main EXEC work; one committed report.
11. **A-6** (CSS micro-deltas) — comparison + committed audit section.

Then collect all Queue B items (B-1 through B-9), present to user with before/after for each, and await explicit decision (restore OR accept) per item.

Gate check after A-2b: `uv run python -m scripts.fidelity.lint_content _posts --asset-root .` exits 0; `uv run python -m pytest tests/ -q` green; `bundle3.3 exec jekyll build` clean.

---

## §F — P6 Exit Gate (per design §11 acceptance bar)

All of the following must hold before P6 is closed:

1. **Queue A complete:** all autonomous items applied (A-1 through A-9); harness gates green (linter 0, structure_check 6/6, 54+ pytest, build clean).
2. **Queue B resolved:** user has given an explicit ACCEPT or RESTORE decision for each of B-1 through B-9; any RESTOREs implemented with `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->` sentinels; linter remains 0 post-restore.
3. **Wayback pixel sweep committed** (`P6-WAYBACK-SAMPLE.md`): all sampled posts PASS or documented-accepted delta; no unexplained structural divergence.
4. **CSS micro-delta audit committed:** all deltas dispositioned (faithful / accepted / fixed).
5. **User final visual signoff:** user reviews the Wayback comparison + built site and approves.
6. **DNS cutover performed by user:** CNAME `blog → mithro.github.io`; GitHub Pages custom-domain + Enforce HTTPS enabled.

**One-line statement:** Autonomous items applied + USER-DECISION items collected from user + Wayback pixel sweep PASS + user approves visual review + DNS cutover done = P6 goal met and migration complete.
