# P8 — Visual Polish + Systemic Tag Import: RESULTS & Handoff

**Status: COMPLETE (this iteration).** P8 exit gate met (§1). Branch
`migration-p8-visual-polish`, merged to `main`. Residual cosmetic items
recorded as P9 followups (FOLLOWUPS.md).

P8 continued the P7 visual-fidelity work toward 100% match with live
blog.mithis.net (broken stuff and all). It closed the remaining
above-the-fold deltas AND uncovered + fixed a systemic content-fidelity
gap: **the WP→Jekyll migration had dropped ALL post tags.**

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| Content linter (CLI, CI-enforced) | 0 | **PASS (0)** ✓ |
| `structure_check` | 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **56 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean ✓ |
| `_posts` count | 76 | **76** ✓ |
| CI build-guard (P5-H) | wired | unchanged ✓ |
| Post tags (footer + archives) | match live | 19 posts re-tagged; 3-sample verified ✓ |
| Category sort order | match live | alphabetical-by-title ✓ |
| Code-block container | match live `.wp_syntax` | gray-bg + silver border ✓ |
| `_posts/` BODIES unchanged | content intact | tag import added only frontmatter `tags:` blocks ✓ |
| Working tree | clean | commits ahead of `main` |

## 2. What P8 did

### Category sort order (`62da879`)
Live lists multi-post categories alphabetically by display title
(`Hardware, HDMI2USB, Summer of Code, TimVideos.us`); local was using
frontmatter order. Added a `_includes/sorted-categories.html` (DRY) used by
`home.html` + `category.html` + `post.html`; sorts categories to match live.
Verified exact match on the SoC post.

### entry-meta fidelity (`6355557`) + include newline (`9d40bd6`)
Fixed `post.html` entry-meta span structure/whitespace to match live.

### Author + tag archive pages (`23adb17`)
Created `/archives/author/mithro/` (was missing locally vs live) + tag
archive layout/generator + 44 `archives/tag/*.md` pages.

### SYSTEMIC: tag import from live (`be5b111`)
**The headline P8 finding.** 0 of 76 posts had a `tags:` frontmatter field;
the WP migration imported `categories:` but dropped tags entirely. No WP
export XML exists → scraped the live site (the authoritative oracle) for
each post's `rel="tag"` display names and imported them into frontmatter:
- 19 posts gained tags (57 genuinely have none on live — matched).
- 102 tag instances, 85 distinct tags.
- 3-sample verified against live (utf-8-in-python, epiphany2firefox,
  starhunter) — same tags, same order, same display names.
- Diff confined to frontmatter `tags:` blocks + 44 new archive pages; zero
  post-body changes.
- Two necessary layout bug-fixes: `post.html` tag-link slug bug (old code
  slugified the whole `/archives/tag/<tag>` path → broken URLs; fixed to
  slugify just the tag) + `tag.html` `where_exp` matching (display-name vs
  slug).

### Code-block container styling (`024fed1`)
Live code blocks use the wp-syntax plugin's `<div class="wp_syntax">`
(background `#f9f9f9` + 1px silver border + 1.5em bottom margin). P7's C7
had removed exactly this. Restored on the Rouge `.highlighter-rouge`
wrapper so code blocks render as the same gray bordered box as live.

## 3. Page-type audit results (P8-FINDINGS.md)

Home, basic post, code-heavy post, category, search, 404, tag archive,
author archive, hardware/project/tutorial layouts, date archives — all
PASS or accepted-divergence or N/A. See P8-FINDINGS.md for the per-type
table. No outstanding HIGH-severity visual delta remains.

## 4. Cumulative project state (P0 → P8)

- Content/structure/comments/URL fidelity (P0–P6) — intact.
- **Tags** — now imported (P8); previously entirely missing.
- Rendered visual fidelity (P7 + P8) — header, sidebar (RIGHT), widgets,
  categories (order + separator + full-content archives), dates (+1000),
  code-block styling, tag/author archives all match live; broken Picasa +
  Twitter reproduced (broken-stuff-faithful).
- Authoring workflow + CI build-guard (P5) — intact.
- **NOT done:** P9 residual cosmetics (tag-slug edge case, Rouge/GeSHi
  token colors, highslide JS) + the user's DNS cutover (still NOT to be
  suggested until the user is satisfied with fidelity).

## 5. P8 gate — independent re-verification

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # exit 0
uv run python -m scripts.fidelity.structure_check                      # 6/6
uv run python -m pytest tests/ -q                                      # 56
bundle3.3 exec jekyll build                                            # clean
ls _posts/*.md | wc -l                                                 # 76
# Tags: grep -l '^tags:' _posts/*.md | wc -l  → 19
# Visual: serve _site/ + Playwright screenshot vs live (P7-RESULTS §3 method)
```
