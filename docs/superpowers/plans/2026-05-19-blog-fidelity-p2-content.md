# Blog Fidelity P2 — Content Fidelity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax. Before claiming P2 done: use @superpowers:verification-before-completion.

**Goal:** Make every migrated post faithful, clean content — drive `lint_content` to zero *remediable* findings across `_posts/*.md` (hardcoded structural HTML → Markdown, 1 N handled per-case) WITHOUT corrupting legitimate content, and reconcile broken category internal-links. The 22 R-P4 LIQUID_LEAK/MISSING_IMAGE findings are deliberately excluded from P2 scope (baseurl-coupled; see P2-FINDINGS.md §3.1 and P4-COUPLED set) and will remain in the linter output until P4.

**Architecture:** Data-driven, mirroring P0/P1. Keystone triage task re-runs the P0 `lint_content` over `_posts/`, classifies every finding (REAL defect vs faithful-content false-positive vs necessary-HTML vs P4-COUPLED-deferred) against the original post as the fidelity oracle, and records `P2-FINDINGS.md`. Remediation tasks (grouped by finding-class) then fix the 25 P2-NOW findings (24 R BLOCK_HTML + 1 N) to faithful Markdown/per-case, leaving the 22 R-P4 findings untouched. Gate: linter shows only the expected 22 P4-coupled residuals AND structural fidelity (P1) + clean build NOT regressed.

**Tech Stack:** P0 harness (`scripts/fidelity/lint_content.py`, `structure_check.py`, `build.py`) via `uv`; Jekyll 4.4 (`bundle3.3`); kramdown/GFM; `curl -k`/Wayback for the original-content fidelity oracle.

**Spec:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md` (§5 P2, §7 content-fidelity strategy, the "no hardcoded structural HTML" rule)
**Inputs:** `docs/superpowers/plans/FOLLOWUPS.md` (the P2 worklist, M1 category-links/casing, M2 category-prose, the P5 linter-FP classes), `P1-RESULTS.md`, `P0-RESULTS.md`. Fidelity oracle: original posts at `https://blog.mithis.net/...` (live, **TLS cert expired → fetch with verification disabled**), `exports/p3-missing-raw/` (not relevant to P2's 72 posts), Wayback fallback.

**Local env:** no `bundle` → `bundle3.3`. `uv` on PATH. Work from the P2 worktree root. Inline `python -c` hook-blocked; use Python scripts in `tmp/` (gitignored; delete after) — NOT multi-statement shell loops. P2 EDITS `_posts/*.md` (that is the point — unlike P1), but ONLY the P2-NOW posts (BLOCK_HTML / N). P2 must NOT edit the LIQUID_LEAK/MISSING_IMAGE lines — see P4-COUPLED constraint below.

**P2 EXIT GATE (precise):** `uv run python -c`-free reproduction: `lint_content` over all `_posts/*.md` (asset_root = repo root) reports **exactly 22 findings** — only the explicitly P4-COUPLED `LIQUID_LEAK`/`MISSING_IMAGE` findings (the 11 LIQUID_LEAK + 11 co-located MISSING_IMAGE across ~8 posts). Zero of the 24 R BLOCK_HTML findings remain; the 1 N (`techtalk-gamingforfreedom:22`) is resolved per-case with a justified linter-allowance. **The remaining 22 R-P4 findings are P4's responsibility; P2 does not touch the `relative_url` post lines (touching them now would break image URLs under the current `baseurl:"/blog.mithis.net"` — kramdown does NOT prepend baseurl to Markdown image paths, so plain `/assets/x` would render without the baseurl prefix on the current deployment).** AND `structure_check` still `PASS (6/6)` (content edits must not regress P1). AND `bundle3.3 exec jekyll build` clean (0). AND full unit suite green. AND a spot-check sample of the P2-NOW remediated posts renders faithfully vs the original site (same structure/lists/code; no mangled HTML).

---

## File Structure

Created:
- `docs/superpowers/plans/P2-FINDINGS.md` — the triaged authoritative worklist (keystone output).
- `docs/superpowers/plans/P2-RESULTS.md` — P2 handoff.

