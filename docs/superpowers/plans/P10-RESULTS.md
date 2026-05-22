# P10 — Exhaustive Structural Remediation: RESULTS & Handoff

**Status: COMPLETE.** P10 exit gate met (§1). Branch
`migration-p10-structural-remediation`, merged to `main`.

## Why P10 happened (and why the prior "100% fidelity" claim was premature)

After P9, I claimed "no known visual delta remains" based on **representative
sampling** (~20 posts/page-types). The resilience loop kept pushing for
"verified 100% fidelity", so I ran an **exhaustive automated all-76-post
structural diff** (built `_site` entry-content vs live blog.mithis.net,
tag-count comparison). It found **22 posts with real deltas** that the
sampling had missed — because I'd happened to check the posts already fixed
in P6–P9, not the un-audited remainder.

**Key lesson: representative sampling is not verification.** PSL fixed
paragraph/list structure for ~34 posts via a *sample-based* audit, but was
INCOMPLETE — ~11 more posts still had paragraph-merging, plus
`eagle-for-pcb` had its entire body wrongly wrapped in a ``` code fence.
Only the exhaustive automated diff caught these.

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| Content linter (CLI, CI-enforced) | 0 | **PASS (0)** ✓ |
| `structure_check` | 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **56 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean ✓ |
| `_posts` count | 76 | **76** ✓ |
| All-76 structural diff (built vs live) | exact match modulo documented artifacts | **69/76 exact + 7 documented WP-artifacts** ✓ |
| Typography (smart-quotes/NBSP) | byte-faithful to pre-P10 | **0 drift** across 17 touched posts ✓ |
| Word content | identical to pre-P10 (only structure + oracle-faithful image/emoji restoration) | verified ✓ |

## 2. What P10 did (3 commits)

- **`f1cc20f`** — fixed structural deltas in 16 posts: paragraph-merging
  (blank-line restoration, PSL B1 recipe for the ~11 posts PSL missed),
  blockquote-wrapped-code restoration (utf-8-in-python, power-scripts,
  using-identitiesonly — live wraps these code samples in `<blockquote>`),
  and the **eagle-for-pcb body-fence bug** (whole body was wrongly ```
  fenced → unfenced into image + paragraphs + bullet list).
- **`b646ab6`** — restored the body images in eagle-for-pcb + eagle2geda
  (the migration had converted `<img>` → empty `[](url)` links; restored
  to `![alt](url)` with the **exact alt text from live**: "PCB Board for
  my Honors Project" / "Component in Eagle and gschem"). Also 79-going-to-
  sydney: `;)` → `😉` (matching live's emoji rendering).
- **`061e262`** — **typography-restoration fix.** The structural edits had
  silently stripped smart-quotes (U+2019/U+201C/U+201D) → ASCII and NBSP →
  space on 4 posts (the recurring edit-tool bug, same as PSL Phase 3).
  Restored from pre-P10 bytes (difflib alignment + 3 manual fixes for
  lines structurally altered beyond typography). Verified 0 drift.

### Content-change verification (all oracle-faithful)
Every non-structural change was verified against the live cache
(`tmp/verify-all/live/<wid>.html`): eagle/eagle2geda image alt text MATCHES
live; going-to-sydney emoji MATCHES live; utf-8/power-scripts/identitiesonly
blockquote-wrapped-code MATCHES live's `<blockquote><pre>` structure. No
fabricated content.

## 3. The 7 remaining deltas — all genuine Markdown-inexpressible WP artifacts

These cannot be reproduced in kramdown Markdown without raw HTML (and per
"broken stuff and all" + the §7 sentinel discipline, are accepted):

| Post | Delta | Why accepted |
|---|---|---|
| 6-gnome-improvements | p:14/9 | WP mixed loose-list wrapping (first `<li>` raw, others with nested `<p>`); kramdown loose/tight is all-or-nothing per list |
| 23-eagle2geda | p:1/0 | live wraps body text in a layout `<table><td>` (no `<p>`); built renders a normal `<p>` |
| 82-techtalk | p:6/7 | live wraps the Flash `<object>` in a `<p>`; kramdown treats raw-HTML block as block-level (no `<p>`) |
| 102-starhunter | p:5/4 | the §7 `fidelity-allow` `<div>` float-wrapper (P6 B-9) adds one `<p>` |
| 1980-hdmi2usb-snippets | p:2/6 | 4× WP `<p>&nbsp;</p>` spacers between sections |
| 1993-hdmi2usb-day-3 | ul:13/15 | post-PRE orphan `<ul><ul>` (known PSL-accepted; Markdown can't express `<ul>` without enclosing `<li>`) |
| 2003-hdmi2usb-day-5-6-7 | p:2/4 | 2× WP `<p>&nbsp;</p>` spacers |

## 4. The verification tool (reusable)

`tmp/verify-all/compare2.py` (+ a curl loop over `_posts` permalinks into
`tmp/verify-all/live/`) performs the all-76 built-vs-live entry-content
structural diff. It slices `entry-content` to the first footer/comments
boundary marker and compares p/ul/ol/li/img/blockquote/pre/h2-h4 counts.
Re-run after any future content/template change to catch structural
regressions. (Not a CI gate — requires network/live; manual diligence.)

## 5. Cumulative project state (P0 → P10)

- Content + tags + structure + comments + URLs (P0–P8) — intact.
- **Per-post structural fidelity (P10)** — 69/76 exact vs live; 7 documented
  Markdown-inexpressible WP-artifacts; eagle body-fence bug fixed; ~11
  PSL-missed paragraph-merging posts fixed; body images restored.
- Rendered visual fidelity (P7–P9) — header/sidebar/widgets/categories/
  dates/code-colors/tag-slugs/highslide all match live.
- Authoring workflow + CI build-guard (P5) — intact.
- **Only remaining work: the user's DNS cutover** (not to be suggested
  until the user confirms satisfaction).

## 6. P10 gate — independent re-verification

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # 0
uv run python -m scripts.fidelity.structure_check                      # 6/6
uv run python -m pytest tests/ -q                                      # 56
bundle3.3 exec jekyll build                                            # clean
ls _posts/*.md | wc -l                                                 # 76
# Exhaustive structural fidelity: re-run tmp/verify-all (curl + compare2.py)
#   → 69/76 exact + 7 documented artifacts
```
