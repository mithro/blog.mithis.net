# P11 — Dropped-Link Restoration: RESULTS & Handoff

**Status: COMPLETE.** P11 exit gate met (§1). Branch
`migration-p11-link-restoration`, merged to `main`.

## Why P11 happened

After P10 (exhaustive structural tag-count diff), I ran a **second
exhaustive automated dimension**: per-post link-href + image-src comparison
(built `_site` entry-content vs live blog.mithis.net). It found the
migration had **dropped ~13 links** across 9 posts — leaving dangling `[`
markers where the `](url)` was lost (rendering as literal `[`). These were
links to **downloadable files** (conference PDFs, an Eagle `.ulp` script,
NetworkManager scripts, a `.deb`, a `.patch`) and **linked-image wrappers**
(`<a href="full-image"><img></a>`), plus one broken email.

**The dropped content was real and user-facing**: visitors could no longer
download the author's OSDC paper/presentation, tech-talk slides, honours-
project report PDFs, or the scripts/patches the posts describe. Content
preservation is a core migration requirement.

Crucially: **the target files already existed in the repo** (migrated to
`assets/images/wp-content/uploads/` but left unlinked) — only the markdown
links were lost. So P11 restored the links pointing to the existing files
(board.png, the one file not in the repo, links to its live URL per the
corpus convention for non-downloaded files).

## 1. Exit gate (verified from clean tree)

| Gate | Required | Observed |
|---|---|---|
| Content linter (CLI, CI-enforced) | 0 | **PASS (0)** ✓ |
| `structure_check` | 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **56 passed** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean ✓ |
| `_posts` count | 76 | **76** ✓ |
| href/src diff (built vs live) | dropped-file-links resolved | **1/76 residual** (acceptable — see §3) ✓ |
| Typography (smart-quotes/NBSP) | byte-faithful | 8/9 posts 0 drift; cfxs's 1 quote change is a **faithful correction to live** (verified `&#8221;`/`”`) ✓ |
| Restored links render | files served | osdc PDFs → `/assets/images/wp-content/uploads/2009/01/osdc-{paper,presentation}.pdf` ✓ |

## 2. What P11 did (9 commits, 13 links)

| wid | Post | Restored |
|---|---|---|
| 99 | osdc-orbital-death | `[put a copy here on my blog]`→osdc-paper.pdf; `[presentation I gave]`→osdc-presentation.pdf |
| 82 | techtalk-gamingforfreedom | `[upload the slides…]`→techtalk6-pdfable.pdf |
| 41 | cfxs-all-done | `[Final Report]`→final-report-small.pdf; `[Technical Document]`→technical-small.pdf (+ closing-quote corrected to live's `”`) |
| 51 | nm-autovpn | `[…/02runcmd]`→02runcmd; `[…/nm-startvpn]`→nm-startvpn |
| 54 | nm-openvpn-dns | `[patch]`→nm-openvpn-dnsdomain.patch; `[deb for Ubuntu Gusty.]`→network-manager-openvpn_*.deb |
| 21 | eagle-for-pcb | board.png as a linked image (`[![alt](src)](full)`; board.png not in repo → live URL) |
| 23 | eagle2geda | `[script which converts…]`→eagle2geda.ulp; eagle2geda.png as a linked image |
| 2045 | first-v2-hdmi2usb | HDMI2USB-Prod-V2.jpg as a linked image |
| 79 | going-to-sydney | broken `mailto://mithis.com` → `mailto://mithro@mithis.com` (matches live) |

Method: **targeted Edits only** (wrap the dangling `[anchor` → `[anchor](url)`),
never bulk line/file rewrites — avoiding the typography-stripping bug that
bit PSL Phase 3 + P10. Independently verified 0 smart-quote/NBSP drift on
8/9 posts; the 1 cfxs quote change was confirmed against the live oracle as
a faithful correction (live renders `&#8221;` = `”`; the migrated source
had an erroneous `“`).

## 3. The 1 residual delta (acceptable)

`2045-first-v2`: external links `digilentinc.com/atlys` / `numato.com` —
live has them **scheme-relative** (no `http(s)://`, technically broken on
live), built has explicit `https://`. The built form is arguably more
correct; this is a pre-existing source nuance, not a dropped link. Left
as-is (could match live's scheme-less form for byte-fidelity, but that
would intentionally re-break the links — not worth it).

## 4. Cumulative project state (P0 → P11)

- Content + tags + **download/file links** + structure + comments + URLs —
  intact and now link-complete.
- Per-post structural fidelity (P10): 69/76 exact + 7 documented artifacts.
- Per-post link/image-target fidelity (P11): 75/76 exact + 1 acceptable
  external-scheme nuance.
- Rendered visual fidelity (P7–P9) — matches live.
- Authoring workflow + CI build-guard (P5) — intact.
- **Only remaining: the user's DNS cutover** (not to be suggested until the
  user confirms satisfaction).

## 5. The two exhaustive verification tools (reusable)

- `tmp/verify-all/compare2.py` — all-76 structural tag-count diff (P10).
- `tmp/hrefcheck/cmp2.py` — all-76 link-href + image-src diff (P11; folds
  the `/assets/images/wp-content/` ↔ `/wp-content/` local-hosting scheme).

Both require a live fetch (curl loop) + a local build; re-run after any
content/template change to catch regressions. Manual diligence, not CI.

## 6. P11 gate — independent re-verification

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # 0
uv run python -m scripts.fidelity.structure_check                      # 6/6
uv run python -m pytest tests/ -q                                      # 56
bundle3.3 exec jekyll build                                            # clean
# href fidelity: re-run tmp/hrefcheck (curl + cmp2.py) → 1/76 residual
```
