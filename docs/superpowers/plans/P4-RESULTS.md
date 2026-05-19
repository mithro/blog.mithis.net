# P4 — Domain/Deploy + R-P4 + Edge Cases: RESULTS & Handoff

**Status: COMPLETE.** P4 exit gate met (proof §1). Branch
`migration-p4-domain-deploy`, ready to merge to `main`.
**A major pre-existing systemic fidelity gap was discovered during P4 — see §4.
It does NOT block P4 (P4's gate is independent) but is the single largest
remaining fidelity item and needs a dedicated pass + a user decision.**

**Regenerate the gate:** `FIDELITY_SKIP_RENDER=1 uv run python -m
scripts.fidelity.run` (build + content linter), `uv run python -m
scripts.fidelity.structure_check` (6/6), `uv run python -m pytest tests/ -q`.

---

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| `_config.yml` | `baseurl: ""`, `url: https://blog.mithis.net` | ✓ both exact |
| `CNAME` | `blog.mithis.net` | ✓ |
| workflow | `--baseurl` base_path override removed | ✓ `bundle exec jekyll build` |
| **Content linter** | **0 findings** (was 22 R-P4) | **PASS — 0** ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)** exit 0 ✓ |
| Hermetic suite | green | **45 passed** ✓ |
| Build | clean | **PASS** ✓ |
| feed.xml / sitemap.xml | absolute `https://blog.mithis.net/…` | ✓ (163 absolute locs; feed absolute; zero `mithro.github.io`) |
| `/blog.mithis.net/` path-prefix in `_site` | none | **zero** ✓ |
| Changed-URL 301s | in place | ✓ (19+19 `/category/<slug>/`→`/archives/category/<slug>/`; rcs-darcs both old URLs) |
| Post WP permalinks | resolve | ✓ |
| Working tree | clean | clean; 13 commits ahead of `main` |

## 2. What P4 did

- **Keystone config (`8a1308f`):** `baseurl:""` + `url:https://blog.mithis.net`
  + `CNAME` + workflow neutralized + `jekyll-redirect-from` gem (controller
  consolidated P4-C5 into P4-C1 — documented P4-FINDINGS §A.4).
- **R-P4 conversion (`e56ed2a`+`aa60d19`):** the 22 deferred
  `{{…|relative_url}}` image/link residuals across 8 posts → faithful plain
  `/assets/…` (pure Markdown where possible; §7-minimal inline `<img>` only
  where width/height/class/srcset/title are Markdown-inexpressible;
  linked-thumbnails & closed links oracle-faithful; un-recoverable srcset
  variants dropped). **Content linter 0** — the corpus is now fully clean.
  (Lost `<a title=>` hover-tooltip on 3 image-links → P6 user-signoff item.)
- **feed/sitemap (`6f928ee`):** sitemap category `<loc>`→`/archives/category/`;
  excluded dead WP-era `sitemap_index.xml`; feeds verified absolute.
- **D-A redirects/forms (`e7a1f2d`+`eeddcee`):** 19 category `.md` + 19
  `feed.xml` `redirect_from` for the M1 URL move; rcs-darcs →
  `/archives/rcs/darcs/` (WP-faithful hierarchical URL) with both old URLs
  redirecting; 404 + dead-sidebar search forms → working `/search.html`.
- **D-B category restorations (`c35eaa4`+`db0998a`):** created 4 missing WP
  (sub)categories — `timvideos-us/hdmi2usb`, `scheme`, `sydney`,
  `rcs-tailor` (`/archives/rcs/tailor/`) — pages+feeds+sidebar; restored
  faithful multi-category `categories:` to 14 posts (each oracle-verified
  against the live WP category pages; followed the live oracle over a stale
  §D.2/§D.4 doc claim). Fixed a pre-existing `_layouts/category.html` bug
  (URL-last-segment vs `cat_slug` — broke hierarchical category listings).
- **D-B polish (`7503ac9`):** corrected the now-stale `lca`/`hdmi2usb`
  sidebar counts (→10, =built=oracle); documented the `cat_slug` listing
  convention in `category.html`.

Every task: fresh implementer → spec-compliance review → code-quality review;
multiple real defects caught & fixed mid-stream (post-7 anchor, the 2167/2169
oracle-sweep gap, the rcs-darcs redirect gap).

## 3. DNS handoff — ACTION REQUIRED BY THE USER (the user performs the cutover)

P4 makes the repo custom-domain-ready. The user must apply DNS + GitHub
settings (design §3: "user performs the cutover"). `blog.mithis.net` is a
SUBDOMAIN → use a CNAME DNS record:

