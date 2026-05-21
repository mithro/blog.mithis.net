# Cross-phase follow-ups (accumulated during P0 execution)

Living list of items discovered while executing the P0 plan that are deliberately
deferred to a later phase (out of P0 scope). Task 13 folds this into P0-RESULTS.md
and the P1/P2/P5 plans. Do NOT action these during P0 unless a P0 task explicitly
covers them.

## P7-pivot — "broken stuff and all" fidelity directive (2026-05-21)

**User directive received during P7-EXEC:** "The github version should be faithful
to the current live https://blog.mithis.net - broken stuff and all."

This **supersedes** the prior CLAUDE.md requirement "Remove Broken Features: Twitter
integration and Google Picasa integration." From this point:
- All Picasa/Shashin integrations are RESTORED (broken ggpht.com URLs preserved as-is)
- Twitter cached tweet widget is RESTORED (broken API links preserved as-is)
- The P7-EXEC subagent (2026-05-21) applied:
  - Header: restored Shashin table+gallery structure (exact live HTML, 6 thumbnails)
  - Sidebar: restored aktt-widget (3 cached tweets) + Shashin photos widget (14 entries)
  - CSS: added shashin.css rules verbatim from live WP plugin
  - CLAUDE.md updated to reflect "Full WP Fidelity" vs "Remove Broken Features"
  - P6-PICASA-CHECK.md prepended with disposition-inversion note

Files changed in P7-pivot commits:
- `_includes/header.html` — Shashin gallery restored
- `_includes/sidebar.html` — Twitter + Shashin photo widgets restored
- `assets/css/main.css` — Shashin CSS added
- `CLAUDE.md` — "Full WP Fidelity" requirement added
- `docs/superpowers/plans/P6-PICASA-CHECK.md` — inversion note prepended

## P2 — content remediation worklist (from Task 5 linter smoke run)

`scripts/fidelity/lint_content.py` over `_posts/*.md` (asset_root='.') → **47 findings**:
- `BLOCK_HTML`: 25 — hardcoded structural HTML in posts to convert to Markdown.
- `LIQUID_LEAK`: 11 — unrendered `{{`/`{%` committed into post content.
- `MISSING_IMAGE`: 11 — several are `{{ ` artifacts secondary to LIQUID_LEAK
  (they disappear once the Liquid leaks are fixed); the rest are genuinely
  missing local images.
(Task 13 regenerates the exact authoritative list grouped by code and by post.)

## P5 — prerequisites before wiring `lint_content` as the build gate

- **PARTIAL RESOLUTION (P2 Task L):** P2 Task L implements a `fidelity-allow`
  sentinel allowance in `lint_content.py` — a `<!-- fidelity-allow: BLOCK_HTML
  necessary-embed — <reason> -->` HTML comment adjacent to a BLOCK_HTML occurrence
  suppresses that one finding. This was required to resolve the 1 N finding
  (`techtalk-gamingforfreedom:22` Flash embed) without counting it against the P2
  exit-gate "exactly 22" residual. The sentinel is per-occurrence (not
  file-wide); un-annotated block HTML is still flagged. The broader F-lint/F-norm
  refinement items below remain deferred (0 F-lint and 0 F-norm in the P2
  corpus). The sentinel mechanism (necessary-HTML allowance) is now established
  and available for future necessary-HTML cases in P5/P6.
  - **P5 polish (from Task L code review, non-blocking):** the
    `_FIDELITY_ALLOW_BLOCK_HTML` regex's trailing `\b` after `BLOCK_HTML` is
    redundant (the literal `fidelity-allow:` prefix already prevents partial
    matches) — drop or comment its intent; add a unit test for the `i == 0`
    body-first-line case WITH a (non-existent) preceding-line sentinel attempt
    to lock the negative-index guard; add a brief inline comment at the
    `prev_line` assignment noting fence predecessors are harmless; document the
    sentinel in the `lint_content` module docstring (ties to I5).

- **I3 (important):** unclosed fenced code block leaves `in_fence=True` to EOF,
  silently suppressing all findings below it. Before P5 makes the linter a hard
  gate, add an `UNCLOSED_FENCE` finding so CI is self-diagnosing, not silently
  permissive. Reviewer-suggested one-liner (append after the loop, before
  `return out` in `lint_text`):
  ```python
  if in_fence:
      out.append(Finding(path, body_start + i, "UNCLOSED_FENCE",
                         "Fenced code block was never closed"))
  ```
- **I5 / docstring:** document the known false-positive classes in the
  `lint_content` module docstring: Liquid-in-inline-code, and structural HTML
  inside 4-space indented code blocks (the plan already accepts inline-code FP as
  a conscious limitation; make it explicit in-code for P5 gate users). Also
  document the `fidelity-allow` sentinel (added in P2 Task L) in the docstring.
- **I1/I2 (hardening):** `_split_front_matter` edge cases — front matter that
  closes at EOF with no trailing newline (potential off-by-one), and an explicit
  CRLF assumption note. Not triggered by the current corpus; harden before the
  gate is enforced.
- **M1/M2:** add missing type annotations to `_check_image` and `lint_paths`
  (consistency with the rest of the module).
- **M3/M4:** add tests for `lint_paths` (file-read/`str(p)` path) and for
  `asset_root=None` (image check skipped) before relying on it as a gate.

## P5 — build-gate (`build.py`) hardening before it becomes the CI gate (from Task 8 review)

All fail-safe (false-positive → noisy block, never false-negative → missed
error); plan-verbatim so deliberately not changed in P0:
- `\bwarning:\s` (IGNORECASE, unanchored) can match Ruby `--trace` gem/bundler
  warnings like `/path.rb:N: warning: ...` → spurious CI block if a future gem
  emits one. Consider anchoring to Jekyll's own `warning:`/`Build Warning:`
  forms or excluding Ruby-backtrace lines.
- `Conflict:` is unanchored — could match a post whose build-output line text
  contains "Conflict:" (not seen in Jekyll's actual output, but tighten to
  line-start `^\s*Conflict:` for safety).
- `run_build` uses `subprocess.run(..., text=True)` with no explicit
  `encoding=`; under a non-UTF-8 CI locale (`LANG=C`) non-ASCII Jekyll output
  could raise `UnicodeDecodeError` and crash the gate instead of returning
  `(False, log)`. Add `encoding="utf-8", errors="replace"`.
