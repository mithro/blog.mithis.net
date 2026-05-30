# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Jekyll-built blog at https://blog.mithis.net, replacing the legacy WordPress install of the same domain. As of 2026-05-30 the cutover is **fully live**: DNS resolves to GitHub Pages (185.199.108-111.153), a valid Let's Encrypt cert is issued for `blog.mithis.net`, and `https_enforced` is on. The WordPress source the site was originally mirrored from is retired — blog.mithis.net IS this repo's build.

The migration phase is complete (175/185 pages were literally pixel-perfect against the WordPress original, remainder under 0.012%). Day-to-day work is **issue-driven cleanup and new authoring**:

- Open issues are tracked at https://github.com/mithro/blog.mithis.net/issues — they list the residual cleanup work (broken Picasa galleries, dead Twitter widget, contact-page rewrite, mobile polish, etc.).
- For new posts follow `docs/AUTHORING.md`.

### Reverting the cutover (if DNS / cert ever breaks)

If something forces a fallback to the mithro.github.io staging URL:

1. `_config.yml`: `baseurl: "/blog.mithis.net"` and `url: "https://mithro.github.io"`.
2. Delete `CNAME`.
3. Push — site goes back to https://mithro.github.io/blog.mithis.net/ staging mode.

`_plugins/baseurl_asset_paths.rb` is kept around dormant for exactly this case — it rewrites raw-HTML asset paths in post bodies to include the baseurl prefix when one is set.

### Core directive (evolved)

The original 2026-05-21 directive was: *"The github version should be faithful to the current live https://blog.mithis.net — broken stuff and all"*. That held throughout the migration phase.

As of 2026-05-30 the user has explicitly moved past fidelity: they want broken things FIXED, not preserved. Open issues #9–#25 are the cleanup backlog. **When you see something broken, file or fix it; don't preserve it as a "live-fidelity" artifact.** Visual-design credits (the Barthelme theme designer Scott Allan Wallick) stay; engine credits and dead links go — see [[keep-theme-designer-credit]] in auto-memory.

## Build, serve, deploy

```bash
# Build (production env so SCSS etc compile right)
JEKYLL_ENV=production bundle3.3 exec jekyll build

# Local serve
cd _site && uv run python -m http.server 8731

# Push to deploy (GitHub Actions builds + publishes)
git push origin main

# After EVERY push, verify CI passed and the site re-deployed before claiming a fix is live:
gh run list --limit 1
```

`bundle3.3` (not bare `bundle`) is the right Ruby 3.3 bundler for this repo's Gemfile.lock.

GitHub Pages must use the **GitHub Actions builder** (not the legacy branch builder) so custom plugins run — see `.github/workflows/jekyll.yml`. The legacy builder would silently skip `_plugins/` and produce a broken build.

## Content lint (raw HTML rule)

`scripts/fidelity/lint_content.py` enforces "no hardcoded block HTML in posts". Inline HTML (`<a>`, `<code>`, `<em>`, `<img>`, etc.) is fine. Block HTML (`<div>`, `<object>`, `<table>`, `<p>` etc.) requires an opt-out sentinel:

```
<!-- fidelity-allow: BLOCK_HTML necessary-embed — <reason> -->
{::nomarkdown}
<p><object …></object></p>
{:/nomarkdown}
```

**Critical:** the sentinel must be on the SAME line as the BLOCK_HTML or the IMMEDIATELY PRECEDING line. Wrapping with `{::nomarkdown}` in between would push the sentinel two lines away → CI fail. (This bit 17 commits silently before being caught.)

Run with: `uv run python -m scripts.fidelity.lint_content _posts --asset-root .`

## Plugin architecture (`_plugins/`)

- **`python_token_overrides.rb`** — Jekyll `post_render` hook that rewrites Rouge-emitted HTML inside `.language-python` / `.language-bash` code blocks to match live's WP-Syntax (GeSHi) output:
  - Per-token color overrides (commas → light green `#66cc66`, `%` operator → inherit, etc.)
  - Span splitting for merged punctuation (`<span class="p">],</span>` → `,` gets its own green span)
  - Pre-styling for module-name patterns (`from cStringIO import` → cStringIO crimson)
  - Stripping of plain `.n` (Name) and `.sa` (string affix) spans to match live's unwrapped text
  - Inserting `\X` escape highlighting inside raw-string `.s` spans
  - Bash-specific overrides (`/` paths bold-black, `;;` bold-black, `$VAR` in `"…"` red)

  The plugin runs after Rouge produces its HTML, so it edits HTML — it does NOT change Rouge's lexer. Patterns and reasoning are documented inline. Since #25, Rouge now wraps each block in a `<table class="rouge-table">` with `.rouge-gutter` (line numbers) and `.rouge-code` columns; the plugin's regex passes still apply because the inner span structure is unchanged.