| Type | Name/Host | Value/Target | TTL |
|---|---|---|---|
| `CNAME` | `blog` | `mithro.github.io` | 3600 (use 300 during cutover) |

Then in **GitHub repo → Settings → Pages**: set **Custom domain** =
`blog.mithis.net`, Save, wait for the DNS check, then enable **Enforce
HTTPS**. GitHub Pages auto-301s the old `*.github.io` URLs to the custom
domain (no extra config). The committed `CNAME` file is read by Pages and
keeps the domain enforced. Verify post-cutover: `https://blog.mithis.net/`
serves; `feed.xml`/`sitemap.xml` are absolute; the `/category/<slug>/` →
`/archives/category/<slug>/` redirects work live.

## 4. ⚠ MAJOR DISCOVERY — systemic multi-category UNDER-IMPORT (HIGH; pre-existing; NOT a P4 defect; needs a dedicated pass + USER DECISION)

While correcting the sidebar counts, the live-WP oracle sweep revealed
**11 categories where the built post count < the live WP oracle count**:

| Category | built | live WP | Δ |
|---|---|---|---|
| gaming-miniconf | 1 | 7 | −6 |
| summer-of-code | 1 | 8 | −7 |
| google | 3 | 7 | −4 |
| uni | 2 | 5 | −3 |
| python | 4 | 6 | −2 |
| pcb | 3 | 5 | −2 |
| diary | 1 | 2 | −1 |
| games | 2 | 3 | −1 |
| highlights | 1 | 2 | −1 |
| ubuntu | 2 | 3 | −1 |
| useful-bits | 3 | 4 | −1 |

**Confirmed root cause (at least partly):** the original WP→Jekyll migration
(P0/P1 era) imported many posts with only their **primary** WP category.
Concrete proof: live WP shows posts 75/66/65/62/61/46 in BOTH `lca` AND
`gaming-miniconf`; in `_posts` they exist but carry `categories: [lca]`
only. So those posts ARE present — they are just **missing their secondary
WP categories**, so they don't appear on the secondary category pages and
those pages/counts under-report. D-B fixed exactly this for its scoped 14
posts (schemepy, using-tailor, the 8+2 hdmi2usb, etc.); the count table
proves it is **systemic across the corpus**, far beyond D-B's slice.

**OPEN QUESTION (not yet resolved — needs an audit, and a user decision):**
are some shortfalls also **entirely-missing posts** (corpus < live WP),
which would contradict the design's "76/76 posts" success criterion, or is
it purely under-categorization of the 76 we have? The `gaming-miniconf`
evidence is pure under-categorization; other categories' Δ have not been
proven to be only that.

**This is the single largest remaining fidelity gap.** It is recorded in
`FOLLOWUPS.md` as a HIGH dedicated pass: an oracle-driven audit + remediation
that (a) determines true corpus completeness vs the live WP, (b) restores
the faithful full multi-category `categories:` to every affected post
(oracle = each post's live `rel="category tag"` set), (c) re-imports any
genuinely-missing posts (P3-style), (d) then makes the sidebar counts
correct/dynamic. The P4 sidebar counts were deliberately LEFT at the
faithful WP-oracle values (matching the original Barthelme sidebar) for
exactly the categories with this gap — changing them to the smaller built
counts would be *less* faithful; only `lca`/`hdmi2usb` (where D-B achieved
full faithful membership so built==oracle) were corrected.

## 5. Other follow-ups (non-blocking; see FOLLOWUPS.md)

- **P6 user-signoff:** the 3 linked-thumbnail `<a title=>` tooltips lost in
  R-P4 (alongside the fritzbox-bold item).
- **P5:** make sidebar counts dynamic (currently hardcoded → fragile, the
  root of the §4 staleness); document the `feed.xml` `where:"categories",
  page.category` vs `category.html` `cat_slug` parallel conventions; the
  `category.html` URL-segment fallback is flat-URL-only (comment added);
  prior P5 items (EOF normalization, dead `_includes/category-feed.xml`,
  comment-form both-forms guardrail, Task-L linter polish).
- **P6 cosmetic:** pre-existing trailing-space on 3 `sitemap.xml` blank
  separator lines; R-E region-3 fence nit; CSS micro-deltas; nav-below
  clearfix; Picasa byte-fidelity; the systemic flat-list/paragraph pass.

## 6. Artifacts

`docs/superpowers/plans/P4-FINDINGS.md` (the triage/plan keystone, with the
in-place corrections), `FOLLOWUPS.md` (authoritative cross-phase backlog —
now incl. the §4 systemic gap). `tmp/p4*` is gitignored scratch (regenerable
via `curl -sk` against the live original; TLS cert expired = expected).