Modified during remediation (data-driven by P2-FINDINGS.md):
- `_posts/*.md` — ONLY the posts with real defects / FP-normalizable examples (faithful edits; preserve rendered meaning vs original WordPress).
- Possibly `assets/images/...` (+ post image paths) — for genuinely MISSING_IMAGE findings.
- Possibly `scripts/fidelity/lint_content.py` + `tests/fidelity/test_lint_content.py` — ONLY a minimal, TDD'd refinement for a proven linter FP class (e.g. ignore Liquid inside single-backtick inline code), if triage proves content is correct and normalization isn't faithful. Advances the FOLLOWUPS P5 linter-hardening too.
- `_layouts/home.html` (+ `post.html`/`category.html` as needed) — M1 internal category-link URL-space + casing reconciliation (templates, not posts).
- Category `.md` front matter — ONLY if M2 decides to preserve category prose via `description:`.

**Faithfulness oracle (used by triage + remediation):** for any finding where the *intended* content is ambiguous, fetch the original rendered post: `https://blog.mithis.net/archives/<cat>/<id>-<slug>` via a Python `urllib` fetch with an unverified SSL context (cert expired) — compare the post's intended body/structure. If the live post 500s or is unreachable, fall back to Wayback (`scripts/fidelity/wayback.py`) then the git history of the post. A remediation is faithful iff the post's RENDERED `_site` HTML conveys the same content/structure the original showed (Liquid leaks rendering literal `{{…}}`, missing images, and mangled list/HTML are self-evidently NOT faithful → fixing them restores fidelity).

---

## Task 1: Triage — regenerate & classify the authoritative finding list (keystone; drives all remediation)

**Files:** Create `docs/superpowers/plans/P2-FINDINGS.md`

- [ ] **Step 1: Regenerate the authoritative linter output**

Write `tmp/p2_lint.py` (gitignored; delete after):
```python
from scripts.fidelity.lint_content import lint_paths
import glob, collections
fs = lint_paths(sorted(glob.glob('_posts/*.md')), asset_root='.')
print(len(fs), 'findings')
print(collections.Counter(f.code for f in fs))
for f in fs:
    print(f"{f.path}:{f.line} [{f.code}] {f.message}")
```
Run `uv run python tmp/p2_lint.py` from the worktree root; capture the FULL output; delete the script. This is the authoritative current list (supersedes the P0-era count of 47 if it has drifted).

- [ ] **Step 2: Classify every finding**

For EACH finding determine its class by reading the post around that line AND (where intent is ambiguous) consulting the fidelity oracle (fetch the original rendered post — live `https://blog.mithis.net/archives/<cat>/<id>-<slug>` with SSL verification disabled via a `tmp/` Python `urllib` script; Wayback/git fallback). Classes:
  - **R (real defect):** genuine hardcoded structural/block HTML left by the WP→MD conversion that kramdown/GFM can express as Markdown; OR a genuine unrendered Liquid leak (`{{ }}`/`{% %}` that was never meant to be literal text — confirm it renders as literal junk vs the original); OR a genuinely missing/broken image (file absent under `assets/`, or wrong path).
  - **F (false-positive — faithful code example):** the post is *demonstrating* HTML/Liquid; the content is correct; the linter over-flags because it's in inline-code or a 4-space-indented block. Sub-decide: **F-norm** = faithfully normalizable to a fenced ```` ``` ```` code block (the modern idiom; renders as a code block; linter correctly skips fences) — preferred; **F-lint** = genuinely the linter's fault and normalization would NOT be faithful (e.g. inline `` `{{x}}` `` mid-sentence) → requires the minimal linter refinement.
  - **N (necessary HTML):** real block-level HTML that Markdown genuinely cannot express faithfully (a real data table the original rendered as a table, an embed/iframe). Rare. Decide per-case: convert to a kramdown-supported form if faithful, else justified linter-allowance.

- [ ] **Step 3: Write `docs/superpowers/plans/P2-FINDINGS.md`**

