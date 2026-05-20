# P5 — New-Post Workflow + Linter Build-Guard + Housekeeping: RESULTS & Handoff

**Status: COMPLETE.** P5 exit gate met (§1). Branch
`migration-p5-newpost-workflow`, ready to merge to `main`.

P5 makes future content adherence enforceable: a documented authoring
workflow, a scaffold that emits a linter-clean post, and a CI build-time
guard that fails the build/deploy on any future structural-HTML violation
in `_posts/`. Plus the rolled-up housekeeping items from the cross-phase
FOLLOWUPS backlog.

**Regenerate the gate:** `uv run python -m scripts.fidelity.lint_content _posts
--asset-root .` (now functional → exit 0 / no output on clean corpus, exit 1
+ printed findings on any violation); `uv run python -m
scripts.fidelity.structure_check` (6/6); `uv run python -m pytest tests/ -q`
(54).

---

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| Content linter (via CLI) | 0 findings | **PASS (0)** + no output ✓ |
| Linter CLI exit code on violations | non-zero | **proven: tmp `<div>` post → exit 1** ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)** exit 0 ✓ |
| Hermetic suite | green | **54 passed** (45 + 5 new_post + 2 lint_content polish + 2 CLI smoke) ✓ |
| Build | clean | **PASS** ✓ |
| `_posts` count | 76 | **76** ✓ |
| CI build-guard wired & functional | step before `Build with Jekyll` | line 45 of `jekyll.yml`, exact run cmd ✓ |
| AUTHORING.md present | documented workflow | `docs/AUTHORING.md` ✓ |
| Scaffold script present | `scripts/new_post.py` produces lint-clean post | ✓ |
| Sample template | not in `_posts/` | `docs/sample-new-post.md` (corpus stays 76) ✓ |
| Working tree | clean | clean; 12 commits ahead of `main` |

## 2. What P5 did (10 commits per the §D sequence)

- **P5-A `5e87195` — lint_content polish:** dropped redundant `\b`, added a
  fence-predecessor comment, expanded module docstring (documents the
  `fidelity-allow` sentinel and UNCLOSED_FENCE), added the `i==0`
  negative-index guard test, **added the UNCLOSED_FENCE detection** (catches
  posts ending with an unclosed fenced block).
- **P5-B `d25dd99` — EOF normalization:** 6 posts that ended with `\n\n`
  normalized to a single `\n`.
- **P5-C `3efbab2` — dead `_includes/category-feed.xml` removed** (no
  callers anywhere; pre-FOLLOWUPS-documented).
- **P5-D `40cee4b` — `_includes/comments.html` list-fallback-robust:** the
  include now handles BOTH the dir-hash form (current both-forms reality;
  P3 fix) AND a `.yml`-only future post (the `comments.first[0]` hash-vs-list
  discriminator). Also: a deferred-dynamic-count Liquid recipe comment in
  `_includes/sidebar.html` per the controller decision C-1 to keep static
  integers (PSC made them all oracle-correct; dynamic is robustness, not
  faithfulness — file under future cosmetic polish).
- **P5-E `d4a9efd` — `docs/AUTHORING.md` (the authoring doc):** front-matter
  variants (10-key WP-imported vs 7-key new-post), 22+1 category table,
  UTF-8 smart-quote convention, image `/assets/images/…` plain paths,
  no-block-HTML rule + `fidelity-allow` sentinel exception, both-forms
  comment data, new-category workflow + `cat_slug` rationale, feed.xml vs
  category.html parallel-convention note, pre-commit checklist.
- **P5-F `d7a75a0` — `scripts/new_post.py` scaffold:** stdlib-only Python
  CLI; emits `_posts/YYYY-MM-DD-<slug>.md` with the correct 7-key new-post
  front matter; refuses overwrite; warns on unknown category slugs. +5 new
  tests.
- **P5-G `172189d` — sample-post validate-then-delete + template:** scaffold
  produced `_posts/2026-05-20-p5-sample-post.md`; all gates green (linter 0,
  structure 6/6, build clean, permalink resolves); sample DELETED from
  `_posts/` (controller decision A-4 — keeps corpus at 76, matching the live
  oracle exactly); the same content kept as `docs/sample-new-post.md`
  (committed, tested reference template; outside Jekyll build per
  `_config.yml exclude:`).
