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

## P1 — theme/structure fidelity & cleanup (from Task 2A)

- Remove orphaned dead code `_includes/category-feed.xml` (no callers; left in
  place by Task 2A per minimal-change constraint).
- Audit category-casing inconsistency: `category/<cat>.md` archive pages carry
  title-case `category:` (e.g. "Summer Of Code") while posts use slug
  `categories: [summer-of-code]`; the `category` layout filters on it. Static
  feed files correctly use the slug. Confirm archive pages list posts correctly
  and normalize casing.
