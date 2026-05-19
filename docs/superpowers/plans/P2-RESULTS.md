# P2 — Content Fidelity: RESULTS & Handoff

**Status: COMPLETE.** P2 exit gate met (proof below). Branch
`migration-p2-content-fidelity`, ready to merge to `main`.

**Regenerate the gate:** `FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run`
(build + content linter) and `uv run python -m scripts.fidelity.structure_check`
(structural 6/6); hermetic suite `uv run python -m pytest tests/ -q`.

---

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| `bundle3.3 exec jekyll build` | clean | **PASS** (clean) |
| Content linter over `_posts/*.md` | exactly 22, **0 BLOCK_HTML**, 1 N sentinel-suppressed | **22** = 11 `LIQUID_LEAK` + 11 `MISSING_IMAGE`, **0 `BLOCK_HTML`** ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)**, exit 0 |
| Hermetic test suite (`tests/`) | green | **45 passed** |
| Working tree | clean | clean; 32 commits ahead of `main` |

The 22 residuals are EXACTLY the P4-COUPLED `relative_url` set predicted by
`P2-FINDINGS.md` §4 — 11 `LIQUID_LEAK` + 11 co-located `MISSING_IMAGE`
artifacts across 8 posts: `2007-05-09-almost-there`, `2007-08-17-resume`,
`2008-02-04-google-patchwork`, `2008-02-18-cfxs-free`,
`2009-05-26-starhunter…`, `2013-10-06-…fritzbox…vpnc`,
`2014-07-25-hdmi2usb…day-4`, `2015-07-05-first-v2-hdmi2usb…`. They are VALID
WORKING Liquid today (correct under `baseurl:"/blog.mithis.net"`); converting
to plain `/assets/…` is only correct+faithful once **P4** sets `baseurl:""`.
**P4 owns these 22** (relurl→plain conversion + final linter-0).

## 2. What P2 did

- **T1 triage** (`P2-FINDINGS.md`): regenerated & classified the authoritative
  47-finding worklist (24 R + 1 N P2-NOW; 22 R-P4 deferred). Containment +
  classification model made the remediation a *provable* countdown.
- **Task L** (`lint_content.py`): TDD `fidelity-allow` sentinel allowance
  (BLOCK_HTML-only, per-occurrence, no blanket weakening); +5 tests.
- **R-A**: removed the Jekyll-injected comment-CSS `<style>` block from 6
  posts (non-original; commit 8a6c3f9 artifact). −12 BLOCK_HTML.
- **R-B**: darcs mangled `<dl>` → kramdown definition list (renders identical
  `<dl><dt>×3<dd>×3</dl>`). −1.
- **R-C**: cfxs-free stray `</pre>`+blockquote → fenced code + prose. −1.
- **R-D**: hdmi2usb day-2/3/5 — deleted mangled `</li> /li>` raw-HTML closers
  + reconstructed `<pre>` error dumps as fenced blocks, oracle-byte-verbatim
  (incl. nbsp / leading-space fidelity). −6.
- **R-E**: fritzbox 4× raw `<pre>` (bare-backtick delimiters, concatenated
  `</pre>`+backtick, `> ` artifact) → 4 fenced blocks, oracle-byte-verbatim.
  −4. (Embedded `<strong>` necessarily lost — see §3.)
- **R-F**: techtalk YouTube `<object><embed>` kept byte-identical (necessary
  HTML) + `fidelity-allow` sentinel → the 1 N suppressed. Corpus → **22**.
- **M1+M2** (oracle-driven, `P2-M1M2-FINDINGS.md`): reconciled category URL
  space to the faithful `/archives/category/<slug>/` (live-oracle confirmed;
  baseurl-independent) across 19 `category/*.md` + 19 `feed.xml` + 3 layouts +
  sidebar + navigation; restored the real WP `category_description()` as
  `description:` front matter (5 non-empty + rcs-darcs; verbatim oracle incl.
  `ideas` U+2019) and removed 8 invented Jekyll-era body-prose blocks; fixed 4
  faithful titles (lca→linux.conf.au, sci-fi→"Sci Fi", tp→Thousand Parsec,
  rcs-darcs→darcs); one consistent display rule = the category page's
  faithful `title:` via a `cat_slug` page-lookup (the reserved-`category`
  Jekyll trap was found in review and fixed). One minimal harness path
  update (`structure_check.py` category archetype → new URL; gate NOT
  weakened, its tests green).

Every task ran fresh-implementer → spec-compliance review → code-quality
review; the M1/M2 spec review caught a real runtime lookup failure + a
byte-fidelity miss, both fixed and re-reviewed ✅.

## 3. Handoff — what later phases MUST pick up (see `FOLLOWUPS.md`)

**P3 (missing posts):** site is up; 4 missing posts already captured to
`exports/p3-missing-raw/{15,35,84,92}.html` (HTTP 500 but full themed
article). Proceed.

**P4 (baseurl/URL — owns these):**
- The 22 R-P4: replace `{{…|relative_url}}` with plain `/assets/…` after
  `baseurl:""`+CNAME; drive the linter to 0; re-resolve the P4-COUPLED line
  numbers (they drifted as P2 edited posts — re-run the linter fresh).
- `rcs-darcs` hierarchical WP URL (`/archives/rcs/darcs`, original 404s the
  flat slug) — redirect/permalink decision.
- `timvideos-us/hdmi2usb` sub-category (live posts link it; absent in Jekyll)
  — create page + restore post `categories:` membership.
- Scheme/Sydney/Tailor categories not migrated — decide.
- Pre-existing 404/search form-action items.

**P6 (visual / MANDATORY user signoff):**
- **HIGH — systemic flat-list/paragraph structure:** WP→MD export flattened
  ALL list nesting + dropped blank-line paragraph separators corpus-wide, so
  kramdown renders structures that diverge from the original (merged `<p>`,
  flattened nesting, absorbed list-breaks). NOT linter-detectable, NOT in the
  47, deliberately out of P2 scope — needs a **dedicated systemic
  content-structure pass** (own brainstorm→spec→plan) before/within P6,
  gated by a live-oracle structural diff. Do not lose this.
- **MANDATORY user signoff — fritzbox bold-in-code:** the 4 fritzbox code
  blocks lost their embedded `<strong>` emphasis (Markdown code is literal;
  no-hardcoded-HTML constraint). Approved per §3.4 but a real user-visible
  reduction — show before/after, get explicit accept-or-alternative.
- CSS micro-deltas; the R-E region-3 cosmetic fence nit; nav-below clearfix;
  Picasa byte-fidelity.

**P5 (new-post workflow + linter build-guard):** wire `lint_content` as the
build gate; Task-L polish (redundant `\b`, i==0 test, docstring); corpus-wide
EOF `\n\n`→`\n` normalization; delete dead `_includes/category-feed.xml`;
document why `feed.xml` keeps `category:` while `.md` use `cat_slug`; add a
`cat_slug` rationale hint to the new-category template/workflow.

## 4. Cross-phase data artifacts (kept)

`docs/superpowers/plans/P2-FINDINGS.md` (remediation triage keystone),
`P2-M1M2-FINDINGS.md` (category-fidelity oracle data + worklist),
`FOLLOWUPS.md` (accumulated backlog, authoritative). Scraped oracle HTML in
`tmp/p2-oracle/` is gitignored scratch (regenerate via `curl -sk` against the
live original; TLS cert expired → verify-disabled is expected).