- Minor: add a comment in `tests/fidelity/test_build.py` stating `run_build` is
  integration-verified by design (not a unit-test oversight).
- `report.py` (Task 10): if the fidelity report ever becomes
  machine-parsed/strict-Markdown-rendered, escape `Finding.message`/`archetype`
  and guard `build_log_tail` against a lone ` ``` ` line closing the fence.
  P0-fine today (controlled inputs; Jekyll logs have no triple-backticks).

## P4 — 22 R-P4 LIQUID_LEAK/MISSING_IMAGE findings transferred from P2-T1 triage

**P4 now ALSO owns** (from P2-T1 triage, commit `97323c4`): the 22 R-P4
findings — after setting `baseurl:""`+CNAME (P4's core job), strip the
redundant `{{ … | relative_url }}` Liquid in ~12 post image lines (11
LIQUID_LEAK + 11 co-located MISSING_IMAGE across the ~8 affected posts listed
in P2-FINDINGS §6 "P4-COUPLED") to plain `/assets/…` (then pure-Markdown,
faithful, correct), and run the FINAL post-corpus `lint_content`-0 gate.
P2's exit gate is linter-clean EXCEPT these 22 by design (expected residual:
exactly 22 LIQUID_LEAK/MISSING_IMAGE findings remain after P2 completes).

**Why deferred:** `_config.yml` currently has `baseurl:"/blog.mithis.net"`.
kramdown does NOT prepend baseurl to Markdown image/link paths — it is a
Jekyll server-level routing prefix. Replacing `{{ '/assets/x' | relative_url }}`
with plain `/assets/x` now would render `<img src="/assets/x">` instead of the
correct `<img src="/blog.mithis.net/assets/x">`, breaking image URLs on the
current deployment. There is no pure-Markdown form that is BOTH no-Liquid AND
baseurl-correct under a non-empty baseurl. The fix is only safe and correct
once P4 sets `baseurl:""`.

**P4 action:** (1) set `baseurl:""`+CNAME; (2) in the ~8 posts, replace each
`{{ '/assets/…' | relative_url }}` with the plain `/assets/…` path; (3) run
`lint_content` over all `_posts/*.md` → 0 findings (the post-corpus
linter-0 final gate). See P2-FINDINGS.md §4 "P4-COUPLED findings" for the
exact file+line inventory.

---

## P4/P6 — build-determinism nuance & excluded WP artifacts (from final P0 review)

- **M1 (P6):** the post-2A build is deterministic for ALL HTML/structural
  content (byte-identical across builds); the ONLY cross-build byte difference
  is `{{ site.time }}` in category-feed + first-party `feed.xml`
  `<pubDate>`/`<lastBuildDate>` — normal Jekyll/RSS behavior, NOT the
  destination-collision nondeterminism 2A fixed (that is fully gone: 0
  `Conflict:`). The P6 Wayback/byte pixel-sweep MUST normalize feed
  `pubDate`/`lastBuildDate` or it will report spurious feed deltas. (The
  word "deterministic" in P0-RESULTS/2A commit means "structurally
  deterministic"; the fidelity oracle is structural+visual on HTML, which is
  fully deterministic.)
- **M2 (P4/P6):** `_config.yml` excludes `xml/` (a deliberate Task 2 Step 4
  leak-fix, but not recorded at the time). `xml/sitemaps/` = 30 WordPress-era
  source sitemap fragments (`sitemap-pt-post-YYYY-MM.xml`), NOT Jekyll output —
  Jekyll generates its own `sitemap.xml`/`sitemap_index.xml`. Excluding them is
  correct (else they'd leak stale WP sitemaps into `_site`). P4/P6 sitemap work
  must treat `xml/` as an intentionally-excluded WP artifact, not a regression.
- **M3 (P5):** `run.py` only surfaces the build log into the report on FAILURE;
  on a clean build no full build log is persisted. When build.py becomes the CI
  gate (P5), persist the full build log unconditionally for CI debuggability.

## P1/P5 — orchestrator (`run.py`) robustness (from Task 12 review)

Plan-verbatim, non-gating at P0; harden when the render path / CI matters:
- **P1:** after `proc.kill()` in the serve-teardown `except TimeoutExpired`,
  add `proc.wait()` to reap the SIGKILLed zombie (currently relies on
  `Popen.__del__`; not a hang, just process hygiene). Only affects the
  not-skip render path.
- **P1:** `main()` has no top-level try/except — if `run_build()` raises
  (e.g. bundler missing) or a Barthelme template file is absent, it crashes
  with a traceback instead of writing a partial report + returning 1. Wrap
  for a harder-to-silently-break gate.
- **P5:** the `## Renderer` section is string-appended in `run.py` (report.py
  frozen) — if a later phase adds a renderer section to report.py, dedupe to
  avoid a double section.
- **P5:** guard `(BARTHELME / a.barthelme_template)` when template is "" (only
  reachable if someone adds a structural archetype with no template; today the
  feed archetype is structural=False so it's safe).
- **P0-RUN visual diff (post-P4):** the real structural diff requires the
  Playwright render, which is (a) heavyweight and was OOM-adjacent with leaked
  `playwright-mcp` procs, and (b) not meaningful until P4 sets `baseurl=""` —
  the served site is currently at `http://localhost:4000/blog.mithis.net/`, so
  `capture_all("http://localhost:4000")` would 404 every archetype. After P4,
  re-run WITHOUT `FIDELITY_SKIP_RENDER` locally to get the real per-archetype
  structural diff (the structural section in P0-RESULTS.md is the PHP-side
  anchor inventory = the P1 theme target list, not yet a Jekyll-vs-PHP diff).

## P2 — internal-linking + category-prose reconciliation (from final P1 review)

- **M1 (P2, pre-existing — verify before P2 spec):** `_layouts/home.html` links
  each post's categories to `/archives/category/<slug>` which does NOT exist in
  `_site` (Jekyll builds category pages at `/category/<slug>/`). Also category
  display casing diverges across archetypes: home `| title` ("Summer Of Code"),
  category `| capitalize` ("Summer of code"), post raw slug. Byte-identical
  between `main` and the P1 HEAD → NOT introduced by P1 (correctly outside P1's
  structural scope), but it's a real broken-internal-link + inconsistency. P2
  (content/internal-linking) must reconcile to ONE category URL space
  (`/category/<slug>/`) and one title-casing rule across home/post/category.
- **M2 (P2 decision):** the per-category `.md` body prose ("Posts about
  hardware development…") is no longer rendered — the Barthelme-faithful
  `category.html` reads `page.description` front-matter (which the `.md`s don't
  set), not `content`; `div.archive-meta` is correctly present-but-empty
  (matches archive.php, which only renders WP `category_description()`). P2 must
  decide: keep dropped (more faithful) or move that prose into `description:`
  front matter to preserve it.
- Note (no action): `nav-below` Liquid recurs in 4 layouts but each is
  intentionally semantically distinct per its Barthelme source
  (post=prev/next-post, index/archive=prev/next-posts, search=static) — a blind
  shared include would be WRONG. Optional low-value parameterized-include
  cleanup only; not urgent (P5 at most).

## P2/P5/P6 — from P1-T8 (search) review (Minors, structural gate already green)

- **P2/P5:** `_includes/sidebar.html` search widget still has stale ids
  `search-input`/`search-results` (the old pre-rewrite ones; no JS wires them
  anywhere — pre-existing dead code). Convert it to a real
  `<form method="get" action="{{ '/search.html' | relative_url }}"><input
  name="s" ...></form>` so it submits to the working `?s=` handler. (Pairs with
  the P4 404/search form-action item.)
- **P2 (a11y):** the search results list has no `aria-live="polite"` — screen
  readers won't announce dynamically injected results. Add in the P2/a11y pass.
- **P2 (UX, minor):** no loading indicator if the user submits before
  `search.json` fetch resolves (brief "Nothing Found" flash). Optional polish.
- **P6 (general, supersedes the home-specific note):** Barthelme's
  `div#nav-below`/`div.navigation` has float children and the theme CSS has no
  clearfix, so an empty/realised nav-below computes zero height (observed on
  home, category, search). This is faithful to Barthelme's own CSS behavior;
  the P6 pixel sweep must confirm it matches the original (do NOT "fix" with a
  non-Barthelme clearfix unless the original visibly differs).

## P4/P5/P6 — from P1-T7 (notfound) review

- **P4 (functional):** `404.html` `form#error404-searchform` uses
  `action="{{ site.url }}"` → currently `https://mithro.github.io` (no baseurl).
  Barthelme posted `?s=` to the WP home (server-side search). On a static
  Jekyll site GET `?s=` does nothing. When P4 finalizes url/baseurl, fix the
  action (`{{ site.url }}{{ site.baseurl }}`, or just `{{ site.url }}` once
  baseurl="" + custom domain) AND decide fidelity-vs-function: likely point the
  404 (and search-archetype) form at the existing `/search.html` client-side
  search so it actually works. Structural anchor is present (P1 OK); this is
  P4/P5 functional.
- ~~**P1-T9 / P5:** tighten `tests/fidelity/test_structure_check.py`
  `test_phantom_anchors...` to assert the FULL set
  (`PHANTOM_ANCHORS == frozenset({Anchor("div","#post-")})`) so any future
  phantom addition is caught; rephrase the `PHANTOM_ANCHORS` NOTE comment as a
  standing invariant ("only genuine PHP dynamic-id artifacts belong here"),
  not an action log. (Fold into P1-T9.)~~
  **RESOLVED (P1-T9):** exact-set assertion added to `test_phantom_anchors_are_barthelme_dynamic_id_artifacts`; PHANTOM_ANCHORS block comment rephrased as a standing invariant with Barthelme source citations (single.php L8, index.php L8, archive.php L28, page.php L8). See FOLLOWUPS.md "P1 phantom-ignore justification (RESOLVED)" note.
- **P6 (do NOT flag as defect):** `404.html` `div#content` has NO `class="hfeed"`
  — this is FAITHFUL (`404.php` is the only Barthelme template omitting hfeed).
  The P6 structural/visual audit must treat 404's missing hfeed as correct, not
  a gap. If a later pass ever standardizes hfeed across archetypes, 404 stays
  the deliberate exception.

## P6 — user signoff: 3 linked-thumbnail `<a title="…">` hover-tooltips lost in P4 R-P4 pure-Markdown conversion (fidelity-vs-no-HTML; accepted per approved P4-FINDINGS §B)

- **What:** P4 Task B converted the 22 R-P4 image residuals. Three were
  linked thumbnails whose original WP `<a>` carried a `title=` (hover
  tooltip): `2007-05-09-almost-there.md` (`title="CFXS Try2 PCB Board"`) and
  `2008-02-04-google-patchwork.md` ×2 (`title="Google patchwork."`,
  `title="Google Transsision"`). The approved P4-FINDINGS §B chose the pure
  Markdown `[![alt](thumb)](full)` form (spec §7 prefers Markdown over inline
  HTML; linter-clean; spec+code review PASSED). Markdown's image-link syntax
  CANNOT carry a link `title=`, so the hover tooltip is lost (alt text,
  image, and the thumb→full link itself are all faithfully preserved — only
  the `<a>` tooltip differs).
- **The tension (same class as the fritzbox-bold item):** spec §7 *would*
  permit a minimal inline `<a href="…" title="…"><img alt="…" src="…"/></a>`
  here (a link `title` is genuinely Markdown-inexpressible — the same
  justification used for the width/height/class inline `<img>`s elsewhere in
  Task B). The approved §B deliberately chose pure Markdown for these three
  (simplicity / Markdown-first). It is a real, tiny, user-visible delta.
- **MANDATORY user signoff (acceptance bar #3):** P6 must show the user the
  before/after for these 3 image-links and get an explicit decision: (a)
  accept the lost hover-tooltip (ship pure Markdown — current state), or (b)
  restore via the §7-sanctioned minimal inline `<a title><img></a>` form.
  Do NOT silently claim 100% fidelity here. P4-Z handoff must surface this
  alongside the fritzbox-bold item.

## P6 — MANDATORY user visual signoff: bold emphasis lost inside fritzbox code blocks (fidelity-vs-no-HTML tension; accepted per approved §3.4)

- **What:** the 4 fritzbox (`2013-10-06-connecting-to-a-fritzbox-…vpnc.md`)
  code blocks in the live original are `<pre>` with **embedded `<strong>`**:
  pre-1 bolds `iphone = 1;` / `xauth_key = "xxxxx";`; pre-2 bolds `key_id` and
  the `use_xauth = yes; xauth { … }` block; pre-3 bolds all 5 replace-me
  placeholders (`ip address or DNS name…`, `[username entered…]`, `[shared
  secret key…]`, `[username…]`, `[password…]`). pre-4 (the shell script) has
  NO bold. The bold guides the reader to exactly the lines that matter.
- **The tension:** the project goal is BOTH "100% visual fidelity" AND "no
  hard-coded HTML in posts". A Markdown fenced code block is **literal** —
  kramdown cannot put `<strong>` inside `<pre><code>`. The ONLY ways to keep
  the bold are raw `<pre><strong>` HTML (violates "no hardcoded HTML" AND is
  exactly the BLOCK_HTML linter finding) or a non-existent kramdown extension.
  So fenced-code = bold is necessarily LOST; raw-HTML = goal violated. These
  two user constraints genuinely conflict here.
- **Decision (follow approved plan):** P2-R-E follows the approved P2-FINDINGS
  §3.4 remediation — convert each `<pre>` to a fenced ``` block with the
  oracle text **plain** (`<strong>` stripped to its inner text; NO literal
  `**` asterisks — the original showed bold text, never literal asterisks, so
  plain text is the closest faithful no-HTML representation). Bold emphasis is
  the accepted casualty of the no-hardcoded-HTML constraint.
- **MANDATORY ACTION — user signoff (acceptance bar #3):** this is precisely a
  "all other options exhausted → user does final visual signoff" case the user
  defined. P6 (or sooner if convenient) MUST explicitly show the user the
  before (bolded) vs after (plain code) for these 4 blocks and get an explicit
  decision: (a) accept the delta (ship plain code blocks), or (b) re-introduce
  emphasis via a sanctioned non-HTML mechanism (e.g. a `# >>>` comment
  convention, a callout, or an agreed minimal-inline-`<strong>` exception
  documented like the techtalk `fidelity-allow` sentinel). Do NOT silently
  ship this as "100% fidelity" — it is a known, user-visible reduction. P2-Z
  handoff MUST surface this prominently.

## P6 — source-cosmetic micro-nits (no render/fidelity impact; tidy in the cosmetic pass)

- **fritzbox R-E (commit `85e6d8c`):** region-3's closing ``` fence (the
  `IPSec gateway …` vpnc.conf template) is immediately followed by the
  `As this file contains usernames…` paragraph with NO intervening blank
  line, whereas region-4's closing fence has one before the following
  heading. CommonMark/kramdown require neither; rendered output is
  byte-correct vs the oracle (spec-review confirmed). Pure source-style
  uniformity nit — add one blank line after the region-3 closing fence in
  the cosmetic pass if desired. Non-blocking; left as-is in P2 to avoid
  re-opening an approved commit for a zero-render-impact change.

## P6 — CSS visual-audit micro-deltas (accumulate; verify in the pixel sweep)

- P1-T6: `_layouts/page.html` title class `page-title`→`entry-title` (faithful to
  page.php L9; the old `.page-title` on pages was a pre-existing mis-application
  of archive-context CSS). Net-neutral (font-size/align/weight identical; base
  `.entry-title` margin `0.5em 0` is overridden back to `0` by
  `div#content .entry-title`). P6 pixel sweep must confirm the page-title margin
  renders identically to the original (no vertical-rhythm shift).

## P1/P6 — structure_check gate-coverage + category fidelity minors (from P1-T5 review)

- **GATE-COVERAGE (P6 acceptance must cover this):** `structure_check` checks ONE
  representative per archetype (e.g. `category/hardware`). It did NOT catch that
  multi-word/hyphenated category pages (`summer-of-code`, `gaming-miniconf`,
  `timvideos-us`, …) were rendering "No posts found" (a Critical functional bug
  found only by the deeper code-review's multi-word verification, now fixed in
  T5 `01faf1d`). The structural gate ≠ functional correctness. **P6 final
  acceptance MUST include a functional sweep**: every one of the 19 category
  pages lists its posts; representative real variants of each archetype render
  (not just the single structure_check sample). Consider a P5/P6 helper that
  asserts no built page contains "No posts found"/empty content.
- **Minor (P1 later / when multi-category posts exist):** `_layouts/category.html`
  `entry-category` cross-link uses `{{ cat | replace:'-',' ' | capitalize }}` →
  "Summer of code" not "Summer Of Code". Inert today (all posts single-category
  so the loop body never emits). Fix to proper title-case / category-title
  lookup if multi-category posts are ever added.
- **Minor fidelity gap:** Barthelme `archive.php` L42 `barthelme_author_link()`
  (an author link in `entry-meta`) is absent from `_layouts/category.html`
  (and not required by the structural gate). Acceptable for a single-author
  blog; note for full visual fidelity / P6.

## P1 — `#post-0` gate-integrity (MUST action at P1-T7/T8) + T1 polish (from P1-T1 review)

- ~~**IMPORTANT (P1-T7 notfound, P1-T8 search):** `PHANTOM_ANCHORS` in
  `structure_check.py` includes `Anchor("div","#post-0")`. Unlike `#post-`
  (genuine PHP-strip artifact of `id="post-<?php the_ID()?>"`), **`#post-0` is a
  STATIC LITERAL** in Barthelme `404.php` and `search.php` (no-results branch) —
  a REAL structural element. Ignoring it could let T7/T8 falsely PASS. At T7 and
  T8: check whether built `_site/404.html` / `_site/search.html` contain
  `div#post-0`. If NOT, ADD `<div id="post-0">` to those Jekyll templates for
  fidelity AND remove `Anchor("div","#post-0")` from `PHANTOM_ANCHORS` (+ fix the
  test & comment). Keep it ignored ONLY if the built HTML genuinely contains it
  (then harmless). Do NOT mark notfound/search PASS until this is resolved.~~
  **RESOLVED (P1-T7/T8):** `div#post-0` added to `404.html` and `search.html`
  (real structural element). `Anchor("div","#post-0")` removed from
  `PHANTOM_ANCHORS`; notfound + search archetypes now pass the gate at 6/6.
- ~~**Minor (do in P1-T9 / opportunistically):** add a one-line comment in
  `ARCHETYPE_SITE_PATHS` explaining the `post` entry is a flat `.html` (no
  trailing-slash permalink → Jekyll writes flat file, not dir/index.html);
  restore the dropped phantom-rationale comment in
  `test_structure_check.py::test_phantom_anchors_are_barthelme_dynamic_id_artifacts`;
  split the `out = Path(...); out.mkdir(...)` semicolon line; note
  `check()`/`run_build()` assume repo-root CWD (untested in isolation).~~
  **PARTIALLY RESOLVED (P1-T9):** phantom-rationale comment restored and
  upgraded to exact-set invariant assertion. Remaining minor polish items
  (ARCHETYPE_SITE_PATHS comment, semicolon split, CWD note) deferred to P5
  as non-gating cleanup.

## P1 — structural-extractor phantom anchors (from Task 6 review)

When `barthelme.extract_anchors` runs on real templates, mixed static/dynamic
ids like `id="post-<?php the_ID(); ?>"` strip to `id="post-"` → a phantom
`Anchor(tag, "#post-")` (appears in single.php + ~6 other templates). Harmless
in P0 (the comparator only reports; P0 doesn't gate on structural), but in P1
this injects spurious "missing anchor" entries into the fidelity diff for every
looped/archetype page. P1 fix options: filter ids ending in `-`/clearly
partial, OR populate Task 7 `structural_diff(..., ignore=...)` with the known
phantom set (the comparator's `ignore` param was designed for exactly this).
Also (P1-minor): add a one-line comment to barthelme's `"<?" not in attr` guard
clarifying it catches strip failures (not pre-strip PHP); add an
`anchors_in_html` unit test.

## P3 — STATUS: source captured, phase de-risked (2026-05-19)

blog.mithis.net root = **HTTP 200** (TLS cert expired → fetch with verification
disabled; the content is what matters). The 4 missing posts each return
**HTTP 500** BUT the server still emits the FULL themed article page
(`entry-content`, `<h2 class="entry-title">…`, real titles, 21–24 KB) — this
500 is almost certainly the original migration-skip cause. Raw HTML snapshotted
to **`exports/p3-missing-raw/{15,35,84,92}.html`** (committed `cc4a28e`):

- 15 → `tp/15-tp-protocol-overview` — "Thousand Parsec Protocol Overview"
- 35 → `tp/35-using-tailor-to-go-to-git` — "Using Tailor to go to git"
- 84 → `ubuntu/84-my-three-weeks-on-a-mac` — "My three weeks on a Mac"
- 92 → `uncategorized/92-power-scripts-in-intrepid` — "WTF power scripts went in Intrepid…."

**P3 phase work** (its own spec→plan→subagent cycle, after P1/P2 unless the user
re-sequences): convert these 4 captures to Jekyll Markdown matching the existing
post format + dual comment representation, using the existing
`scripts/html_to_markdown.py` pipeline; set WordPress-exact permalinks
(`/archives/<cat>/<id>-<slug>`) + `wordpress_id`/`wordpress_category`/
`wordpress_url` front matter; run the P0 content linter on them; structure_check
must still pass. Wayback is now only a per-post cross-check/fallback (no longer
required — source is captured & durable). Flag to user: the live WP server 500s
on exactly these 4 posts (worth fixing server-side if a clean 200 is ever
wanted, but NOT required for P3 — the captures are complete).

## P3/P6 — wayback resolver call-site hardening (from Task 9 review)

`scripts/fidelity/wayback.py` is correct/minimal for P0 but its callers must
harden when authored:
- P3's per-missing-post loop MUST wrap `snapshot_url(...)` in
  `try/except (urllib.error.URLError, http.client.RemoteDisconnected)` so one
  network failure doesn't abort the whole recovery sweep.
- Consider `https://archive.org/wayback/available` (currently `http://`; works
  via redirect but adds a round-trip) and set a descriptive `User-Agent` +
  modest rate-limit/retry when calling in a tight P3 loop (archive.org throttles).
These are call-site responsibilities (the module's DI `opener` seam supports a
retry/UA opener cleanly) — not P0 module defects.

## P1 — theme/structure fidelity & cleanup (from Task 2A)

- Remove orphaned dead code `_includes/category-feed.xml` (no callers; left in
  place by Task 2A per minimal-change constraint).
- Audit category-casing inconsistency: `category/<cat>.md` archive pages carry
  title-case `category:` (e.g. "Summer Of Code") while posts use slug
  `categories: [summer-of-code]`; the `category` layout filters on it. Static
  feed files correctly use the slug. Confirm archive pages list posts correctly
  and normalize casing.

## P1 phantom-ignore justification (RESOLVED — P1-T9)

`PHANTOM_ANCHORS == { div#post- }` — exactly one member; justification:

Barthelme's content templates emit a per-post wrapper whose `id` attribute is
computed at PHP request time:

- `theme_analysis/barthelme/single.php` L8:
  `<div id="post-<?php the_ID(); ?>" class="<?php barthelme_post_class(); ?>">`
- `theme_analysis/barthelme/index.php` L8:
  `<div id="post-<?php the_ID() ?>" class="<?php barthelme_post_class() ?>">`
- Also: `archive.php` L28, `page.php` L8, `attachment.php` L8, `image.php` L8,
  `search.php` L12, `links.php` L13, `sitemap.php` L12, `archives.php` L13.

PHP-stripping (the P0 static extractor strips `<?php … ?>` blocks) reduces
`id="post-<?php the_ID(); ?>"` to the bare prefix `id="post-"`, which the
anchor extractor normalises to `#post-`. This token is NOT a valid CSS id (it
has no numeric suffix) and NO faithful Jekyll output can or should carry it —
Jekyll emits concrete post ids (`post-2186`, `post-84`, …) never the bare
prefix. Ignoring `div#post-` in `structure_check` is therefore correct.

`#post-0` was de-listed in P1-T7 (commit `63b1d47`; resolved under the
`#post-0 gate-integrity` item above): it IS a static literal in Barthelme's
`404.php` and `search.php` (no-results branch) — a REAL structural element now
enforced by the gate and satisfied by the T7/T8 template additions.

The standing invariant (only genuine PHP dynamic-id artifacts, never static
literals) is now encoded both in the `PHANTOM_ANCHORS` block comment in
`scripts/fidelity/structure_check.py` and in the exact-set assertion in
`tests/fidelity/test_structure_check.py::test_phantom_anchors_are_barthelme_dynamic_id_artifacts`.

**Picasa header literal-fidelity note (P1-T9):** `_includes/header.html`
contains the Picasa photo-gallery strip unchanged from its creation commit
(`8d0ada8`). No P1 branch commit has touched it (confirmed via `git log
--oneline -- _includes/header.html`). Decision: replicate the Picasa strip
EXACTLY (literal fidelity) for now; any improvement (broken lh3.ggpht.com
thumbnails, picasaweb.google.com links now defunct) is deferred to P6 visual
audit. Deep byte-fidelity vs the now-reachable live site is a P6 concern.

## SYSTEMIC/HIGH — corpus-wide multi-category UNDER-IMPORT (discovered in P4 D-B; the single largest remaining fidelity gap; needs a DEDICATED pass + USER DECISION)

- **Symptom:** the live-WP oracle sweep during P4 D-B found **11 categories
  whose built post count < the live WP count** (gaming-miniconf 1 vs 7;
  summer-of-code 1 vs 8; google 3 vs 7; uni 2 vs 5; python 4 vs 6; pcb 3 vs
  5; diary/games/highlights/ubuntu/useful-bits each −1). See P4-RESULTS §4
  for the table.
- **Confirmed cause (at least partly):** the original WP→Jekyll migration
  (P0/P1 era) imported many posts with ONLY their PRIMARY WP category. Proof:
  live WP shows posts 75/66/65/62/61/46 in BOTH `lca` AND `gaming-miniconf`;
  in `_posts` they exist but carry `categories: [lca]` only → they don't
  appear on the `gaming-miniconf` page; that page (and ~10 others) and the
  sidebar counts under-report. D-B oracle-fixed exactly this for its scoped
  14 posts; the count table proves it is SYSTEMIC, far beyond D-B's slice.
- **OPEN QUESTION (unresolved — the dedicated pass must answer first):** is
  some shortfall ALSO entirely-missing posts (corpus < live WP), which would
  contradict the design's "76/76 posts" success criterion (§11), or is it
  purely under-categorization of the 76 we have? `gaming-miniconf` is proven
  pure under-categorization; the others are NOT yet proven to be only that.
- **Why it MUST be addressed:** the goal is *verified 100% fidelity*; faithful
  category membership is part of it (the original blog showed every post in
  ALL its WP categories). This is now the single largest known fidelity gap.
- **Owner / shape:** a **dedicated oracle-driven systemic pass** (own
  brainstorm→spec→plan→subagent cycle, like P2-R / P3 / the flat-list pass):
  (a) audit true corpus completeness vs the live WP (enumerate live WP posts;
  compare to our 76; resolve the open question); (b) for EVERY post, fetch
  its live `rel="category tag"` set and restore the faithful full
  multi-category `categories:` front matter (front-matter-only, oracle-exact,
  per-post 2-stage reviewed — same rigor as D-B); (c) P3-style re-import any
  genuinely-missing posts; (d) THEN correct/auto-compute the sidebar counts
  (ties to the P5 dynamic-count item). Gate: every category page's post set
  == the live WP oracle's, corpus-wide.
- **P4 interim posture (deliberate, faithful):** P4 left the hardcoded
  sidebar counts at the WP-oracle values for the 11 affected categories
  (they match the ORIGINAL Barthelme sidebar — faithful; the built shortfall
  is THIS gap, not a label bug). Only `lca`/`hdmi2usb` (D-B achieved full
  faithful membership → built==oracle) were corrected. Do NOT "fix" the
  others by lowering them to built counts (that would be LESS faithful) —
  fix the underlying membership in the dedicated pass.
- **USER DECISION pending (surfaced by the controller after P4 merge):**
  whether to run this dedicated systemic pass next (recommended — it is core
  to the 100% goal), its priority vs P5/P6, and how to treat any
  genuinely-missing posts vs the "76/76" criterion.

## P6/SYSTEMIC — flat WP→MD lists don't reproduce original list structure (HIGH — core to the 100%-fidelity goal; surfaced repeatedly during P2-R-C/R-D)

- **Symptom (systemic, NOT linter-detectable, NOT in the 47 P2 findings):** the
  WP→MD export emitted post bodies with NO blank-line separators and ALL list
  items flattened to top-level `- ` (no indentation). kramdown (`input: GFM`)
  therefore renders structures that DIVERGE from the live original even though
  the Markdown is valid and has zero raw HTML:
  - Consecutive prose lines merge into ONE `<p>` (e.g. `cfxs-free` lines 15–18
    render as a single `<p>`; the original had separate `<p>` per paragraph).
  - Multi-level nested `<ul><li><ul>…</ul></li></ul>` (live oracle confirmed on
    `hdmi2usb` day-2/day-3) is flattened to a single-level list.
  - A list that the original CLOSED, followed by an interstitial
    `<p><strong>…</strong></p>` and a NEW `<ul>`, instead renders as one
    continuous `<ul>` absorbing the strong-text + following items (confirmed by
    the R-D day-5 spec review: live oracle = 3-`<li>` "25th July" `<ul>` then
    `<p><strong>Streaming System Hacking</strong></p>` then a new `<ul>`; built
    site = one 16-item `<ul>`). Present byte-identically in parent commits — a
    pre-existing export artifact, not introduced by any P2 commit.
- **Why P2 does NOT fix this:** P2's approved scope (spec §7 / P2-FINDINGS) is
  the content-LINTER findings = raw mangled HTML only. This flat-structure
  divergence is *valid* Markdown with no raw HTML, so the linter cannot and does
  not flag it; "re-nesting/blank-lining the whole corpus" is explicitly out of
  P2-NOW scope and was deliberately left untouched in R-C/R-D (only the
  finding-local sublist tied to a mangled `</li> /li>` closer is restored, per
  P2-FINDINGS §3.5). Touching it post-wide in P2 would be unbounded scope creep
  and would conflate two different problems.
- **Why it MUST be addressed (owner):** the project goal is *verified 100%
  visual fidelity*. This systemic divergence affects MANY posts (every
  multi-paragraph / nested-list post) and is exactly the gap between "no raw
  HTML in posts" (P2) and "renders pixel-identical to the original" (P6). It is
  almost certainly too large+structural for the P6 *CSS* micro-delta sweep
  alone — recommend a **dedicated systemic content-structure pass** (its own
  brainstorm→spec→plan→subagent cycle) BEFORE or AS PART OF P6, driven by the
  now-reachable live oracle (TLS cert expired → verify-disabled fetch), that
  restores faithful paragraph separation + list nesting/breaks across the whole
  `_posts` corpus WITHOUT hardcoding HTML (i.e. correct Markdown blank-lines +
  indentation), with a structural diff vs the live original as the gate. The P6
  Wayback/live pixel sweep + user signoff will otherwise fail on these posts.
- **Action:** P2-Z handoff MUST surface this prominently to P3/P6 planning; the
  P6 (or dedicated-pass) spec MUST own a corpus-wide list/paragraph-structure
  fidelity gate. Do NOT lose this between phases.

## P5-housekeeping — corpus-wide EOF trailing-blank-line normalization (MINOR, cosmetic, NOT P2)

- **Observation (R-D day-2 spec review):** many `_posts/*.md` end with `\n\n`
  (one trailing blank line) rather than a single `\n`, a WP→MD export artifact
  present corpus-wide. It is invisible (kramdown ignores trailing blank lines —
  zero render/fidelity impact), NOT a content-linter finding, and NOT in the 47.
- **Why P2 does NOT touch it:** mid-file P2 edits (R-D day-2/3/5) correctly do
  NOT alter EOF bytes outside their edit region — preserving the pre-existing
  byte is the faithful, in-scope behaviour (changing it would be unrequested
  drift). Posts whose P2 edit happened to be AT EOF (R-A's 6 `<style>`
  removals) legitimately normalized to a single `\n` because the injected
  block's removal restored the original pre-injection EOF — so the corpus is
  now MIXED (single-`\n` for R-A's 6; `\n\n` for the untouched majority). This
  mixed state is cosmetic only.
- **Owner:** a dedicated **P5 housekeeping** one-shot (or fold into the
  P6/SYSTEMIC pass) — normalize every `_posts/*.md` to exactly one trailing
  `\n` in a single mechanical commit, with a guard added to the new-post
  workflow/linter (P5) so future posts stay normalized. Reviewers: treat a
  pre-existing `\n\n` EOF on a post whose P2 edit did not touch EOF as a
  documented NON-REGRESSION (per this note), not a defect.

## P6 — verify pre-existing comment-data fidelity (from P3 final review; non-blocking, NOT a P3 regression)

- **`82-techtalk-gamingforfreedom` comment 7236 renders its author "name" as
  a blog-post title** (`Mithro rants about stuff : OSDC & orbital death,
  better late then never…`) with the message being an excerpt. This is
  almost certainly a WordPress **pingback/trackback** (WP displays the
  linking post's title as the "author" — so this MAY be faithful to the
  original). This is PRE-EXISTING comment data (committed before P3; the
  comment-render fix merely made it visible — it was an empty shell before),
  NOT a P3 regression. P6 (or a comment-data verification pass) MUST check
  the live/Wayback original for these 6 long-standing comment posts and
  confirm each stored comment `name`/`message` is faithful (esp.
  pingbacks/trackbacks rendered the WP way; no scrape-mangled names). Only
  the 4 P3-recovered posts' comments (84/92) were oracle-verified verbatim
  in P3; the 6 pre-existing ones' comment DATA fidelity was out of P3 scope.

## P5 — comment-system follow-ups (from P3 comment-render fix; non-blocking)

- **`_includes/comments.html` assumes BOTH comment forms always exist.** P3
  confirmed Jekyll resolves `site.data.comments[slug]` to the per-comment
  DIRECTORY hash (the same-named `<slug>.yml` aggregate is shadowed). The
  fixed include (commit `8fe51c7`) iterates the dir-hash values + sorts by
  `date` ascending. If a FUTURE comment post is added with ONLY the `.yml`
  aggregate and no `<slug>/` dir, `site.data.comments[slug]` would be a LIST
  and the include would render zero comments. The P5 new-post/new-comment
  workflow MUST require creating BOTH forms (per design §1) — bake this into
  the scaffold/doc — OR make the include list-fallback-robust. (Spec §1
  already mandates both forms; this is a workflow-guardrail + doc item.)
- **Cosmetic (P6):** the comment-include's array-accumulation `{% assign %}`/
  `{% for %}` block emits ~2 blank lines of HTML whitespace before
  `<div class="comments-section">` (no visible/render defect; build clean).
  Optionally add `{%- -%}` whitespace-control in the P6 cosmetic pass.

## P5 — category-fidelity follow-ups (from M1/M2 code review; non-blocking)

- **Dead `_includes/category-feed.xml` has stale `/category/<slug>/` URLs
  (lines ~9–10).** It is NOT referenced by any layout/include (the live
  per-category feeds are the committed `category/<slug>/feed.xml` files,
  already migrated to `/archives/category/<slug>/feed/`). Harmless dead code
  now, but a latent trap if ever wired in, and it pollutes a repo-wide
  `/category/` grep. P5 cleanup: delete the dead include (or migrate its URLs
  if a reason to keep it emerges).
- **`category/<slug>/feed.xml` deliberately keeps `category:` front matter
  (NOT renamed to `cat_slug:`).** This is CORRECT: the reserved-word trap only
  breaks cross-page `site.pages | where: "category", …`; the feed body's
  same-page `page.category` read works fine. Documented here so a future
  editor does NOT "normalize" feed.xml to `cat_slug` and silently break the
  feed's post filter. (The `.md` pages use `cat_slug:` specifically to enable
  the cross-page title lookup in the 3 layouts.)
- **`cat_slug:` needs a one-line explanatory hint for the new-category
  workflow.** Adding a 20th category by copy-pasting a `category/*.md` works,
  but an editor may write `category:` (reserved → silently regresses the
  display name to the raw slug). P5 (which owns the new-post/new-content
  workflow + templates) should add a brief inline rationale (YAML comment in
  the category template, or doc in the workflow) noting WHY it's `cat_slug`
  not `category` (Jekyll reserves `category`/`categories` on pages, breaking
  `where: "category"` lookups — see M1/M2 commit `86d8ddb`).

## P5 polish — from P5-EXEC code review (Minor; non-blocking; bundle in a future polish pass)

1. **`scripts/fidelity/lint_content.py` line 42 comment is technically inaccurate** — claims the prefix prevents partial matches but `\b` also anchored at a word boundary (preventing `BLOCK_HTML_EXTRA` etc.). Harmless in practice (sentinel values are controlled). Reword to: `# \b removed — sentinel values are controlled; no corpus text matches BLOCK_HTML_* variants`.
2. **`tests/test_new_post.py` lines 10–18: dead `run_new_post()` helper** — defined but never called (all 5 tests use `subprocess.run` via the `post_env` fixture). Delete it.
3. **`docs/AUTHORING.md` §8 wording self-contradicts after P5-D** — says "you MUST create BOTH forms" then notes the `.yml` aggregate alone is sufficient (P5-D made the include list-fallback-robust). Reword §8 lead-in to: "If a post will have comments, create the aggregate `<id>-<slug>.yml`. The per-comment directory form is optional (the include handles both)."
4. **`scripts/new_post.py` `--slug` accepts spaces/uppercase without normalization** — silently produces broken filenames/permalinks. Add a guard rejecting `^[^a-z0-9-]` OR auto-normalize via `re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-")`. Add a test asserting the behavior.
5. **`.github/workflows/jekyll.yml` lint step assumes `uv` pre-installed** on ubuntu-latest (true since 2024). Self-documentation polish: pin a minimum runner version OR add an explicit setup step (`pip install uv` fallback) so the workflow is self-contained against future runner-image changes.

## PSL polish — from PSL-EXEC reviews (Minor; non-blocking; bundle in a future polish pass)

These are pre-existing or cosmetic items surfaced during PSL Phase 1/2/3 reviews. None block the PSL merge to `main`; capture them for a future housekeeping commit.

1. **Pre-existing trailing whitespace on 10 lines across 6 posts** — present at base commit `1679cf1`, NOT introduced by PSL. Affected: `2007-03-01-graphical-programming.md` lines 16,18,20,22,24; `2007-03-24-liferea-bug.md` line 16; `2008-03-18-gsoc2008.md` line 19; `2008-04-27-going-to-sydney.md` line 24; `2008-11-15-in-the-land-of-the-sheep.md` line 21; `2016-03-15-timvideos-us-and-google-summer-of-code-2016.md` line 21. Sweep + `sed -i 's/ *$//'` across `_posts/*.md` in a single commit; verify linter remains 0 (trailing whitespace is not a linter finding today but is hygiene).

2. **Pre-existing NBSP (U+00A0) inside body text** of `_posts/2014-07-29-hdmi2usb-production-board-bring-up-day-8-…-2014.md` line 20 (`Was\xc2\xa0able to view`) — present at base commit, preserved by Phase 2's re-indent. WordPress export artifact; replace with ASCII space if desired in the same housekeeping commit (but verify against the live oracle first — the NBSP may be intentional for line-break suppression).

3. **PSL Phase 3 fix commit (`96ecd0b`) Co-Authored-By trailer** says `Claude Sonnet 4.6` instead of the project-convention `Claude Opus 4.7 (1M context)`. Cosmetic; no functional impact. A future `git commit --amend` (on the local branch before push) OR a documentation note here closes the loop. **Recorded.**

4. **PSL Phase 2 commit subject lines >72 chars** (4 commits: `0e955ee` 82c, `34ff90c` 80c, `e6e3998` 75c, `32b0d27` 75c) — long slug names plus the `(B3)` classifier push them over the soft conventional 72-char guideline. Subjects are still readable; this is a cosmetic gap only. Future polish: when commit subjects must contain a long slug, drop the `(B3)` suffix (information is in the body) or use a shortened identifier.

5. **`scripts/fidelity/lint_content.py` `_BLOCK_HTML` pattern coverage gap: `<hr>`** (and `<hr/>`) is NOT flagged. A `<hr/>` survives in `_posts/2016-01-15-timvideos-us-2016-new-years-resolutions.md` line 22 (pre-existing; PSL preserved). Visually equivalent to `---` markdown, so usually harmless, but the linter should at least flag for review. Add `r"<hr\s*/?>"` to the pattern and either replace existing `<hr/>` instances with `---` or add a `<!-- fidelity-allow: BLOCK_HTML -->` sentinel.

