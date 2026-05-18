# Blog Migration Completion — Design Spec

**Date:** 2026-05-18
**Status:** Approved design (pending spec review + user spec review)
**Topic:** Complete the WordPress → Jekyll/GitHub Pages migration of blog.mithis.net with verified 100% visual fidelity, no hardcoded HTML, and a repeatable new-post workflow.

---

## 1. Context & current state

The repository migrates Tim "mithro" Ansell's WordPress blog (Barthelme theme) to a Jekyll
static site deployed via GitHub Actions to GitHub Pages.

What already exists and works:

- **Theme is properly templated**, not hardcoded: `_layouts/` (default, post, home, page,
  category, project, tutorial, hardware) + `_includes/` (header, footer, sidebar,
  navigation, comments) + `assets/css/main.css`. Posts are Markdown + YAML front matter.
- **72 of 76 posts** migrated as clean Markdown with WordPress-exact per-post
  `permalink:` (`/archives/{category}/{id}-{slug}`).
- **Static comment system**: 12 posts have threaded comments in `_data/comments/*.yml`.
- **Reference source of truth**: `theme_analysis/barthelme/` contains the *complete*
  original WordPress theme — every `.php` template, `style.css`, `print.css`, and
  `screenshot.png`.
- **Deploy**: `.github/workflows/jekyll.yml` builds and deploys to GitHub Pages.
- **Recovery tooling** already present: `scripts/wayback_extractor.py`,
  `scripts/extract_missing_posts.py`, `exports/scripts/full_site_scraper.py`,
  `scripts/html_to_markdown.py`, and related conversion scripts.

Known problems / unverified areas:

- The 5 most recent commits are all Jekyll build-failure firefighting (Liquid syntax,
  HTML list tags). There is **no build gate**, so regressions recur.
- Jekyll/Bundler are **not installed locally**; build health is unverified.
- **4 posts missing**: WordPress IDs 15, 35, 84, 92.
- **Config conflict**: `_config.yml` hardcodes `baseurl: /blog.mithis.net` while the
  workflow *also* passes `--baseurl "${{ steps.pages.outputs.base_path }}"`. They agree
  by coincidence today but break under a custom domain.
- **Visual fidelity is unmeasured**. The original `blog.mithis.net` is offline
  (connection refused — confirmed genuinely down, not a sandbox block), so there is no
  live comparison target yet.
- The Picasa header photo strip in `_includes/header.html` hotlinks Google CDN images
  and contains dead "View at Picasa" links.

Environment facts established: this environment **can** reach `rubygems.org`,
`web.archive.org`, and `github.com` (so local Jekyll build, Playwright, and Wayback are
all viable). It **cannot** reach `blog.mithis.net` (offline).

## 2. Goal & success criteria

Complete the migration such that:

1. **100% visual fidelity** to the original Barthelme-themed blog, verified by *all* of:
   (a) structural/visual diff vs `theme_analysis/barthelme/` + Playwright screenshots,
   (b) Wayback Machine pixel reference, (c) user final visual signoff.
2. **No hardcoded HTML** in posts — theme stays Liquid-templated; posts stay Markdown;
   this is *enforced* by an automated check so it remains true for future posts.
3. **New posts follow the existing theme** via a documented, validated authoring workflow.
4. **All 76 posts present** (recover the 4 missing).
5. **Custom-domain ready**: configured for `blog.mithis.net`; user performs DNS later.
6. **Picasa header** kept literally identical to the original for now (improvement deferred).

## 3. Decisions (user-confirmed 2026-05-18)

- **Deploy target**: custom domain `blog.mithis.net`. Configure `CNAME` +
  `url: https://blog.mithis.net` + `baseurl: ""` now; user does DNS cutover later. The
  workflow's `--baseurl` override must be removed/neutralized for custom-domain correctness.
- **4 missing posts (15, 35, 84, 92)**: user will restore the live `blog.mithis.net` so
  they can be scraped from source; Wayback is the fallback per post.
- **Picasa header**: Phase 1 = replicate *exactly* as the original (hotlinked Google CDN
  images and dead links included). Phase 2 (post-fidelity, out of scope here) = replace
  with a better result.
- **Fidelity acceptance**: all three methods required — structural+Playwright, Wayback
  pixel, then user signoff once the first two pass.
- **Sequencing**: proceed with all work that has no live-site dependency now; periodically
  poll `blog.mithis.net` reachability so P3 (missing posts) and the live portion of P6
  start automatically as soon as the user's restore is detected.

## 4. Chosen approach

**Approach 1 — verification-harness-first, diff-driven gap closure.**

