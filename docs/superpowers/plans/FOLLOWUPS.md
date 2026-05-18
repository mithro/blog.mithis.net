# Cross-phase follow-ups (accumulated during P0 execution)

Living list of items discovered while executing the P0 plan that are deliberately
deferred to a later phase (out of P0 scope). Task 13 folds this into P0-RESULTS.md
and the P1/P2/P5 plans. Do NOT action these during P0 unless a P0 task explicitly
covers them.

## P2 — content remediation worklist (from Task 5 linter smoke run)

`scripts/fidelity/lint_content.py` over `_posts/*.md` (asset_root='.') → **47 findings**:
- `BLOCK_HTML`: 25 — hardcoded structural HTML in posts to convert to Markdown.
- `LIQUID_LEAK`: 11 — unrendered `{{`/`{%` committed into post content.
- `MISSING_IMAGE`: 11 — several are `{{ ` artifacts secondary to LIQUID_LEAK
  (they disappear once the Liquid leaks are fixed); the rest are genuinely
  missing local images.
(Task 13 regenerates the exact authoritative list grouped by code and by post.)

## P5 — prerequisites before wiring `lint_content` as the build gate

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
  a conscious limitation; make it explicit in-code for P5 gate users).
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

`#post-0` was de-listed in P1-T7 (commit `a40770a` area; resolved under the
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
