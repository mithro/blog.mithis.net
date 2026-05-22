# P8 — Visual Polish + Tag Import: per-page-type audit & findings

Audit of all remaining page types vs live blog.mithis.net (1280px viewport,
Playwright screenshot pairs). Companion to P8-RESULTS.md.

## Per-page-type results

| Page type | Status | Notes |
|---|---|---|
| Home `/` | ✅ PASS | sidebar RIGHT, header Picasa, Twitter widget, category order/sep, dates — all match (P7 + P8 category-sort) |
| Post (basic) | ✅ PASS | starhunter — matches live |
| Post (code-heavy) | ✅ FIXED | utf-8-in-python — code block now has gray-bg + silver border matching live `.wp_syntax` (`024fed1`). Syntax token colors (Rouge vs GeSHi) differ subtly → followup. |
| Post (footer "Tagged …") | ✅ FIXED | was missing — tag import (`be5b111`) restored tags on 19 posts; footer now renders the tag list matching live. |
| Category page | ✅ PASS | python — full post content inline, category order/sep match (P7 + P8) |
| Search `/search.html` | ✅ ACCEPTED-DIVERGENCE | Live uses WP dynamic `/?s=query` (server-side); Jekyll uses static `/search.html` + JS (`search.json`). Inherent static-site difference; the page chrome (header/sidebar/title) matches. |
| 404 | ✅ PASS | Both local + live return "Not Found" content; local `404.html` present. |
| Tag archive `/archives/tag/<slug>/` | ✅ FIXED | 44 archive pages created (`23adb17`) + now populated by tag import. |
| Author archive `/archives/author/mithro/` | ✅ FIXED | created (`23adb17`) — was missing locally. |
| Hardware/Project/Tutorial layouts | ✅ N/A | No `_posts/*.md` uses these layouts (`grep -l "^layout: X"` → empty). Layouts exist but are unused → no fidelity concern. |
| Date archives `/archives/YYYY/` | ✅ N/A | Live returns 404 for `/archives/2009/` — live has NO date archives. Local has none. No delta. |

## Systemic finding: WP migration dropped ALL post tags

The biggest P8 discovery: **0 of 76 posts had a `tags:` frontmatter field**,
though live shows tags on posts (footer "Tagged …" + `/archives/tag/`).
The WP→Jekyll migration imported `categories:` but not tags. Fixed by
scraping the live site (no WP export XML exists) and importing tags into
frontmatter — see P8-RESULTS §2 / commit `be5b111`. 19 posts have tags on
live (57 genuinely have none); 102 instances, 85 distinct tags; 3-sample
verified against live (name + order).

## Remaining deltas → P8-followups (recorded in FOLLOWUPS.md)

1. **Tag slug edge case** (2 tags): `sys.stdout` → Jekyll slugify
   `sys-stdout` vs live `sysstdout`; `linux.conf.au` → `linux-conf-au` vs
   live `linuxconfau`. Jekyll's `slugify` converts `.`→`-`; WP removes it.
   Alias archive pages created so both URLs resolve, but the primary
   post-footer tag link uses the Jekyll slug. To match live exactly would
   need a WP-compatible slug filter/mapping for dot-containing tags.
2. **Rouge vs GeSHi syntax token colors**: code-block container now matches
   (gray bg + silver border); the per-token highlight COLORS differ (Rouge
   palette vs live's GeSHi). Would need a custom Rouge theme matching GeSHi.
3. **Highslide lightbox JS** (from P7): header thumbnail click → ggpht 404
   directly instead of JS lightbox. Low priority (thumbnails 404 anyway).