Stand up a green reproducible build and an automated fidelity harness *before* fixing
anything. Every fidelity gap is then *found by measurement*, fixed, and *re-verified*
against the same harness. This converts "100% fidelity" from a subjective judgement into
a measured, regression-safe gate, directly operationalizing the user's multi-method
acceptance bar, while reusing existing working code rather than discarding it.

Rejected alternatives:

- **Manual page-by-page eyeballing**: not reproducible, subjective, does not scale to 72+
  posts, does not satisfy the automated-verification requirement.
- **Rewrite all templates from the Barthelme PHP**: discards substantial working code
  (header gallery, comment integration, navigation), high regression risk, assumes
  everything is wrong instead of measuring what actually differs.

## 5. Architecture — phased plan

Each phase has an explicit exit gate enforced by the harness. Phases with no live-site
dependency (P0, P1, P2, P4, P5) proceed immediately; P3 and the live portion of P6 are
gated on `blog.mithis.net` becoming reachable (polled).

| Phase | Goal | Exit gate |
|---|---|---|
| **P0 Build + Harness** | Pinned `bundle install`; `jekyll build` with zero errors/warnings; Playwright archetype screenshots; Wayback fetcher; structural comparator; content linter | Green build **and** harness emits `tmp/fidelity/fidelity-report.md` |
| **P1 Theme fidelity** | Diff each layout/include/CSS vs the matching Barthelme `.php` + `style.css`; close gaps | Every archetype structurally matches Barthelme; Picasa header byte-identical to original markup |
| **P2 Content fidelity** | Audit all 72 posts: no Liquid leakage, no raw structural HTML, images resolve, code/lists correct | All posts render clean; no-hardcoded-HTML check passes for every post |
| **P3 Missing posts** | Recover IDs 15/35/84/92 from restored live site (Wayback fallback per post); convert to existing post format incl. comments | 76/76 posts; their WordPress URLs resolve; pass content linter |
| **P4 Domain/deploy** | `CNAME`; `_config.yml` `url`/`baseurl`; remove workflow `--baseurl` conflict; feed/sitemap absolute URLs | Build correct under custom domain; exact DNS records handed to user |
| **P5 New-post workflow** | Authoring guide + scaffold script + sample post proving identical rendering; build-time hardcoded-HTML guard | Sample post renders pixel-identical to peers; guard active and documented |
| **P6 Final acceptance** | Wayback pixel-comparison sweep across archetypes + sample posts; final fidelity report; user signoff | First two acceptance methods pass; user approves |

## 6. The verification harness (novel core)

Lives in `scripts/` (Python, run via `uv run`); all transient output in project-local
`tmp/fidelity/` (gitignored; cleaned up after runs). Each component is single-purpose with
a defined input/output so it can be understood and tested in isolation.

- **6.1 Builder** — wrapper around `bundle exec jekyll build` (and `serve` for Playwright).
  Input: repo. Output: `_site/` + a build log. Contract: non-zero exit on *any* Jekyll
  error or warning. This is the missing build gate.
- **6.2 Archetype renderer** — drives Playwright (MCP) against the locally served site at
  fixed viewport(s). Input: list of archetype URLs (home, a representative post, a
  category page, a static page, 404, search, `feed.xml`). Output: per-archetype PNG
  screenshot + serialized DOM snapshot in `tmp/fidelity/jekyll/`.
- **6.3 Reference capture** —
  - *Wayback fetcher*: for a given original URL, resolves the best `web.archive.org`
    snapshot and stores rendered HTML + screenshot in `tmp/fidelity/wayback/`.
  - *Barthelme structure extractor*: parses `theme_analysis/barthelme/*.php` to derive the
    expected element/class/id skeleton per template (the structural ground truth).
- **6.4 Comparator** — two diffs per archetype: (i) *structural* — Jekyll DOM vs Barthelme
  expected skeleton (element tree + class/id presence/order); (ii) *visual* — Jekyll
  screenshot vs Wayback screenshot. Output: `tmp/fidelity/fidelity-report.md` with
  per-page PASS/FAIL, the specific differing nodes, and image diffs.
- **6.5 Content linter** — scans `_posts/` (and recovered posts) for: unrendered Liquid
  (`{{`/`{%` leakage), raw block-level HTML that should be Markdown, unresolved image
  paths, broken internal links. Output: machine-readable findings list; non-zero exit on
  any finding. Reused as the P5 build-time hardcoded-HTML guard.

