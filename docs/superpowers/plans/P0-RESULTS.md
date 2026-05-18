# P0 Results — measured worklist & handoff to P1

**Date:** 2026-05-19
**Branch:** `migration-fidelity-completion` (HEAD `94805bb`, 96 commits)
**Spec:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md`
**Plan:** `docs/superpowers/plans/2026-05-18-blog-fidelity-p0-build-and-harness.md`
**Regenerate this data:** `FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run` (writes `tmp/fidelity/fidelity-report.md`)

## P0 EXIT GATE — PASSED

Per spec §6.2 the P0 CI-able gate is build + content-linter + structural-comparator (no browser):

- **Build: PASS** — clean, deterministic `bundle exec jekyll build` (zero errors/warnings/Deprecation/Conflict). Verified by the Task 8 gate + the orchestrator run.
- **Harness emits `tmp/fidelity/fidelity-report.md`** ✅ (8950 bytes, server-free skip-render path).
- **Linter + structural comparator operational and unit-tested** ✅ — 35 hermetic unit tests pass (`uv run pytest -m "not integration" -q`).
- Harness process exit = **1**, which is the CORRECT/expected P0 result (`return 0 if (build_ok and not findings)`; build clean but the linter has the expected P2 worklist — P0 measures, it is not all-green).
- P0 tasks complete: T1, T2, T2A, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12 — each two-stage reviewed (spec compliance + code quality).

## Structural section = P1 THEME worklist

The structural comparator was run with render skipped (per spec §6.2 + the
`FIDELITY_SKIP_RENDER` rationale: the Playwright visual layer is heavyweight and
NOT meaningful until P4 sets `baseurl=""` — the dev site currently serves under
`/blog.mithis.net/` so browser captures would 404). Therefore the structural
"MISSING" lists below are the **Barthelme PHP-side structural anchor inventory**
each archetype's Jekyll output MUST contain — i.e. the concrete P1 theme target
list — NOT yet a Jekyll-vs-PHP diff. The real per-archetype diff is a documented
**post-P4 local re-run** (run the harness WITHOUT `FIDELITY_SKIP_RENDER`).

Anchors the Jekyll templates must reproduce, by archetype (from Barthelme
`index.php / single.php / archive.php / page.php / 404.php / search.php`):

- **home** (18): `div#container div#content div.hfeed div#post- div.post-container div.post-content h2.entry-title div.entry-content div.entry-meta span.entry-date span.entry-category span.entry-comments span.entry-permalink abbr.published div.navigation div#nav-below div.nav-previous div.nav-next`
- **post** (15): `div#container div#content div.hfeed div#post- h2.entry-title div.entry-content div.entry-date div.entry-meta span.meta-sep span.entry-interact abbr.published div.navigation div#nav-below div.nav-previous div.nav-next`
- **category** (20): adds `div.archive-meta span.archive-meta h2.page-title h3.entry-title` to the home set
- **page** (6): `div#container div#content div#post- h2.entry-title div.entry-content div.hfeed`
- **notfound** (9): `div#container div#content div#post-0 div.post div.entry-content h2.entry-title form#error404-searchform input#error404-s input#error404-searchsubmit`
- **search** (25): the home/category set + `form#noresults-searchform input#noresults-s input#noresults-searchsubmit div#post-0 span.search-meta`

Known noise to handle in P1 (already in FOLLOWUPS): `div#post-` / `div#post-0`
are phantom anchors from Barthelme's `id="post-<?php the_ID() ?>"` stripping —
filter or add to `compare.structural_diff(ignore=...)` in P1, do not chase them
as real Jekyll gaps.

## Content linter = P2 worklist (47 findings)

By code: **BLOCK_HTML 25**, **LIQUID_LEAK 11**, **MISSING_IMAGE 11** (several
MISSING_IMAGE are `{{ ` artifacts secondary to a LIQUID_LEAK on the same line —
they disappear once the Liquid leak is fixed). Posts needing P2 remediation:

```
2007-02-26-darcs-almost-perfect.md            BLOCK_HTML
2007-05-09-almost-there.md                    LIQUID_LEAK (+img artifact)
2007-08-17-resume.md                          LIQUID_LEAK
2007-09-06-nm-autovpn.md                      BLOCK_HTML x2
2007-11-11-python-swap-var.md                 BLOCK_HTML x2
2008-02-04-google-patchwork.md                LIQUID_LEAK x2 (+img artifacts)
2008-02-18-cfxs-free.md                       BLOCK_HTML + LIQUID_LEAK
2008-06-10-techtalk-gamingforfreedom.md       BLOCK_HTML
2009-01-20-reading-cookies-firefox.md         BLOCK_HTML x2
2009-01-26-osdc-orbital-death...md            BLOCK_HTML x2
2009-01-27-xcompiling-cygwin...md             BLOCK_HTML x2
2009-05-26-starhunter-fireflys...md           LIQUID_LEAK + BLOCK_HTML x2
2013-10-06-connecting-to-a-fritzbox...md      BLOCK_HTML x4 + LIQUID_LEAK x2
2014-07-23-hdmi2usb...day-2...md              BLOCK_HTML x3
2014-07-24-hdmi2usb...day-3...md              BLOCK_HTML x2
2014-07-25-hdmi2usb...day-4...md              LIQUID_LEAK x2 (+img artifacts)
2014-07-28-hdmi2usb...day-5-6-7...md          BLOCK_HTML
2015-07-05-first-v2-hdmi2usb...md             LIQUID_LEAK (+img artifact)
```
(Authoritative line-numbered list: regenerate `tmp/fidelity/fidelity-report.md`.)

## Live-site status → P3 is UNBLOCKED

`https://blog.mithis.net/` now returns **HTTP 200** with TLS verification
disabled (`curl -k`); plain HTTPS fails only with `certificate has expired`
(curl error 60). The user is restoring the site. **P3 (recover missing posts
15, 35, 84, 92) is now feasible**: the P3 scraper must either disable TLS
verification (the content is what matters, not the cert) OR the user renews the
cert first. Wayback remains the per-post fallback.

## Deferred items

All cross-phase follow-ups discovered during P0 are in
`docs/superpowers/plans/FOLLOWUPS.md` (P1 theme/phantom/cleanup, P2 content,
P3 wayback call-site + live-site cert, P5 gate/linter hardening).

## Next step (do NOT fix ad hoc)

P0 is complete. Per plan Task 13: return to `superpowers:writing-plans` to author
the **P1 theme-fidelity plan** (driven by the structural target list above +
post-P4 visual re-run) and subsequently P2/P3/P4/P5/P6. P3 is now unblocked by
the live site; P4 (custom-domain `baseurl=""`) is a prerequisite for the real
visual structural diff. Each subsequent phase is its own spec→plan→execute cycle.
