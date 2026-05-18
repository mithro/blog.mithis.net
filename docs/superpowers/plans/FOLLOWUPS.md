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
