# PSC — Systemic Category Fidelity: RESULTS & Handoff

**Status: COMPLETE.** PSC exit gate met (§1). Branch
`migration-psc-systemic-categories`, ready to merge to `main`.

**The single largest remaining 100%-fidelity gap discovered during P4 is now
closed**, and the foundational corpus-completeness question is resolved
favorably: **the live WP has 76 posts; our corpus has 76 posts; §11 "76/76"
is met** (no posts are entirely missing; P3 closed that question completely).

---

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| §11 corpus completeness | live WP total == our `_posts/` count | **76 == 76** ✓ |
| Every category page | built count == live WP oracle count | **all 22+1 match** ✓ |
| Every post `categories:` | == live oracle slugified set | **all 76 verified** ✓ |
| Content linter | 0 findings | **PASS (0)** ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)** exit 0 ✓ |
| Hermetic suite | green | **45 passed** ✓ |
| Build | clean | **PASS** ✓ |
| Sidebar counts | match live oracle | lca 12 ✓, HDMI2USB 10 ✓, all others faithful ✓ |
| Working tree | clean | clean; 2 commits ahead of `main` |

## 2. What PSC did

- **PSC-T1 oracle audit (`c8c8706`):** enumerated the live WP's complete post
  inventory via WP per-month sub-sitemaps + category-archive union (76
  distinct WP IDs); for each post compared its live `rel="category tag"` set
  to current `categories:`. Produced `PSC-FINDINGS.md` (~900 lines).
  - **Resolved §11 "76/76":** live total = our 76. No genuinely-missing
    posts. (P3's 4 recoveries were the last; the discovery during P4 D-B was
    purely under-categorization, not missing posts.)
  - **Quantified the gap:** 26 under-categorized posts, 13 affected
    categories. No new category pages needed (P4 D-B's 4 covered it).
- **PSC-EXEC (`031f58c`):** front-matter-only `categories:` additions on
  exactly the 26 posts — every addition oracle-verified against the live WP
  (direct post for HTTP 200; live category-archive union for 500s). Plus the
  one sidebar count fix (`linux.conf.au` 10→12 — the P4 D-B polish had
  reduced it from a single-page WP-archive count; PSC's robust multi-page
  enumeration showed the true total is 12). Spec+code review independently
  re-verified all 26 posts oracle-faithful and all 13 category built counts =
  live oracle's post-ID sets.

## 3. Cumulative project state (P0 → P4 → PSC)

- **76/76** posts (§11 met; corpus content-complete).
- **Content linter: 0** findings corpus-wide (the 47 P0/P1-era findings →
  fully resolved across P2/P3/P4).
- **All 22+1 category pages** list exactly the live WP oracle's posts (now
  oracle-faithful in both count and post-set).
- **Custom-domain ready:** `baseurl:""`, `url: https://blog.mithis.net`,
  `CNAME`, workflow neutralized, `jekyll-redirect-from` in place, 19+19+
  rcs-darcs+tailor redirects for changed-URL spaces, feed/sitemap absolute.
- **structure_check 6/6** + **45 pytest** green.
- **Build clean** end-to-end.

## 4. Handoff — what remains (see `FOLLOWUPS.md`)

**User action (P4 RESULTS §3, unchanged):** the DNS cutover — apply the
`CNAME` DNS record `blog → mithro.github.io` (TTL 3600), set GitHub Pages
custom-domain to `blog.mithis.net`, enable Enforce HTTPS.

**P5 — new-post workflow + linter build-guard:** wire `lint_content` as a
build-time guard; scaffold a documented authoring workflow (so future
content adheres to the established faithful conventions); plus the recorded
P5 follow-ups: make sidebar counts dynamic (currently hardcoded; the P5/P6
robustness item the lca-fix surfaced); EOF normalization; dead
`_includes/category-feed.xml` cleanup; comment-form both-forms guardrail;
feed.xml `where:"categories",page.category` vs category.html `cat_slug`
parallel-convention doc; Task-L linter polish; the `cat_slug` rationale hint
for new categories.

**P6 — visual / Wayback / user signoff:**
- **HIGH/SYSTEMIC: flat WP→MD list/paragraph structure.** Whole corpus
  divergence (no blank-line separators; flattened nested `<ul>` / list-break
  ⇒ flattened in built render). Linter-invisible, deliberately deferred
  through P2/P3/P4/PSC. Needs a dedicated systemic content-structure pass —
  this is now the next-largest fidelity gap. (PSC's success suggests the
  same data-driven oracle-audit→subagent-execute pattern.)
- **MANDATORY user visual signoff (acceptance bar #3):**
  - fritzbox bold-in-code lost (3 `<pre>` blocks; §3.4 accepted micro-delta)
  - 3 linked-thumbnail `<a title=>` hover-tooltips lost in R-P4 (almost-there,
    google-patchwork ×2)
- **Wayback pixel sweep + final visual signoff** of every archetype/built
  post incl. the now-restored category pages + the recovered P3 posts.
- CSS micro-deltas, Picasa byte-fidelity, nav-below clearfix, R-E region-3
  fence cosmetic.

## 5. Notes

- The corpus is now in the strongest fidelity state the project has reached:
  count-complete, linter-clean, category-faithful, custom-domain-ready.
  The remaining gaps (P5 workflow hardening; P6 visual structure + signoff)
  are smaller in scope than PSC was and well-understood.
- The PSC pattern (oracle-audit → data-driven findings → subagent-execute
  per-post with 2-stage review) is reusable for the systemic flat-list pass.
