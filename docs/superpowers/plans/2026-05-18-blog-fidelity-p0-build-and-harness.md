# Blog Fidelity P0 — Build Gate + Verification Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. TDD tasks: use @superpowers:test-driven-development. Before claiming P0 done: use @superpowers:verification-before-completion.

**Goal:** Establish a green, reproducible Jekyll build and an automated, testable fidelity-measurement harness that becomes the objective oracle driving every later phase (P1–P6).

**Architecture:** A clean Jekyll build (proper `exclude:`, pinned toolchain) plus a small single-responsibility Python package `scripts/fidelity/` (run via `uv`): a build gate, a content linter, a Barthelme structural extractor, a structural comparator, a Wayback fetcher, a Playwright renderer, and a report assembler — orchestrated into one `fidelity-report.md`. Pure-logic components are TDD'd; integration components have explicit run/verify steps. Structural diff + content linter are the CI-able authoritative gates; Playwright screenshots are a local/manual visual layer (per spec §6.2).

**Tech Stack:** Ruby/Jekyll 4.4 + Bundler; Python 3 via `uv` (pytest, beautifulsoup-free stdlib `html.parser`, Playwright Python for the local visual layer); GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-05-18-blog-fidelity-completion-design.md`

**P0 EXIT GATE (precise):** P0 is *not* "all fidelity passes." P0 is done when: (a) `bundle exec jekyll build` is clean — zero errors/warnings; (b) the harness runs end-to-end and writes `tmp/fidelity/fidelity-report.md`; (c) the content linter and structural comparator are operational and unit-tested. The gaps the report surfaces are the *inputs* to P1/P2 and are expected to be non-empty at P0.

**Local environment note (execution machine):** This Debian box ships Bundler only as `bundle3.3` (no `bundle` on PATH); a global PATH shim is out of scope. Therefore: (a) harness code (`build.py`, `run.py`) resolves the bundler at runtime via `shutil.which("bundle") or shutil.which("bundle3.3")` — portable across machines and CI; (b) for manual shell steps in this plan, if `bundle` is absent substitute `bundle3.3` (e.g. `bundle3.3 exec jekyll build`). CI is unaffected (`ruby/setup-ruby` provides `bundle`).

---

## File Structure

Created by this plan:

- `.ruby-version` — pin Ruby for local/CI parity (build reproducibility).
- `pyproject.toml` — `uv`/pytest config for the harness (repo root; excluded from Jekyll).
- `scripts/__init__.py`, `scripts/fidelity/__init__.py` — make the harness importable.
- `scripts/fidelity/archetypes.py` — the single source of truth for the archetype set.
- `scripts/fidelity/build.py` — Jekyll build gate (problem detector + wrapper).
- `scripts/fidelity/lint_content.py` — content linter (Liquid leak, block HTML, missing images). Reused as the P5 build-time guard.
- `scripts/fidelity/barthelme.py` — extract structural anchors from Barthelme `.php`.
- `scripts/fidelity/compare.py` — structural containment diff (Barthelme → Jekyll DOM).
- `scripts/fidelity/wayback.py` — resolve best Wayback snapshot URL.
- `scripts/fidelity/render.py` — Playwright Python archetype renderer (local visual layer).
- `scripts/fidelity/report.py` — assemble `fidelity-report.md`.
- `scripts/fidelity/run.py` — orchestrator + CLI entrypoint (the P0 exit-gate runner).
- `tests/__init__.py`, `tests/fidelity/__init__.py`, `tests/fidelity/test_*.py` — unit tests.

Modified by this plan:

- `_config.yml` — add `exclude:` so the build is clean.
- `.gitignore` — ignore `tmp/`.
- `.github/workflows/jekyll.yml` — consume `.ruby-version` (local/CI parity).
- `Gemfile.lock` — refreshed/pinned by `bundle install`.

**Containment model (used by `compare.py`, applies to P1):** Jekyll output PASSES structural diff for an archetype when it contains *every* structural anchor (`tag#id`, `tag.class`) present in the static portions of the corresponding Barthelme `.php`. Jekyll may contain *extra* anchors (it will — e.g. the header gallery) without failing. Known-justified omissions go in an explicit `ignore` set with a comment. This operationalizes "structural fidelity" tolerantly of dynamic PHP while strictly preserving original structure.

---

## Task 1: Reproducible toolchain (Ruby pin + Bundler + CI parity)

**Files:**
- Create: `.ruby-version`
- Modify: `.github/workflows/jekyll.yml`
- Modify: `Gemfile.lock` (via `bundle install`)

- [ ] **Step 1: Pin Ruby**

Create `.ruby-version` containing exactly:

```
3.3.8
```

(Local interpreter is Ruby 3.3.8; Jekyll 4.4 supports it. `ruby/setup-ruby` reads `.ruby-version`, giving local/CI parity.)

- [ ] **Step 2: Install the Jekyll toolchain**

Run: `bundle install`
Expected: resolves `jekyll ~> 4.4.1`, `webrick`, `jekyll-paginate`, `jekyll-feed`, `jekyll-sitemap`; ends with `Bundle complete!`. If `Gemfile.lock` changes, that is expected (pinning).

- [ ] **Step 3: Make CI consume the pin**

In `.github/workflows/jekyll.yml`, change the Setup Ruby step to drop the hardcoded version so it uses `.ruby-version`:

```yaml
      - name: Setup Ruby
        # https://github.com/ruby/setup-ruby/releases/tag/v1.207.0
        uses: ruby/setup-ruby@4a9ddd6f338a97768b8006bf671dfbad383215f4
        with:
          bundler-cache: true # runs 'bundle install' and caches installed gems automatically
          cache-version: 0 # Increment this number if you need to re-download cached gems
```