**Data flow:** Builder → served site → Archetype renderer → (Jekyll artifacts); Reference
capture → (Wayback + Barthelme artifacts); Comparator consumes both → report. Content
linter runs directly on sources, independent of the render pipeline.

## 7. Content fidelity strategy (P2)

"No hardcoded HTML" is defined precisely: a post may contain *inline* HTML only where
Markdown cannot express the original (e.g. an `<abbr>`, an attribute on an image) — but
no structural/layout HTML (no `<div>`, no layout tables, no theme chrome). The content
linter encodes this rule. Every post is checked; violations are converted to Markdown or
to the minimal justified inline element. The audit is systematic (all 72 posts), not
sampled, because the recent commit history shows conversion artifacts are widespread.

## 8. Missing posts recovery (P3)

Gated on `blog.mithis.net` reachable (polled). Per post (15, 35, 84, 92): scrape from the
restored live site using the existing scraper; if a post is unavailable live, fall back to
Wayback for that post. Convert via the existing `html_to_markdown.py` pipeline to *match
the exact front-matter shape and Markdown style of already-migrated posts* (same keys:
`author, categories, date, excerpt, layout, permalink, title, wordpress_category,
wordpress_id, wordpress_url`). Attach any comments to `_data/comments/`. Each recovered
post must pass the content linter and its WordPress URL must resolve.

## 9. Domain / deploy changes (P4)

- Add `CNAME` containing `blog.mithis.net`.
- `_config.yml`: `url: "https://blog.mithis.net"`, `baseurl: ""`.
- `.github/workflows/jekyll.yml`: remove/neutralize
  `--baseurl "${{ steps.pages.outputs.base_path }}"` so a custom domain build uses an
  empty base path (otherwise every asset/URL gets a wrong `/blog.mithis.net` prefix).
- Verify `feed.xml`, `sitemap.xml`, and `jekyll-sitemap`/`jekyll-feed` output use absolute
  `https://blog.mithis.net` URLs.
- Produce the exact DNS records (A/AAAA apex + `www`/CNAME as applicable) for the user to
  apply; the user performs the cutover.

## 10. New-post workflow (P5)

Deliverables: a short `CONTRIBUTING`-style authoring doc (front-matter template, required
keys, category list, where images go, how permalinks work) **plus** a scaffold script that
emits a correctly-stubbed post file. Validation: create one sample post through the
documented workflow and assert via the harness that it renders structurally/visually
identical to existing posts. The content linter is wired as a build-time guard so a future
post containing hardcoded structural HTML fails the build.

## 11. Acceptance criteria

Mapped directly to the user's three-method bar; **all** must hold:

1. Structural diff vs `theme_analysis/barthelme/` shows zero *unexplained* differences for
   every archetype, **and** Playwright screenshots are reviewed.
2. Wayback pixel comparison shows no visible layout/typography/color deviation across
   archetypes and sample posts.
3. User final visual signoff after (1) and (2) pass.

Plus objective gates: green Jekyll build with zero warnings; 76/76 posts; content linter
clean; custom-domain build correct; sample new post renders identically; hardcoded-HTML
guard active.

## 12. Isolation & conventions

- Harness scripts: Python, `uv run`, one responsibility each, under `scripts/`.
- All transient output under project-local `tmp/` (gitignored), cleaned up after use.
- No hardcoded structural HTML introduced anywhere; theme changes stay in
  layouts/includes/CSS.
- Small, focused commits per gap closed (per repo `CLAUDE.md`).
- Dates: ISO 8601 / day-first only.

## 13. Risks & mitigations

- **Live site never restored** → P3 and live-portion of P6 fall back fully to Wayback;
  any post unrecoverable even from Wayback is reported to the user with a recommendation
  (stub-with-URL vs accept gap) rather than silently dropped.
- **Wayback snapshots incomplete/altered** → structural diff vs `theme_analysis` PHP
  remains the primary fidelity oracle; Wayback is corroborating, not sole.
- **Build environment drift** (local Ruby 3.3 vs CI 3.1) → pin via `Gemfile.lock` and add
  a `.ruby-version`; the Builder gate runs the same command CI runs.
- **Visual diff false positives** (font rendering, antialiasing) → comparator reports
  diffs for human adjudication rather than hard-failing on pixel noise; structural diff is
  authoritative for PASS/FAIL.

## 14. Out of scope (YAGNI)

- Phase 2 Picasa-gallery replacement/redesign.
- Performance/CDN/image-format optimization beyond what fidelity requires.
- Analytics/GA setup (placeholder stays).
- Comment *submission* (the static comment system is display-only by design).
- Any redesign or "modernization" of the Barthelme look — fidelity, not improvement.
