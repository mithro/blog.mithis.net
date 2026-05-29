# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Jekyll-built **pixel-perfect mirror** of the legacy WordPress blog at https://blog.mithis.net, currently deployed to https://mithro.github.io/blog.mithis.net via GitHub Pages. **Cutover is imminent**: blog.mithis.net will soon point at this site as its custom domain.

The migration phase is complete (175/185 pages literally pixel-perfect, remainder under 0.012%). Day-to-day work is **fidelity maintenance** and **new authoring**: when the deployed site drifts from live, identify the divergence with the diff tools below and fix it; when writing a new post, follow `docs/AUTHORING.md`.

### Cutover to blog.mithis.net (when DNS flips)

Three changes — one commit:

1. `_config.yml`: set `baseurl: ""` (drop the `/blog.mithis.net` subpath).
2. `_config.yml`: set `url: "https://blog.mithis.net"` (drop the github.io staging origin).
3. Create a `CNAME` file at the repo root containing the single line `blog.mithis.net`.

After deploy, the diff tooling in `tmp/` still works — point `LIVE_BASE` / `DEPLOYED_BASE` at the same custom-domain origin to verify zero regression, or compare against the Wayback machine to validate cutover-day fidelity.

### Core directive (durable, from the user 2026-05-21)

> "The github version should be faithful to the current live https://blog.mithis.net — broken stuff and all"

Broken Picasa thumbnails, cached Twitter, Shashin galleries, missing wp-content uploads — all preserved as-is. Don't "fix" them. The site should be visually and functionally indistinguishable from the live blog, including its bugs.

## Build, serve, deploy

```bash
# Build (production env so SCSS etc compile right)
JEKYLL_ENV=production bundle3.3 exec jekyll build

# Local serve — see "Local serving" below; URLs must use the /blog.mithis.net/ baseurl prefix
uv run python tmp/serve.py    # runs SimpleHTTPServer on :8731 from tmp/serve/

# Push to deploy (GitHub Actions builds + publishes)
git push origin main

# After EVERY push, verify CI passed and the site re-deployed before claiming a fix is live:
gh run list --limit 1
```

`bundle3.3` (not bare `bundle`) is the right Ruby 3.3 bundler for this repo's Gemfile.lock.

GitHub Pages must use the **GitHub Actions builder** (not the legacy branch builder) so custom plugins run — see `.github/workflows/jekyll.yml`. The legacy builder would silently skip `_plugins/` and produce a broken build.

## Local serving (`tmp/serve/`)

`_config.yml` sets `baseurl: /blog.mithis.net`, so internal URLs have a `/blog.mithis.net/...` prefix. The build still emits files to `_site/` (without that prefix). `tmp/serve/blog.mithis.net` is a symlink → `_site/` so `http://127.0.0.1:8731/blog.mithis.net/...` resolves locally to `_site/...`.

Always start the local server from `tmp/serve/` (not `_site/`) so the baseurl prefix works.

Cutover to the `blog.mithis.net` custom domain is a future step: change `_config.yml` `baseurl: ""` and `url:` to the production origin.

## Pixel-perfect verification workflow

The breakthrough tool of the recent fidelity push: **`tmp/diff_mask.py`** — generates a full-page mask image where every pixel that differs between live and local is painted red on white. Red pixels form character-shape clusters, so you can immediately see WHICH glyphs differ instead of guessing at sub-pixel noise. Use it FIRST on any new divergence.

Workflow tools (all in `tmp/`, all use Playwright + numpy/PIL via `uv run --with playwright --with numpy --with pillow python …`):

| Tool | Purpose |
|---|---|
| `batch_pixdiff.py` | Sweep all 75 posts: live vs local. Reports per-post diff %. |
| `listing_diff_all.py` | Same, for all 110 listing/tag/category/author/pagination pages. |
| `sweep_deployed.py` | live vs DEPLOYED mithro.github.io (use after CI deploy). |
| `check_each.py` | For one list of pages, dump per-page diff bands as (y₀,y₁,xrange,px_count). |
| `diff_mask.py` | The red-on-white character-shape mask (the breakthrough viz). |
| `diff_per_row.py` | Sort rows by diff-pixel count. |
| `sample_color.py` | Sample exact RGB at given (x,y) — confirms whether a glyph really differs or is just anti-aliasing. |
| `shot_one.py`, `cmp_dep.py` | Pairwise screenshot helpers. |
| `crop_box.py`, `upscale4x.py` | Crop a region and zoom 4x for visual diff. |

DOM probes (Playwright + `getComputedStyle`) are how you confirm a CSS/HTML hypothesis. Don't trust your eyes on zoomed PNGs — sample actual pixel colors and computed styles.

The pixel-perfect goal targets the DEPLOYED mithro.github.io site, not just local. After every push, run `sweep_deployed.py` (or a targeted sub-set via `check_each.py`) to confirm the fix landed.