(Removed `ruby-version: '3.1'` — `.ruby-version` now governs. **Do NOT** touch the `--baseurl` line here; that is P4's job, deliberately out of P0 scope.)

- [ ] **Step 4: Verify Jekyll runs**

Run: `bundle exec jekyll --version`
Expected: `jekyll 4.4.x`

- [ ] **Step 5: Commit**

```bash
git add .ruby-version .github/workflows/jekyll.yml Gemfile.lock
git commit -m "P0: pin Ruby via .ruby-version for local/CI build parity"
```

---

## Task 2: Clean build — Jekyll `exclude:`

Jekyll currently has no `exclude:`, so it copies/processes `scripts/`, `docs/`, `exports/`, `theme_analysis/`, `*.py`, migration `*.json`/`*.md` into `_site`, producing noise/warnings. The build gate cannot be clean until this is fixed.

**Files:**
- Modify: `_config.yml`
- Modify: `.gitignore`

- [ ] **Step 1: Ignore tmp/**

Append to `.gitignore`:

```
tmp/
```

- [ ] **Step 2: Add an explicit exclude list**

In `_config.yml`, replace the commented-out `# exclude:` block with this concrete list (top-level site pages `about.markdown`, `archives.md`, `contact.md`, `projects.md`, `tutorials.md` are deliberately NOT excluded):

```yaml
exclude:
  - scripts/
  - tests/
  - tmp/
  - docs/
  - exports/
  - theme_analysis/
  - .github/
  - vendor/
  - node_modules/
  - Gemfile
  - Gemfile.lock
  - pyproject.toml
  - uv.lock
  - setup-tools.sh
  - test_migration.sh
  - debug_posts.py
  - CLAUDE.md
  - MIGRATION_PLAN.md
  - MIGRATION_TODO.md
  - BARTHELME_SOURCE_ANALYSIS.md
  - BARTHELME_THEME_ANALYSIS.md
  - URL_STRUCTURE_COMPARISON.md
  - URL_VERIFICATION_REPORT.md
  - WORDPRESS_EXPORT_STRATEGY.md
  - migration_status.json
  - all_post_urls.json
  - checkpoint_10.json
  - checkpoint_20.json
  - checkpoint_30.json
  - checkpoint_40.json
  - checkpoint_50.json
```

- [ ] **Step 3: Build and inspect for leaks**

Run: `bundle exec jekyll build --trace`
Expected: completes; `done in N seconds`.

Run: `ls _site | sort`
Expected: NO `scripts`, `docs`, `exports`, `theme_analysis`, `tests`, `tmp`, `*.py`, migration `*.md`/`checkpoint_*.json` present. Site dirs (`archives` or `category`, `about`, `feed.xml`, `assets`, ...) ARE present.

- [ ] **Step 4: Patch any remaining leak**

If Step 3 shows leaked files, add each offending top-level path to the `exclude:` list and re-run Step 3 until clean. Record what you added.

- [ ] **Step 5: Commit**

```bash
git add _config.yml .gitignore
git commit -m "P0: exclude non-site files from Jekyll build for a clean _site"
```

---

## Task 2A: Resolve category-feed build conflicts (clean-build prerequisite)

**Discovered during execution.** `bundle exec jekyll build` emits 19 `Conflict:`
warnings — each `category/<cat>/feed.xml` (front matter `permalink:
/category/<cat>/feed/`) is registered **twice**, both writing
`_site/category/<cat>/feed/index.xml` ("written file may end up with unexpected
contents" → nondeterministic `_site`). A nondeterministic build is fatal for a
fidelity baseline, so this MUST be clean before the harness measures anything.
This is sequenced after Task 2 (it completes "make the build clean") and before
Task 3; the Python scaffold/TDD tasks do not depend on it, but Task 8/Task 12
(build gate / exit gate) do.

**Files:** likely the 19 `category/*/feed.xml`; possibly `_config.yml`. Dead
code `_layouts/category_feed.xml` / `_includes/category-feed.xml` may be
involved — investigate before touching.

**Hard constraints (fidelity-preserving):**
- Each of the 19 categories MUST still produce exactly one feed at the SAME
  output URL (`/category/<cat>/feed/` → `_site/category/<cat>/feed/index.xml`)
  with the same rendered RSS content. Do NOT delete category feeds, change their
  URLs, or switch to jekyll-feed category generation (URL change = P1 fidelity
  regression introduced by P0).
- Minimal change: eliminate only the double-registration. Do not restructure the
  category system or touch posts/layouts beyond what removes the conflict.
- If `_layouts/category_feed.xml` and `_includes/category-feed.xml` are provably
  unreferenced dead code, removing them is in scope ONLY if it is part of the
  actual fix; otherwise leave them and note them for P1 cleanup.

- [ ] **Step 1: Diagnose the double-registration**

Run from the worktree: `bundle3.3 exec jekyll build --trace 2>&1 | grep -A4 "Conflict:" | sed 's/\x1b\[[0-9;]*m//g' | head -20`. Inspect a sample `category/<cat>/feed.xml` front matter and a sibling `category/<cat>.md`. Determine WHY Jekyll lists the one source file twice (e.g. trailing-slash `permalink` on a `.xml` file producing an ambiguous directory/file destination, a `defaults:` rule, or a duplicate generation path). State the root cause in your report before changing anything.

- [ ] **Step 2: Apply the minimal fidelity-preserving fix**

Apply the smallest change that makes Jekyll register each category feed exactly once at the same destination URL. (Likely candidate: give each feed an explicit unambiguous `permalink` such as `/category/<cat>/feed/index.xml`, or remove whichever single source is the duplicate — whichever your Step 1 diagnosis proves is correct. Preserve the `/category/<cat>/feed/` browser URL.)

- [ ] **Step 3: Verify zero conflicts, feeds intact, no regression**

```
bundle3.3 exec jekyll build --trace 2>&1 | grep -c "Conflict:"        # MUST print 0
bundle3.3 exec jekyll build --trace 2>&1 | grep -ciE "error|warning|Deprecation"   # no new problems
```
Then assert every category feed still exists and is non-empty RSS, e.g.:
`for d in category/*/; do c=$(basename "$d"); test -s "_site/category/$c/feed/index.xml" || echo "MISSING $c"; done` → no MISSING output.
Also confirm overall `_site` HTML page set is unchanged vs before the fix (capture `find _site -name '*.html' | wc -l` before and after; counts must match) and that `_site/category/<cat>/index.html` archive pages still exist.

- [ ] **Step 4: Commit**

```bash
git add -A
git -c commit.gpgsign=false commit -m "P0: fix category-feed destination conflicts for a deterministic build

<one-line root cause>. Each category still emits one feed at the same
/category/<cat>/feed/ URL; no _site regression.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

**Exit gate for 2A:** `grep -c "Conflict:"` on a fresh build prints `0`; all 19
category feeds present and non-empty at the unchanged URL; `_site` HTML page
count unchanged; no new errors/warnings/deprecations.

---

## Task 3: Python harness scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `scripts/__init__.py` (empty), `scripts/fidelity/__init__.py` (empty)
- Create: `tests/__init__.py` (empty), `tests/fidelity/__init__.py` (empty)

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "blog-fidelity-harness"
version = "0.1.0"
description = "Fidelity verification harness for the blog.mithis.net Jekyll migration"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = ["pytest>=8", "playwright>=1.44"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
markers = [
  "integration: needs a built site, network, or a browser (deselect with -m 'not integration')",
]
```

- [ ] **Step 2: Create the package marker files**

Create the four empty `__init__.py` files listed above.

- [ ] **Step 3: Verify the toolchain**

Run: `uv run pytest -q`
Expected: `no tests ran` (exit 5) — confirms `uv` resolves the env and pytest is wired. (Adding `--co` is fine too.)

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml scripts/__init__.py scripts/fidelity/__init__.py tests/__init__.py tests/fidelity/__init__.py
git commit -m "P0: scaffold uv/pytest fidelity-harness package"
```

---

## Task 4: `archetypes.py` — the defined archetype set (TDD)

Use @superpowers:test-driven-development.

**Files:**
- Create: `scripts/fidelity/archetypes.py`
- Test: `tests/fidelity/test_archetypes.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_archetypes.py
from scripts.fidelity.archetypes import (
    ARCHETYPES, EXCLUDED_BARTHELME_TEMPLATES, structural_archetypes,
)

def test_structural_archetypes_map_to_php_templates():
    for a in structural_archetypes():
        assert a.barthelme_template.endswith(".php"), a

def test_feed_is_present_but_not_structural():
    feed = next(a for a in ARCHETYPES if a.name == "feed")
    assert feed.structural is False

def test_excluded_templates_disjoint_from_used():
    used = {a.barthelme_template for a in ARCHETYPES if a.barthelme_template}
    assert used.isdisjoint(EXCLUDED_BARTHELME_TEMPLATES)

def test_post_archetype_uses_a_real_permalink():
    post = next(a for a in ARCHETYPES if a.name == "post")
    assert post.path == "/archives/hardware/2186-nmigen-new-improved-by-whitequark"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_archetypes.py -q`
Expected: FAIL — `ModuleNotFoundError: scripts.fidelity.archetypes`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/archetypes.py
"""Single source of truth for the page archetypes the harness verifies."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Archetype:
    name: str
    path: str                # URL path on the served Jekyll site
    barthelme_template: str  # reference .php in theme_analysis/barthelme/ ("" = none)
    structural: bool         # participates in the structural diff gate

# Stable representative pages. The post is the 2020 nMigen post (exists, fixed slug).
ARCHETYPES: tuple[Archetype, ...] = (
    Archetype("home",     "/",                                                        "index.php",   True),
    Archetype("post",     "/archives/hardware/2186-nmigen-new-improved-by-whitequark", "single.php",  True),
    Archetype("category", "/category/hardware/",                                       "archive.php", True),
    Archetype("page",     "/about/",                                                   "page.php",    True),
    Archetype("notfound", "/404.html",                                                 "404.php",     True),
    Archetype("search",   "/search.html",                                              "search.php",  True),
    Archetype("feed",     "/feed.xml",                                                 "",            False),
)

# Barthelme templates deliberately OUT of scope for the structural diff (spec §6.2):
# no equivalent live surface in this blog.
EXCLUDED_BARTHELME_TEMPLATES = frozenset(
    {"archives.php", "attachment.php", "image.php", "links.php", "sitemap.php"}
)

def structural_archetypes() -> tuple[Archetype, ...]:
    return tuple(a for a in ARCHETYPES if a.structural)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_archetypes.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Sanity-check the paths exist as sources**

Run: `ls about.markdown search.html 404.html feed.xml category/hardware.md theme_analysis/barthelme/index.php theme_analysis/barthelme/single.php theme_analysis/barthelme/archive.php theme_analysis/barthelme/page.php theme_analysis/barthelme/404.php theme_analysis/barthelme/search.php`
Expected: all listed (no "No such file"). If `category/hardware.md` differs, adjust the category archetype path to a category page that exists.

- [ ] **Step 6: Commit**

```bash
git add scripts/fidelity/archetypes.py tests/fidelity/test_archetypes.py
git commit -m "P0: define verified archetype set with scope boundary"
```

---

## Task 5: `lint_content.py` — content linter (TDD)

Use @superpowers:test-driven-development. This is the highest-value component: it drives P2 and is reused as the P5 hardcoded-HTML build guard.

**Files:**
- Create: `scripts/fidelity/lint_content.py`
- Test: `tests/fidelity/test_lint_content.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_lint_content.py
from pathlib import Path
from scripts.fidelity.lint_content import lint_text, Finding

FM = "---\ntitle: x\nlayout: post\n---\n"

def codes(findings): return sorted(f.code for f in findings)

def test_clean_markdown_has_no_findings():
    assert lint_text("p.md", FM + "Just **markdown** and a [link](https://x).\n") == []

def test_detects_liquid_leak():
    f = lint_text("p.md", FM + "Oops {{ page.title }} leaked\n")
    assert "LIQUID_LEAK" in codes(f)

def test_detects_block_html():
    f = lint_text("p.md", FM + "<div class='x'>nope</div>\n")
    assert "BLOCK_HTML" in codes(f)

def test_allows_inline_html():
    f = lint_text("p.md", FM + 'Use <abbr title="y">Y</abbr> and <code>z</code>.\n')
    assert f == []

def test_ignores_fenced_code_blocks():
    body = FM + "```\n<div>{{ not_real }}</div>\n```\n"
    assert lint_text("p.md", body) == []

def test_front_matter_is_not_scanned_for_html():
    assert lint_text("p.md", "---\nexcerpt: <p>x</p>\n---\nclean\n") == []

def test_missing_local_image(tmp_path: Path):
    (tmp_path / "assets").mkdir()
    f = lint_text("p.md", FM + "![a](/assets/missing.png)\n", asset_root=tmp_path)
    assert "MISSING_IMAGE" in codes(f)

def test_present_local_image_ok(tmp_path: Path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "ok.png").write_bytes(b"x")
    f = lint_text("p.md", FM + "![a](/assets/ok.png)\n", asset_root=tmp_path)
    assert f == []

def test_remote_image_not_flagged(tmp_path: Path):
    f = lint_text("p.md", FM + "![a](https://lh3.ggpht.com/x.jpg)\n", asset_root=tmp_path)
    assert f == []

def test_finding_has_line_number():
    f = lint_text("p.md", FM + "line1\n{{ bad }}\n")
    leak = [x for x in f if x.code == "LIQUID_LEAK"][0]
    assert leak.line == 6  # 4 FM lines + "line1" + the leak
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_lint_content.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/lint_content.py
"""Lint committed post content: no Liquid leakage, no hardcoded block HTML,
no missing local images. Encodes the spec's 'no hardcoded structural HTML' rule.
Inline HTML (a, abbr, code, em, strong, sup, sub, br, img, span, kbd, q, cite,
del, ins, mark, time) is allowed where Markdown can't express the original."""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

_BLOCK_HTML = re.compile(
    r"</?(?:div|section|article|header|footer|nav|aside|main|table|thead|tbody|"
    r"tfoot|tr|td|th|ul|ol|li|dl|dt|dd|h[1-6]|p|figure|figcaption|blockquote|"
    r"pre|form|fieldset|iframe|script|style|center|font|object|embed)\b",
    re.IGNORECASE,
)
_LIQUID = re.compile(r"\{\{|\{%")
_MD_IMG = re.compile(r"!\[[^\]]*\]\(\s*([^)\s]+)")
_HTML_IMG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.IGNORECASE)

def _split_front_matter(text: str) -> tuple[int, str]:
    """Return (1-based line where body starts, body text)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            if nl != -1:
                prefix = text[: nl + 1]
                return prefix.count("\n") + 1, text[nl + 1 :]
    return 1, text

def _check_image(path, lineno, src, asset_root, out):
    if src.startswith(("http://", "https://", "//", "data:", "mailto:")):
        return
    if asset_root is None:
        return
    rel = src.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    if rel and not (Path(asset_root) / rel).exists():
        out.append(Finding(path, lineno, "MISSING_IMAGE",
                            f"Local image not found: {src}"))

def lint_text(path: str, text: str, *, asset_root: Path | None = None) -> list[Finding]:
    out: list[Finding] = []
    body_start, body = _split_front_matter(text)
    in_fence = False
    for i, raw in enumerate(body.splitlines()):
        lineno = body_start + i
        s = raw.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _LIQUID.search(raw):
            out.append(Finding(path, lineno, "LIQUID_LEAK",
                               "Unrendered Liquid ({{ or {%) in committed content"))
        if _BLOCK_HTML.search(raw):
            out.append(Finding(path, lineno, "BLOCK_HTML",
                               "Hardcoded block-level HTML; express this in Markdown"))
        for m in _MD_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
        for m in _HTML_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
    return out

def lint_paths(paths, *, asset_root: Path | None = None) -> list[Finding]:
    out: list[Finding] = []
    for p in paths:
        p = Path(p)
        out.extend(lint_text(str(p), p.read_text(encoding="utf-8"),
                             asset_root=asset_root))
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_lint_content.py -q`
Expected: PASS (10 passed)

- [ ] **Step 5: Smoke-run against real posts (informational, do not fix here)**

Run: `uv run python -c "from scripts.fidelity.lint_content import lint_paths; import glob; fs=lint_paths(sorted(glob.glob('_posts/*.md')), asset_root='.'); print(len(fs),'findings'); [print(f) for f in fs[:20]]"`
Expected: prints a finding count + sample. Non-zero is EXPECTED — this is the P2 worklist, recorded later by the report. Do **not** fix posts in P0.

- [ ] **Step 6: Commit**

```bash
git add scripts/fidelity/lint_content.py tests/fidelity/test_lint_content.py
git commit -m "P0: content linter (Liquid leak / block HTML / missing image)"
```

---

## Task 6: `barthelme.py` — structural anchor extractor (TDD)

Use @superpowers:test-driven-development.

**Files:**
- Create: `scripts/fidelity/barthelme.py`
- Test: `tests/fidelity/test_barthelme.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_barthelme.py
from pathlib import Path
from scripts.fidelity.barthelme import strip_php, extract_anchors, Anchor

def test_strip_php_removes_blocks():
    assert "<?php" not in strip_php("<div><?php echo $x; ?></div>")
    assert "<?=" not in strip_php("<a><?= $y ?></a>")

def test_extracts_id_and_class_anchors():
    a = extract_anchors('<div id="wrapper"><p class="entry-content alt">x</p></div>')
    assert Anchor("div", "#wrapper") in a
    assert Anchor("p", ".entry-content") in a
    assert Anchor("p", ".alt") in a

def test_skips_php_generated_attribute_values():
    a = extract_anchors('<body class="<?php barthelme_body_class(); ?>">x</body>')
    assert all(an.tag != "body" for an in a)  # dynamic class => no static anchor

def test_real_single_php_has_known_anchors():
    php = Path("theme_analysis/barthelme/single.php").read_text(encoding="utf-8",
                                                                 errors="replace")
    anchors = extract_anchors(php)
    # single.php wraps the post; entry-content is the canonical Barthelme hook.
    assert any(an.ident == ".entry-content" for an in anchors)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_barthelme.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/barthelme.py
"""Extract structural anchors (tag#id, tag.class) from the static portions of a
Barthelme PHP template. PHP blocks are stripped; attribute values containing PHP
are treated as dynamic and produce no static anchor."""
from __future__ import annotations
import re
from dataclasses import dataclass
from html.parser import HTMLParser

_PHP = re.compile(r"<\?php.*?\?>", re.DOTALL)
_PHP_ECHO = re.compile(r"<\?=.*?\?>", re.DOTALL)

@dataclass(frozen=True, order=True)
class Anchor:
    tag: str
    ident: str  # "#id" or ".class"

class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[Anchor] = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cid = d.get("id")
        if cid and "<?" not in cid:
            self.anchors.add(Anchor(tag, f"#{cid.strip()}"))
        cls = d.get("class")
        if cls and "<?" not in cls:
            for c in cls.split():
                if c:
                    self.anchors.add(Anchor(tag, f".{c}"))

def strip_php(php_text: str) -> str:
    return _PHP_ECHO.sub("", _PHP.sub("", php_text))

def extract_anchors(php_text: str) -> set[Anchor]:
    c = _Collector()
    c.feed(strip_php(php_text))
    return c.anchors

def anchors_in_html(html: str) -> set[Anchor]:
    c = _Collector()
    c.feed(html)
    return c.anchors
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_barthelme.py -q`
Expected: PASS (4 passed). If `test_real_single_php_has_known_anchors` fails, inspect `theme_analysis/barthelme/single.php` for the actual canonical class and update the assertion to the real anchor (record what you found) — the extractor is correct; the fixture expectation must match reality.

- [ ] **Step 5: Commit**

```bash
git add scripts/fidelity/barthelme.py tests/fidelity/test_barthelme.py
git commit -m "P0: Barthelme structural-anchor extractor"
```

---

## Task 7: `compare.py` — structural containment diff (TDD)

Use @superpowers:test-driven-development.

**Files:**
- Create: `scripts/fidelity/compare.py`
- Test: `tests/fidelity/test_compare.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_compare.py
from scripts.fidelity.compare import structural_diff, StructuralResult
from scripts.fidelity.barthelme import Anchor

def test_pass_when_jekyll_contains_all_barthelme_anchors():
    php = '<div id="wrapper"><div class="entry-content">x</div></div>'
    html = '<div id="wrapper"><div class="entry-content"><p>hi</p></div></div>'
    r = structural_diff("post", php, html)
    assert r.passed and r.missing == ()

def test_extra_jekyll_anchors_do_not_fail():
    php = '<div id="wrapper"></div>'
    html = '<div id="wrapper"><div id="header-photos">gallery</div></div>'
    assert structural_diff("home", php, html).passed

def test_missing_anchor_fails_and_is_reported():
    php = '<div id="wrapper"><div id="sidebar">s</div></div>'
    html = '<div id="wrapper"></div>'
    r = structural_diff("home", php, html)
    assert not r.passed
    assert Anchor("div", "#sidebar") in r.missing

def test_ignore_set_suppresses_known_omissions():
    php = '<div id="wrapper"><div id="wp-only">w</div></div>'
    html = '<div id="wrapper"></div>'
    r = structural_diff("home", php, html, ignore={Anchor("div", "#wp-only")})
    assert r.passed
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_compare.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/compare.py
"""Structural containment diff: Jekyll output must contain every structural
anchor present in the corresponding Barthelme template. Extra Jekyll anchors are
allowed. See plan 'Containment model'."""
from __future__ import annotations
from dataclasses import dataclass
from .barthelme import Anchor, extract_anchors, anchors_in_html

@dataclass(frozen=True)
class StructuralResult:
    archetype: str
    missing: tuple[Anchor, ...]
    @property
    def passed(self) -> bool:
        return not self.missing

def structural_diff(archetype: str, barthelme_php: str, jekyll_html: str,
                    *, ignore: frozenset[Anchor] | set[Anchor] = frozenset()
                    ) -> StructuralResult:
    expected = extract_anchors(barthelme_php) - set(ignore)
    actual = anchors_in_html(jekyll_html)
    missing = tuple(sorted(expected - actual))
    return StructuralResult(archetype, missing)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_compare.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/fidelity/compare.py tests/fidelity/test_compare.py
git commit -m "P0: structural containment comparator"
```

---

## Task 8: `build.py` — Jekyll build gate (TDD for the detector + integration wrapper)

Use @superpowers:test-driven-development for Step 1–4 (pure detector). Steps 5–7 integration-verify the wrapper.

**Files:**
- Create: `scripts/fidelity/build.py`
- Test: `tests/fidelity/test_build.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_build.py
from scripts.fidelity.build import detect_problems, bundler

GOOD = """Configuration file: /x/_config.yml
            Source: /x
       Destination: /x/_site
      Generating...
                    done in 3.2 seconds.
"""

def test_clean_log_has_no_problems():
    assert detect_problems(GOOD) == []

def test_liquid_exception_is_a_problem():
    log = GOOD + "Liquid Exception: Liquid syntax error (line 3): Unknown tag\n"
    assert detect_problems(log)

def test_deprecation_is_a_problem():
    assert detect_problems("Deprecation: pagination is now a plugin\n")

def test_jekyll_error_prefix_is_a_problem():
    assert detect_problems("  Error: could not read file foo: bar\n")

def test_normal_generating_line_is_not_a_problem():
    assert detect_problems("      Generating... \n                    done.\n") == []

def test_jekyll_conflict_is_a_problem():
    log = "          Conflict: The following destination is shared by multiple files.\n"
    assert detect_problems(log)

def test_bundler_resolves_to_a_command():
    # Debian ships 'bundle3.3'; most machines/CI ship 'bundle'. Either is fine.
    assert bundler()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_build.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/build.py
"""Jekyll build gate. detect_problems() is pure and unit-tested; run_build()
wraps the same command CI runs and fails on any detected problem."""
from __future__ import annotations
import re
import shutil
import subprocess

# Jekyll's actual problem signatures (avoid matching benign "Generating..." etc.)
_PROBLEM = re.compile(
    r"(Liquid (Exception|Warning|syntax error))"
    r"|(^\s*Error:)"
    r"|(^\s*jekyll \d.*Error)"
    r"|(Deprecation:)"
    r"|(\bwarning:\s)"
    r"|(Build Warning:)"
    r"|(Conflict:)",
    re.IGNORECASE | re.MULTILINE,
)

def detect_problems(log: str) -> list[str]:
    return [ln.strip() for ln in log.splitlines() if _PROBLEM.search(ln)]

def bundler() -> str:
    """Resolve the Bundler executable. Debian names it 'bundle3.3'; most
    machines and CI provide 'bundle'. Portable across both."""
    return shutil.which("bundle") or shutil.which("bundle3.3") or "bundle"

def run_build(baseurl: str = "") -> tuple[bool, str]:
    cmd = [bundler(), "exec", "jekyll", "build", "--trace"]
    if baseurl:
        cmd += ["--baseurl", baseurl]
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = (p.stdout or "") + "\n" + (p.stderr or "")
    ok = p.returncode == 0 and not detect_problems(log)
    return ok, log
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_build.py -q`
Expected: PASS (5 passed)

- [ ] **Step 5: Integration — real build is clean**

Run: `uv run python -c "from scripts.fidelity.build import run_build; ok,log=run_build(); print('OK' if ok else 'FAIL'); print(log[-800:])"`
Expected: prints `OK`. If `FAIL`, the tail shows the problem lines — this is a genuine build issue to fix now (extend Task 2's `exclude:` or fix the offending template/post) since P0's gate requires a clean build. Re-run until `OK`.

- [ ] **Step 6: Mark the integration boundary**

Confirm `tests/fidelity/test_build.py` contains only pure `detect_problems` tests (no subprocess) so `uv run pytest -m "not integration"` stays fast and hermetic.

- [ ] **Step 7: Commit**

```bash
git add scripts/fidelity/build.py tests/fidelity/test_build.py
git commit -m "P0: Jekyll build gate with problem detector"
```

---

## Task 9: `wayback.py` — snapshot resolver (TDD, mocked)

Use @superpowers:test-driven-development.

**Files:**
- Create: `scripts/fidelity/wayback.py`
- Test: `tests/fidelity/test_wayback.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_wayback.py
import io, json
from scripts.fidelity.wayback import parse_availability, snapshot_url

def test_parse_returns_url_when_available():
    payload = {"archived_snapshots": {"closest": {
        "available": True, "url": "http://web.archive.org/web/2016/https://blog.mithis.net/"}}}
    assert parse_availability(payload).startswith("http://web.archive.org/web/")

def test_parse_returns_none_when_empty():
    assert parse_availability({"archived_snapshots": {}}) is None
    assert parse_availability({}) is None

def test_snapshot_url_uses_injected_opener():
    body = json.dumps({"archived_snapshots": {"closest": {
        "available": True, "url": "http://web.archive.org/web/x"}}}).encode()
    class Resp(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): return False
    captured = {}
    def fake_opener(url, timeout=0):
        captured["url"] = url
        return Resp(body)
    out = snapshot_url("https://blog.mithis.net/archives/tp/15-tp-protocol-overview",
                       "20120101", opener=fake_opener)
    assert out == "http://web.archive.org/web/x"
    assert "blog.mithis.net" in captured["url"] and "timestamp=20120101" in captured["url"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_wayback.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/wayback.py
"""Resolve the best Wayback Machine snapshot for an original URL via the
Availability API. Network is injected for testability."""
from __future__ import annotations
import json
import urllib.parse
import urllib.request

_AVAIL = "http://archive.org/wayback/available"

def parse_availability(payload: dict | None) -> str | None:
    snap = ((payload or {}).get("archived_snapshots") or {}).get("closest") or {}
    if snap.get("available") and snap.get("url"):
        return snap["url"]
    return None

def snapshot_url(original_url: str, timestamp: str = "", *,
                 opener=urllib.request.urlopen) -> str | None:
    q = {"url": original_url}
    if timestamp:
        q["timestamp"] = timestamp
    url = f"{_AVAIL}?{urllib.parse.urlencode(q)}"
    with opener(url, timeout=30) as r:
        return parse_availability(json.loads(r.read().decode("utf-8")))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_wayback.py -q`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/fidelity/wayback.py tests/fidelity/test_wayback.py
git commit -m "P0: Wayback snapshot resolver"
```

---

## Task 10: `report.py` — fidelity report assembler (TDD)

Use @superpowers:test-driven-development.

**Files:**
- Create: `scripts/fidelity/report.py`
- Test: `tests/fidelity/test_report.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/fidelity/test_report.py
from scripts.fidelity.report import render_report
from scripts.fidelity.compare import StructuralResult
from scripts.fidelity.barthelme import Anchor
from scripts.fidelity.lint_content import Finding

def test_all_green_report():
    md = render_report(build_ok=True, build_log_tail="",
                       structural=[StructuralResult("home", ())], lint=[])
    assert "Build: PASS" in md
    assert "Structural diff: PASS (1/1" in md
    assert "Content linter: PASS (0 finding" in md

def test_failures_are_itemised():
    md = render_report(
        build_ok=False, build_log_tail="Liquid Exception: boom",
        structural=[StructuralResult("home", (Anchor("div", "#sidebar"),))],
        lint=[Finding("_posts/x.md", 12, "BLOCK_HTML", "no <div>")],
    )
    assert "Build: FAIL" in md
    assert "MISSING `div#sidebar`" in md
    assert "_posts/x.md:12 [BLOCK_HTML]" in md
    assert "Liquid Exception: boom" in md
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/fidelity/test_report.py -q`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fidelity/report.py
"""Assemble tmp/fidelity/fidelity-report.md from component results."""
from __future__ import annotations
from .compare import StructuralResult
from .lint_content import Finding

def render_report(*, build_ok: bool, build_log_tail: str,
                  structural: list[StructuralResult],
                  lint: list[Finding]) -> str:
    s_ok = bool(structural) and all(r.passed for r in structural)
    n_ok = sum(1 for r in structural if r.passed)
    L: list[str] = ["# Fidelity Report", ""]
    L.append(f"- Build: {'PASS' if build_ok else 'FAIL'}")
    L.append(f"- Structural diff: {'PASS' if s_ok else 'FAIL'} "
             f"({n_ok}/{len(structural)} archetypes)")
    L.append(f"- Content linter: {'PASS' if not lint else 'FAIL'} "
             f"({len(lint)} finding(s))")
    L += ["", "## Structural", ""]
    for r in structural:
        L.append(f"### {r.archetype}: {'PASS' if r.passed else 'FAIL'}")
        for a in r.missing:
            L.append(f"- MISSING `{a.tag}{a.ident}`")
    L += ["", "## Content findings", ""]
    for f in lint:
        L.append(f"- {f.path}:{f.line} [{f.code}] {f.message}")
    if not build_ok and build_log_tail:
        L += ["", "## Build log (tail)", "", "```", build_log_tail, "```"]
    return "\n".join(L) + "\n"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/fidelity/test_report.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/fidelity/report.py tests/fidelity/test_report.py
git commit -m "P0: fidelity report assembler"
```

---

## Task 11: `render.py` — Playwright archetype renderer (integration, local visual layer)

Per spec §6.2 this is the local/manual visual layer, NOT a CI gate. No unit test; one integration verification.

**Files:**
- Create: `scripts/fidelity/render.py`

- [ ] **Step 1: Implement the renderer**

```python
# scripts/fidelity/render.py
"""Local visual layer: screenshot + DOM snapshot per archetype against a served
Jekyll site. Uses the Playwright Python library (the Playwright MCP is the
separate interactive tool). Not a CI gate (spec §6.2)."""
from __future__ import annotations
from pathlib import Path
from .archetypes import ARCHETYPES

def capture_all(base_url: str, out_dir: str | Path,
                viewport=(1280, 1024)) -> dict[str, dict]:
    from playwright.sync_api import sync_playwright  # lazy: optional dep
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport[0],
                                           "height": viewport[1]})
        for a in ARCHETYPES:
            url = base_url.rstrip("/") + a.path
            png = out / f"{a.name}.png"
            html = out / f"{a.name}.html"
            try:
                # NOT 'networkidle': the original Picasa header hotlinks dead
                # Google CDN images, so the network never goes idle and every
                # capture would burn the full timeout. 'domcontentloaded' + a
                # short settle captures local CSS/layout without the stall.
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(1500)
                page.screenshot(path=str(png), full_page=True)
                html.write_text(page.content(), encoding="utf-8")
                results[a.name] = {"url": url, "png": str(png),
                                   "html": str(html), "ok": True}
            except Exception as e:  # record, never abort the sweep
                results[a.name] = {"url": url, "ok": False, "error": repr(e)}
        browser.close()
    return results
```

- [ ] **Step 2: Install the browser**

Run: `uv run playwright install chromium`
Expected: downloads Chromium; ends success.

- [ ] **Step 3: Integration verify (served site)**

In one shell: `bundle exec jekyll serve --port 4000 --detach`
Then: `uv run python -c "from scripts.fidelity.render import capture_all; r=capture_all('http://localhost:4000','tmp/fidelity/jekyll'); print({k:v['ok'] for k,v in r.items()})"`
Expected: dict with `home`, `post`, `category`, `page`, `notfound`, `search`, `feed` → mostly `True`; `tmp/fidelity/jekyll/home.png` exists.
Then stop the server: `pkill -f "jekyll serve"` (or kill the detached pid).

- [ ] **Step 4: Commit**

```bash
git add scripts/fidelity/render.py
git commit -m "P0: Playwright archetype renderer (local visual layer)"
```

---

## Task 12: `run.py` — orchestrator + first fidelity report (P0 EXIT GATE)

Ties the harness together and produces `tmp/fidelity/fidelity-report.md`. Use @superpowers:verification-before-completion before declaring P0 complete.

**Files:**
- Create: `scripts/fidelity/run.py`
- Test: `tests/fidelity/test_run_smoke.py`

- [ ] **Step 1: Write the orchestrator**

```python
# scripts/fidelity/run.py
"""P0 exit-gate runner: build -> serve -> render -> structural diff vs Barthelme
-> lint posts -> write tmp/fidelity/fidelity-report.md.

Exit policy (spec P0 gate): exit 1 if the build is NOT clean OR the content
linter has findings. Structural results are REPORTED (P1 input) and do not, by
themselves, fail P0 — P0's job is to measure, not to be all-green."""
from __future__ import annotations
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

from .archetypes import structural_archetypes
from .build import bundler, run_build
from .compare import structural_diff
from .lint_content import lint_paths
from .report import render_report

OUT = Path("tmp/fidelity")
BARTHELME = Path("theme_analysis/barthelme")

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    build_ok, log = run_build()

    structural = []
    render_error = ""
    proc = None
    serve_log = open(OUT / "jekyll-serve.log", "w", encoding="utf-8")
    try:
        # No --detach: keep serve as a child so proc.terminate() reaps it.
        # --skip-initial-build serves the _site produced by run_build() above.
        # serve output goes to a log file (NOT DEVNULL) so a flaky local
        # serve is debuggable and stderr stays visible.
        proc = subprocess.Popen(
            [bundler(), "exec", "jekyll", "serve", "--port", "4000",
             "--skip-initial-build", "--no-watch"],
            stdout=serve_log, stderr=subprocess.STDOUT)
        time.sleep(6)
        # spec §6.2: the Playwright visual layer is the LOCAL, non-gating step.
        # It must never break the CI-able P0 gate (build+lint+structural). Two
        # guards: (1) FIDELITY_SKIP_RENDER skips the browser entirely (it is
        # heavyweight and not meaningful until P4 sets baseurl="" so served
        # URLs resolve); (2) any capture exception degrades to no rendered HTML.
        if os.environ.get("FIDELITY_SKIP_RENDER"):
            rendered = {}
            render_error = "skipped via FIDELITY_SKIP_RENDER (spec §6.2 local layer)"
        else:
            try:
                from .render import capture_all
                rendered = capture_all("http://localhost:4000", OUT / "jekyll")
            except Exception as e:
                rendered = {}
                render_error = repr(e)
        for a in structural_archetypes():
            r = rendered.get(a.name, {})
            html = (Path(r["html"]).read_text(encoding="utf-8")
                    if r.get("ok") else "")
            php = (BARTHELME / a.barthelme_template).read_text(
                encoding="utf-8", errors="replace")
            structural.append(structural_diff(a.name, php, html))
    finally:
        if proc:
            proc.terminate()
        serve_log.close()

    findings = lint_paths(sorted(glob.glob("_posts/*.md")), asset_root=".")

    report = render_report(build_ok=build_ok, build_log_tail=log[-1500:],
                           structural=structural, lint=findings)
    if render_error:
        report += ("\n## Renderer\n\nPlaywright visual layer NOT RUN "
                   "(spec §6.2: local, non-gating). Structural results above "
                   "reflect NO rendered HTML (every Barthelme anchor shows as "
                   "missing) — re-run locally with a browser (after P4 sets "
                   "baseurl=\"\" so served URLs resolve) for the real "
                   f"structural diff.\nReason: {render_error}\n")
    (OUT / "fidelity-report.md").write_text(report, encoding="utf-8")
    print(report)

    return 0 if (build_ok and not findings) else 1

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke test the orchestrator is importable/wired**

```python
# tests/fidelity/test_run_smoke.py
import importlib
def test_run_module_imports():
    m = importlib.import_module("scripts.fidelity.run")
    assert hasattr(m, "main")
```

Run: `uv run pytest tests/fidelity/test_run_smoke.py -q`
Expected: PASS (1 passed)

- [ ] **Step 3: Full unit suite green**

Run: `uv run pytest -m "not integration" -q`
Expected: PASS — all unit tests across tasks 4–10 + smoke (no network/browser needed).

- [ ] **Step 4: Run the harness end-to-end (the P0 exit gate)**

Run: `FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run`
(Per spec §6.2 the P0 exit gate is the CI-able build+linter+structural-comparator — NOT the browser. The Playwright visual layer is a local step that is not meaningful until P4 sets `baseurl=""` so served URLs resolve, and it is heavyweight; `FIDELITY_SKIP_RENDER=1` is the correct way to run the P0 gate. The full browser render is a documented post-P4 local step, not a P0 deliverable.)
Expected: writes `tmp/fidelity/fidelity-report.md` and prints it. The report MUST show `Build: PASS`, a `## Renderer ... NOT RUN` note, and `Structural diff`/`Content linter` sections showing FAIL/findings — that is correct and expected: it is the measured P1/P2 worklist.

- [ ] **Step 5: Verify the exit gate semantics**

Run: `FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run; echo "exit=$?"`
Expected: `exit=1` *iff* build failed or linter has findings (normal at P0 since posts are unaudited — exit=1 here is SUCCESS for P0, driven by the expected lint worklist). Confirm `Build: PASS` in the report regardless. If `Build: FAIL`, STOP and surface the build-log tail (do not mask it) — a clean build is mandatory and was verified in Task 8/2A.

- [ ] **Step 6: @superpowers:verification-before-completion**

Confirm with evidence, pasted into the completion note: (a) `uv run pytest -m "not integration" -q` output showing all unit tests pass; (b) the `tmp/fidelity/fidelity-report.md` header showing `Build: PASS`; (c) `ls _site` showing no leaked non-site dirs. Do not claim P0 complete without all three.

- [ ] **Step 7: Commit**

```bash
git add scripts/fidelity/run.py tests/fidelity/test_run_smoke.py
git commit -m "P0: fidelity orchestrator + first measured fidelity report"
```

---

## Task 13: Record P0 outputs and hand off to P1

**Files:**
- Create: `docs/superpowers/plans/P0-RESULTS.md`

- [ ] **Step 1: Capture the measured worklist**

Write `docs/superpowers/plans/P0-RESULTS.md` containing: the `Build:` status; the per-archetype structural PASS/FAIL with the list of MISSING anchors (the P1 theme worklist); the content-linter finding counts grouped by `code` and by post (the P2 content worklist); and the live-site poll status for P3. This is the factual input for authoring the P1 and P2 plans.

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/plans/P0-RESULTS.md
git commit -m "P0: record measured fidelity worklist for P1/P2"
```

- [ ] **Step 3: Stop and re-plan**

Do NOT start fixing theme/content ad hoc. Return to @superpowers:writing-plans to author **`2026-…-blog-fidelity-p1-theme.md`** (theme gap closure, driven by the recorded MISSING anchors + Playwright/Wayback visual comparison) and subsequently the P2/P3/P4/P5/P6 plans. Each subsequent plan is data-driven by P0's report and follows the same TDD/commit discipline.

---

## Subsequent plans (scope note — NOT implemented by this plan)

These are deliberately separate, data-driven plans (spec §5), authored after P0 produces measurements:

- **P1 Theme fidelity** — close every MISSING structural anchor + Playwright/Wayback visual deltas per archetype; verify Picasa header markup byte-identical to the original. Gate: structural diff PASS for all structural archetypes.
- **P2 Content fidelity** — drive the linter to zero findings across all posts (Liquid leaks, block HTML→Markdown, missing images). Gate: linter clean.
- **P3 Missing posts** — gated on `blog.mithis.net` reachable (poll; Wayback fallback per post): recover IDs 15/35/84/92, convert to the exact existing post format incl. dual comment representation. Gate: 76/76 + linter clean.
- **P4 Domain/deploy** — `CNAME`, `_config.yml` `url`/`baseurl`, remove the workflow `--baseurl` override, absolute feed/sitemap URLs, DNS records for the user. Gate: correct custom-domain build.
- **P5 New-post workflow** — authoring doc + scaffold script + sample post proving identical render; wire `lint_content` as a build-time guard. Gate: guard active, sample identical.
- **P6 Final acceptance** — Wayback pixel sweep + report + user signoff. Gate: all three acceptance methods pass.

**Live-site polling (cross-cutting):** from P0 onward, before any session that could start P3, run `curl -sS -o /dev/null -w '%{http_code}' -m 20 https://blog.mithis.net/` — `200` means start P3; connection failure means continue non-live work.