A table: `path:line | code | class (R / F-norm / F-lint / N) | original-content evidence (oracle) | planned remediation`. Group a remediation-task plan: by file is usually cleanest (one commit per post fixes all that post's findings). Tally R/F-norm/F-lint/N counts. This is the authoritative, data-driven remediation worklist for Tasks 2+.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/P2-FINDINGS.md
git -c commit.gpgsign=false commit -m "P2: triage & classify the authoritative content-finding worklist

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Tasks 2…N: Remediate — data-driven by P2-FINDINGS.md (controller dispatches per file/group)

**P2 scope: P2-NOW findings ONLY (25 total: 24 R BLOCK_HTML + 1 N).** The 22 R-P4 LIQUID_LEAK/MISSING_IMAGE findings are OUT OF P2 SCOPE — owned by P4, do not touch.

**Each task = one post (or a small group of closely-related posts) with all its P2-NOW findings.** Same protocol per task:

- [ ] **Step 1: Read** the post + its P2-FINDINGS §"P2-NOW" rows + the oracle evidence for that post. Verify: does this post also have P4-COUPLED rows? If yes, leave those lines EXACTLY as-is; only edit the BLOCK_HTML lines.
- [ ] **Step 2: Remediate faithfully** per class (P2-NOW only):
  - **R block-HTML:** convert to equivalent Markdown (kramdown/GFM). The rendered `_site` HTML for that post must convey the same structure/content the original showed (lists→`-`/`1.`, emphasis, links, headings, blockquotes, pre/code→fenced). Keep genuinely-inline HTML the linter allows where Markdown can't express it.
  - **N (necessary HTML):** do NOT mangle the post. The resolution is a per-case justified linter-allowance (the only N is `techtalk-gamingforfreedom:22` — Flash embed; see P2-FINDINGS §3.7).
  - **R-P4 (LIQUID_LEAK / MISSING_IMAGE):** DO NOT TOUCH. These are valid working Liquid today. Editing them under the current `baseurl:"/blog.mithis.net"` would break image URLs on the live deployment.
  - NEVER change the post's meaning vs the original; preserve front matter, permalink, dates, categories.
- [ ] **Step 3: Verify** — re-run the linter for THIS post → its P2-NOW BLOCK_HTML findings gone (0 BLOCK_HTML for this file; any LIQUID_LEAK/MISSING_IMAGE rows remain as expected); `bundle3.3 exec jekyll build --trace 2>&1 | grep -ciE "error|warning|deprecation|conflict"` → 0; `uv run python -m scripts.fidelity.structure_check` → still `PASS (6/6)` (content edits must not regress P1); spot-compare the post's rendered `_site` output against the oracle (same headings/list items/links/text — no mangled HTML).
- [ ] **Step 4: Commit** that post/group:
```bash
git add _posts/<file>.md [assets/...]
git -c commit.gpgsign=false commit -m "P2: content fidelity — <post> (<R/N summary>)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```
**Exit per task:** that post's BLOCK_HTML/N linter findings = 0; any LIQUID_LEAK/MISSING_IMAGE rows remain (correct); build clean; structure_check 6/6; rendered output faithful to the original; only that post changed; zero front-matter/permalink drift.

---

## Task L (only if triage finds F-lint/N): minimal `lint_content` FP refinement (TDD)

Use @superpowers:test-driven-development. ONLY if P2-FINDINGS has F-lint/N rows that cannot be faithfully content-normalized.

**Files:** `scripts/fidelity/lint_content.py`, `tests/fidelity/test_lint_content.py`

- [ ] Add a failing test encoding the proven FP (e.g. `lint_text` must NOT flag `{{ x }}` inside single-backtick inline code; or must not flag block HTML inside a 4-space-indented code block). Run → fails.
- [ ] Implement the minimal rule refinement (strip/ignore inline-code spans before the Liquid scan; treat 4-space-indented runs like fenced blocks) — keep all existing `test_lint_content.py` assertions green (real defects still flagged). This also advances the FOLLOWUPS P5 linter-hardening (note it there as partially-resolved).
- [ ] Run full `uv run pytest -m "not integration" -q` → all pass. Re-run the post-corpus linter → the F-lint findings are gone WITHOUT having touched those posts. Commit (`scripts/fidelity/lint_content.py` + test only).

---

## Task M1: Reconcile broken category internal-links + casing (templates, not posts)

**Files:** `_layouts/home.html` (+ `_layouts/post.html`/`_layouts/category.html` if they diverge)

- [ ] **Step 1:** Confirm the bug (FOLLOWUPS M1): `_layouts/home.html` links post categories to `/archives/category/<slug>` which does NOT exist in `_site` (categories build at `/category/<slug>/`); display casing diverges (`| title` vs `| capitalize` vs raw) across home/post/category.
- [ ] **Step 2:** Reconcile ALL category links across home/post/category to the single real URL space `{{ '/category/' | append: <slug> | relative_url }}` resolving to `/category/<slug>/`, and ONE consistent display rule (match what Barthelme/the category page shows for the category name — pick the rule the category archetype already uses and apply it uniformly; faithful to the original).
- [ ] **Step 3:** Build; verify in `_site` that home/post category links resolve to existing `/category/<slug>/` pages (no `/archives/category/` 404s); `structure_check` still `PASS (6/6)`; build clean; suite green. Commit (templates only; zero `_posts` edits in this task).

---

## Task M2: Category descriptive-prose decision

**Files:** `docs/superpowers/plans/P2-RESULTS.md` (decision record) [+ category `*.md` front matter ONLY if "preserve" chosen]

- [ ] **Step 1:** Determine via the oracle whether the original WordPress category pages displayed a description. Barthelme `archive.php` only renders WP `category_description()`. If the original site shows NO per-category description text → the faithful choice is **keep dropped** (the Jekyll-era `.md` body prose was a non-Barthelme addition); record the decision + rationale in P2-RESULTS, no content change. If the original DID show category descriptions → move the `.md` body prose into `description:` front matter so `category.html`'s `div.archive-meta` renders it (faithful), build, verify, commit.
- [ ] **Step 2:** Record the decision + evidence in P2-RESULTS.md.

---

## Task Z: P2 exit gate + handoff to P3

Use @superpowers:verification-before-completion.

- [ ] **Step 1: Full P2 gate.** Regenerate the linter over `_posts/*.md` (asset_root=`.`) → **exactly 22 findings** (only the P4-COUPLED LIQUID_LEAK/MISSING_IMAGE residuals; zero BLOCK_HTML). `uv run python -m scripts.fidelity.structure_check` → `PASS (6/6)`. `bundle3.3 exec jekyll build --trace 2>&1 | grep -ciE "error|warning|deprecation|conflict"` → 0. `uv run pytest -m "not integration" -q` → all pass. Spot-check ≥5 P2-NOW remediated posts: rendered `_site` HTML faithful vs the original site (no mangled HTML, lists/code/structure equivalent). Paste evidence. Confirm: the 22 residual findings are all `LIQUID_LEAK`/`MISSING_IMAGE` in the ~8 posts listed under "P4-COUPLED" in P2-FINDINGS §6 — this is expected and correct by design.
- [ ] **Step 2: Write `docs/superpowers/plans/P2-RESULTS.md`** — findings triaged (R-now/R-P4/N tallies: 25 P2-NOW [24 R + 1 N] + 22 R-P4 deferred), what was remediated in P2, the M1 fix, the M2 decision, confirmation P1 structural fidelity not regressed, the 22 R-P4 findings explicitly called out as P4's responsibility, P3 readiness (the 4 captured posts in `exports/p3-missing-raw/`). Commit.
- [ ] **Step 3: Stop and re-plan.** Do NOT start P3 ad hoc. Return to @superpowers:writing-plans for the **P3** plan (recover the 4 captured missing posts → faithful Markdown matching existing post format + dual comment representation), then P4 (domain/`baseurl=""`+CNAME + strip the 22 R-P4 LIQUID_LEAK residuals → plain `/assets/…` + final linter-0 gate), P5 (new-post workflow + wire `lint_content` as build-guard + the FOLLOWUPS gate/linter hardening), P6 (visual + functional acceptance + user signoff).

---

## Subsequent plans (scope note — NOT this plan)

P3 missing-post recovery (source already captured/de-risked), P4 domain/`baseurl=""`/CNAME + form-action fixes, P5 new-post workflow + linter-as-build-guard + accumulated gate/linter hardening, P6 visual pixel sweep + functional sweep + CSS-micro-delta audit + Picasa decision + user signoff. Each is its own data-driven spec→plan→subagent-execute→merge cycle. The FOLLOWUPS backlog carries all deferred items.