- **`baseurl_asset_paths.rb`** — dormant post-cutover (only fires when `site.baseurl` is non-empty). Rewrites raw-HTML asset paths in post bodies to prepend the baseurl. Kept for the revert recipe above.

## Code-block line numbers (since #25)

Enabled site-wide via `_config.yml`:

```yaml
kramdown:
  syntax_highlighter_opts:
    block:
      line_numbers: true
      start_line: 1
```

Rouge emits table mode: `<td class="rouge-gutter">` holds the line numbers, `<td class="rouge-code">` holds the code. CSS for the gutter (`assets/css/main.css`, near the `.language-python.highlighter-rouge` block) sets `user-select: none` so the numbers are excluded from copy-paste. This is a deliberate divergence from live's WP-Syntax rendering.

## Auto-generated sidebar widgets (since #17/#18)

`_includes/sidebar.html` generates the **tags cloud** and **categories dropdown** from data instead of hardcoded HTML:

- **Tags cloud:** iterates `site.pages | where: "layout", "tag"`, looks up `site.tags[tag_name] | size` for the count, scales font-size 8pt→22pt linearly. Picks up all on-disk tag pages.
- **Categories dropdown:** iterates `site.pages | where: "layout", "category"`, looks up `site.categories[cat_slug] | size`. The onChange handler is `if(this.value && this.value != '-1') { window.location.href = this.value; }` — replaced the prior `if(this.value > 0)` which always evaluated NaN > 0 → false and never navigated.

The hierarchy display (sub-categories indented under parents) was dropped — sub-cats appear flat in their alphabetical position. To restore hierarchy, add a `parent_cat:` field to sub-category page frontmatter and group at render time.

## Critical files & invariants

- **`_layouts/default.html` starts with `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" …>`** — XHTML 1.0 Transitional triggers Chromium's *almost-standards mode* which matches the live blog's rendering. Do not change to HTML5 doctype; it breaks rendering across all pages.
- **`assets/css/main.css`** is the main stylesheet. Plain CSS (not SCSS). Many token-color overrides live here scoped to `.language-python .highlight .X` selectors. Inline comments explain WHY each rule exists (with `Live's GeSHi …` references).
- **Galleries are PINNED** (deterministic) for both the header and sidebar — commits 341a44c, 757ec74, d174bac. Don't randomize them (and they're all broken Picasa thumbnails tracked in #10/#11 — to be removed/replaced, not "fixed in place").

## Pixel-diff tools (now mostly historical)

The diff tools in `tmp/` (sweep_deployed.py, batch_pixdiff.py, listing_diff_all.py, diff_mask.py, etc.) were the workhorses of the migration's pixel-perfect push. They compare local/deployed against `https://blog.mithis.net` (the live WordPress).

Post-cutover, the live WordPress is being retired — the diff tools no longer have a separate "live source of truth" to diff against. They remain useful for **regression detection** (build A vs build B of the Jekyll site), but the "match live WordPress pixel-for-pixel" workflow is over.

The breakthrough viz `diff_mask.py` (red pixels on white where builds differ) is still the right tool when a CSS change might have regressed something — diff before/after builds.

## Git workflow

- `origin` is `git+ssh://github.com/mithro/blog.mithis.net`. Push to it directly.
- Commit messages should explain WHY. During the cleanup phase, that "why" usually points at a GitHub issue (`Closes #N`). End commit messages with `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- GitHub's auto-close keyword only catches the FIRST `#N` reference in a multi-issue commit like `Closes #14, #15, #16` — close the rest manually with `gh issue close N`.
- **Always check CI after pushing:** `gh run list --limit 1`. A green CI is necessary, not sufficient — also verify the change is actually live (`curl -s https://blog.mithis.net/<path>` or a Playwright screenshot).

## Auto-memory location

`/home/tim/.claude/projects/-home-tim-github-mithro-blog-mithis-net/memory/` holds session-spanning notes. The `MEMORY.md` index there is the entry point. Key memories: the [[keep-theme-designer-credit]] rule (distinguish engine credits from visual-design credits when cleaning up), the [[check-ci-and-deployment]] reminder.

## Common pitfalls

- **Bare `bundle exec`** — uses the wrong Ruby. Use `bundle3.3 exec`.
- **GitHub auto-close only catches the first issue reference.** "Closes #14, #15, #16" only closes #14 automatically; manually close the rest with `gh issue close`.
- **`onchange="if(this.value > 0) …"` is broken for URL values** — string > 0 is always NaN > 0 = false. Use explicit string compare against the placeholder option's value.
- **Stale screenshots in `tmp/`** — diff/screenshot scripts overwrite the same paths. Re-run after every build.
- **Stderr redirection (`2>/dev/null`) is blocked** by a hook — keep stderr visible.
- **Inline `python -c "..."` is blocked** by a hook — write to a tmp script file and run that instead.