## Plugin architecture (`_plugins/`)

Two custom Jekyll plugins do the heavy lifting:

- **`baseurl_asset_paths.rb`** — rewrites asset paths in the output HTML to include the `/blog.mithis.net/` baseurl prefix for the github.io staging mode.

- **`python_token_overrides.rb`** — Jekyll `post_render` hook that rewrites Rouge-emitted HTML inside `.language-python` / `.language-bash` code blocks to match the live's WP-Syntax (GeSHi) output:
  - Per-token color overrides (commas → light green `#66cc66`, `%` operator → inherit, etc.)
  - Span splitting for merged punctuation (`<span class="p">],</span>` → `,` gets its own green span)
  - Pre-styling for module-name patterns (`from cStringIO import` → cStringIO crimson)
  - Stripping of plain `.n` (Name) and `.sa` (string affix) spans to match live's unwrapped text
  - Inserting `\X` escape highlighting inside raw-string `.s` spans
  - Bash-specific overrides (`/` paths bold-black, `;;` bold-black, `$VAR` in `"…"` red)

The plugin runs after Rouge produces its HTML, so it edits HTML — it does NOT change Rouge's lexer. Patterns and reasoning are documented inline in the file.

## Critical files & invariants

- **`_layouts/default.html` starts with `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" …>`** — XHTML 1.0 Transitional triggers Chromium's *almost-standards mode* which matches the live blog's rendering. Do not change to HTML5 doctype; it breaks pixel parity across all pages.
- **`assets/css/main.css`** is the main stylesheet. Plain CSS (not SCSS). Many token-color overrides live here scoped to `.language-python .highlight .X` selectors. Notes inside explain WHY each rule exists (with `Live's GeSHi …` references).
- **`_config.yml`** baseurl / url comments mark the staging-vs-cutover toggle.
- **Galleries are PINNED** (deterministic) for both the header and sidebar — see commits 341a44c, 757ec74, d174bac. Don't randomize them.

## Fidelity linter (raw HTML rule)

`scripts/fidelity/lint_content.py` enforces "no hardcoded block HTML in posts". Inline HTML (`<a>`, `<code>`, `<em>`, `<img>`, etc.) is fine. Block HTML (`<div>`, `<object>`, `<table>`, `<p>` etc.) requires an opt-out sentinel:

```
<!-- fidelity-allow: BLOCK_HTML necessary-embed — <reason> -->
{::nomarkdown}
<p><object …></object></p>
{:/nomarkdown}
```

**Critical:** the sentinel must be on the SAME line as the BLOCK_HTML or the IMMEDIATELY PRECEDING line. Wrapping with `{::nomarkdown}` in between would push the sentinel two lines away → CI fail. (This bit 17 commits silently before being caught.)

## Git workflow

- `origin` is `git+ssh://github.com/mithro/blog.mithis.net`. Push to it directly (no fork chain).
- Commit messages should explain WHY (the live-fidelity reason), not just WHAT. Include diff-% before/after when relevant. End with `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- **Always check CI after pushing:** `gh run list --limit 1`. A green CI is necessary, not sufficient — also verify with `sweep_deployed.py` (or by reading mithro.github.io directly) that the change is actually deployed and matches live.

## Auto-memory location

`/home/tim/.claude/projects/-home-tim-github-mithro-blog-mithis-net/memory/` holds session-spanning notes (current fidelity state, workflow learnings, server-leftover audit, etc.). The `MEMORY.md` index there is the entry point.

## Common pitfalls

- **Wrong server cwd** — starting the local server from `_site/` instead of `tmp/serve/` makes every `/blog.mithis.net/…` URL 404. The pixel diff will hit ~12% (just live's content vs an empty local), looking like a catastrophic regression.
- **Bare `bundle exec`** — uses the wrong Ruby. Use `bundle3.3 exec`.
- **Stale screenshots in `tmp/`** — pairwise diff scripts overwrite the same paths. Re-run `shot_one.py` after every build, or you'll be looking at last-build's diff.
- **Trusting visual judgment of zoomed PNGs** — Chromium renders the same character differently for cross-domain font cascades. Use `sample_color.py` / DOM probes to confirm.
- **Forgetting the CI check** — commit + push doesn't equal deployed. The user notices when github.io still shows old content while CI is mid-run or failed.

## Personal coding conventions (from the user's global `~/.claude/CLAUDE.md`)

- Always use `uv run` / `uv pip` for Python (never bare `python`/`pip`).
- Date format: ISO 8601 (`YYYY-MM-DD`) or day-first (`29 May 2026`). Never American month-first.
- Small, focused commits. No `git push --force` (use `git safe-force-push <branch>` if necessary).
- Project-local `tmp/` for scratch files. Never `/tmp/`. Clean up tmp files when done.
- Never redirect stderr to `/dev/null`.
- Never use `-H` with `ssh-keyscan`.
