# P3 — Missing Posts Recovery: RESULTS & Handoff

**Status: COMPLETE.** P3 exit gate met (proof below). Branch
`migration-p3-missing-posts`, ready to merge to `main`.

**Regenerate the gate:** `uv run python -m scripts.fidelity.structure_check`
(6/6); `FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run` (build +
content linter); `uv run python -m pytest tests/ -q` (45). The 4 recovered
posts' permalinks resolve under `_site/archives/...`.

---

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| `_posts` count | 76 (was 72; +4 recovered) | **76** ✓ |
| 4 recovered posts present + WP permalinks resolve | yes | all 4 built at `_site/archives/{tp,tp,ubuntu,uncategorized}/{15,35,84,92}-…` ✓ |
| Content linter — recovered posts | 0 new findings | **0** in any of the 4 ✓ |
| Content linter — corpus | exactly 22 (P2 deferred R-P4), 0 BLOCK_HTML | **22** = 11 LIQUID_LEAK + 11 MISSING_IMAGE, **0 BLOCK_HTML** ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)** exit 0 ✓ |
| Hermetic suite (`tests/`) | green | **45 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | **PASS** ✓ |
| Comments (84, 92) | both `_data/comments/` forms + render | both forms present & verbatim; render chronologically ✓ |
| Working tree | clean | clean; 8 commits ahead of `main` |

## 2. What P3 did

- **T1 triage** (`P3-FINDINGS.md`): for WP ids 15/35/84/92 — all 4 live URLs
  return HTTP 500 (site root 200; the posts themselves error). Recovered
  article bodies from the **insurance captures** `exports/p3-missing-raw/*.html`
  (captured 2026-05-19; bodies complete, tails truncated). Comments for 84/92
  recovered from **Wayback**; 15/35 ship comment-less (15's Wayback comment had
  no body; 35 had no Wayback snapshot). Documented exact per-post metadata,
  target front-matter shape, comment both-forms schema, conversion pipeline.
- **4 posts recovered** as clean, faithful Markdown (each: fresh implementer →
  spec-compliance review → code-quality review; post 15 needed a smart-quote
  source-fidelity fix + re-review):
  - **15** `_posts/2007-02-23-tp-protocol-overview.md` — 3 (one nested) WP `<dl>`
    → kramdown definition lists (renders real `<dl><dt><dd>`, same proven
    approach as P2-R-B darcs).
  - **35** `_posts/2007-04-21-using-tailor-to-go-to-git.md` — 9-paragraph prose,
    12 links verbatim.
  - **84** `_posts/2008-07-08-my-three-weeks-on-a-mac.md` — 8 paragraphs, 5
    `<span style="font-weight:bold">` → `**bold**`; **+3 comments**.
  - **92** `_posts/2009-01-19-power-scripts-in-intrepid.md` — 2 WP-Syntax
    `<pre class="bash">` blocks reconstructed (spans/wrappers stripped,
    entities decoded, code byte-exact) → fenced ```` ```bash ````; `<i>`→`*`;
    title with real U+2026 `…`; **+3 comments** (paul/7212 had no author URL →
    `wordpress_url` set to post `#comment-7212` per spec §B3).
  - All 4: front matter in the exact **live-migrated corpus shape** (alphabetical
    keys, no `wayback_recovered`, single-quoted U+2019 excerpt), source stores
    the oracle's **UTF-8 smart quotes per-entity** (corpus convention, not ASCII
    — kramdown smartquotes is NOT relied on), faithful blank-line paragraph
    separation, **zero hardcoded structural HTML**, content-linter clean.
- **Comment-render defect FIXED (`8fe51c7`) — site-wide fidelity recovery.**
  Pre-existing P0/P1-era bug surfaced by P3's "comments must render" gate:
  `_data/comments/<slug>.yml` (list) and the same-named `<slug>/` dir collide;
  Jekyll deterministically exposes `site.data.comments[slug]` as the **directory
  hash** (the `.yml` aggregate is shadowed). The old `_includes/comments.html`
  did `{% for comment in comments %}` → iterated `[stem,obj]` pairs → **every
  author/date/message rendered EMPTY on all comment posts** (the "Comments (N)"
  count still showed). Fixed the include to read the dir-hash values and render
  them ordered by `date` ascending (the faithful original WordPress/Barthelme
  order — confirmed against the Wayback oracle for 94-reading-cookies-firefox).
  Verified across **all 8 comment posts** (6 long-standing + 84 + 92): real
  author/date/message, chronological, correct count. Both on-disk comment forms
  preserved per spec §1; markup/CSS unchanged.

## 3. Handoff (see `FOLLOWUPS.md`)

**P4 (baseurl/URL — unchanged from P2 handoff):** the 22 R-P4 relative_url
residuals → plain `/assets/…` after `baseurl:""`+CNAME; drive linter to 0;
re-resolve drifted line numbers. Plus the P2-flagged edge cases: `rcs-darcs`
hierarchical WP URL; `timvideos-us/hdmi2usb` sub-category; Scheme/Sydney/Tailor
categories; 404/search form-action. The 4 recovered posts have **no images**
(no new R-P4 added).

**P5 (new-post/comment workflow + build guard):** wire `lint_content` as the
build gate; **NEW comment-system guardrail** — the fixed include relies on BOTH
comment forms existing (a `.yml`-only future post would render zero comments);
the scaffold/doc MUST require creating both `_data/comments/<id>-<slug>.yml`
AND `_data/comments/<id>-<slug>/` (or make the include list-fallback-robust).
Plus the prior P5 items (EOF normalization, dead `_includes/category-feed.xml`,
`cat_slug` rationale, Task-L linter polish).

**P6 (visual / MANDATORY user signoff — unchanged):** the HIGH systemic
flat-list/paragraph-structure pass (NOTE: the 4 P3 posts were authored
structurally-faithful from the start, so they do NOT add to that debt — only
the 72 originally-migrated posts need it); fritzbox bold-in-code user signoff;
CSS micro-deltas; comment-include whitespace cosmetic; the R-E region-3 fence
nit; nav-below clearfix; Picasa byte-fidelity.

## 4. Notes / data artifacts

- All 4 posts sourced from `exports/p3-missing-raw/*.html` (committed insurance
  captures); comments for 84/92 from Wayback. The live posts themselves remain
  HTTP 500 on the restored site (only the bodies were ever recoverable — the
  insurance captures + Wayback were essential; design §13's "live never fully
  restored" risk partially materialized and the documented fallback worked).
- `docs/superpowers/plans/P3-FINDINGS.md` is the authoritative recovery-data
  keystone. `tmp/p3/` holds the scrape/extract scratch (gitignored;
  regenerable). `FOLLOWUPS.md` remains the authoritative cross-phase backlog.
