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