6. **PSL/P6 accepted WP-artifact `<p>`-count tolerances** — Phase 2/3 commit bodies accept structural divergences that **legitimately need inline HTML per design §7** to fully reproduce. These are candidates for P6 USER-DECISION (restore via minimal `<HTML>` per §7, OR accept the divergence and document):
   - `epiphany2firefox`: oracle `<p style="text-align: center">` around a screenshot.
   - `hdmi2usb-day-4`: oracle `<p>&nbsp;</p>` spacer; oracle `<blockquote><p style="text-align: center">` image wrapper.
   - `hdmi2usb-snippets`: 4 oracle `<p>&nbsp;</p>` spacers between sections.
   - `hdmi2usb-day-5-6-7`: 3 oracle `<p>&nbsp;</p>` spacers.
   - `hdmi2usb-day-3`: post-PRE orphan `<ul><ul>` (oracle has nested `<ul>` without an enclosing `<li>` after the `<pre>` block — Markdown can't express this); also oracle's two separate `<ul>` blocks merge into one in the built rendering.
   - `fritzbox-vpnc`: final section wrapped in `<blockquote>` containing an `<h2>` + paragraphs (oracle); source uses standalone `## heading` (built renders as heading-not-quoted). NOTE: existing P6 USER-DECISION for `<pre><strong>` bold-in-code still pending separately.
   - `starhunter`: oracle has an empty `<div>` thumbnail wrapper (probably the linked-thumbnail tooltip case already in the P6 USER-DECISION list).

   For each, P6 visual signoff decides: accept the divergence (no change), or restore via minimal `<HTML>` per design §7 with a `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->` sentinel.