- **P5-H `579325e` — CI build-guard:** added `- name: Lint post content
  (no hardcoded structural HTML)` step at `.github/workflows/jekyll.yml`
  line 45, immediately before `Build with Jekyll`, running `uv run python
  -m scripts.fidelity.lint_content _posts --asset-root .`. (Initially a
  no-op until the CLI fix below.)
- **P5-H fix `84784f2` — `lint_content.py` CLI:** the script had no
  `__main__`/argparse → invoking it as a module exited 0 silently regardless
  of input → the build-guard was a no-op. Added an idiomatic argparse
  `_cli_main()` that lints the given paths (default `_posts`), prints
  findings in `path:line [CODE] message` format, exits 1 on findings (or
  path errors). +2 CLI smoke tests (clean-exits-0; violation-exits-1). The
  build-guard now actually enforces the P5 contract.
- **P5-A fix `1bd9d6f` — `_posts/2009-01-19-utf-8-in-python.md` fence:** the
  new UNCLOSED_FENCE check correctly flagged a pre-existing P0/P1-era
  WP-export defect (a `> ```python` blockquote-wrapped fence with a stray
  bare ` ``` `). The implementer missed it because the CLI was a no-op (the
  reviewer caught both). Applied the same approved §3.4 cfxs-free/fritzbox
  remediation: dropped the `> ` blockquote wrapper, reconstructed as a
  clean ```` ```python ```` block, oracle-faithfully byte-matched against
  the live WP page (the Python code incl. the `☺` U+263A literal restored).

## 3. Cumulative project state (P0 → P4 → PSC → P5)

- **76/76** posts (§11 verified).
- **Content linter 0** corpus-wide AND **enforced at CI build-time** (future
  structural-HTML in posts fails the deploy).
- **All 22+1 category pages** oracle-faithful (count + post-set).
- **Custom-domain ready:** `baseurl:""` + `url: https://blog.mithis.net` +
  CNAME + workflow + redirects + feed/sitemap absolute.
- **Authoring workflow documented + scaffolded:** `docs/AUTHORING.md`,
  `scripts/new_post.py`, `docs/sample-new-post.md` template.
- **structure_check 6/6** + **54 pytest** green.
- Comment system rendering site-wide (P3 fix); the include is now also
  list-fallback-robust for future `.yml`-only posts.

## 4. Handoff — what remains (see `FOLLOWUPS.md`)

**User action (carried from P4):** DNS cutover — CNAME `blog →
mithro.github.io`, GitHub Pages custom-domain + Enforce HTTPS.

**P6 — visual / Wayback / user signoff:**
- **HIGH/SYSTEMIC:** flat WP→MD list/paragraph structure (linter-invisible
  corpus-wide divergence; the next systemic pass — same data-driven
  oracle-audit→subagent-execute pattern PSC proved out).
- **MANDATORY user visual signoff (acceptance bar #3):** fritzbox bold-in-
  code lost; 3 linked-thumbnail `<a title=>` hover-tooltips lost in R-P4.
- **Wayback pixel sweep + final visual signoff** of every archetype/built
  post (incl. recovered P3 + restored PSC category pages).
- CSS micro-deltas, Picasa byte-fidelity, nav-below clearfix, R-E region-3
  fence cosmetic, P3 pre-existing comment-data fidelity check (e.g. 82-
  techtalk's pingback-looking comment author).

**P5 polish (recorded; all Minor, non-blocking):** 5 items from the P5-EXEC
code review — regex comment wording; dead test helper; AUTHORING §8 wording
self-contradiction; slug normalization in `new_post.py`; workflow uv-setup
self-documentation. Bundle in a future small polish commit.

## 5. Notes

- The CI build-guard is the project's first PROACTIVE fidelity safeguard
  (every prior phase fixed historical content; P5-H prevents future
  regressions in posts).
- The PSC pattern (oracle-audit → data-driven findings → subagent-execute
  per-row with 2-stage review) remains reusable for the P6/SYSTEMIC
  flat-list pass and any future systemic remediation.
