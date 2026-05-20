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


# --- Task L: fidelity-allow sentinel tests ---

_EMBED_LINE = '<object data="foo.swf"><embed src="foo.swf"></embed></object>'
_SENTINEL = '<!-- fidelity-allow: BLOCK_HTML necessary-embed — Flash video required for original content fidelity -->'

def test_fidelity_allow_sentinel_suppresses_block_html():
    """(a) BLOCK_HTML with fidelity-allow sentinel on the same line → zero BLOCK_HTML findings."""
    line = _EMBED_LINE + " " + _SENTINEL
    f = lint_text("p.md", FM + line + "\n")
    block_findings = [x for x in f if x.code == "BLOCK_HTML"]
    assert block_findings == [], (
        f"Expected no BLOCK_HTML findings when sentinel is present, got: {block_findings}"
    )


def test_fidelity_allow_sentinel_on_preceding_line_suppresses_block_html():
    """(a) BLOCK_HTML with fidelity-allow sentinel on the immediately preceding line → zero BLOCK_HTML findings."""
    body = _SENTINEL + "\n" + _EMBED_LINE + "\n"
    f = lint_text("p.md", FM + body)
    block_findings = [x for x in f if x.code == "BLOCK_HTML"]
    assert block_findings == [], (
        f"Expected no BLOCK_HTML findings when sentinel is on preceding line, got: {block_findings}"
    )


def test_block_html_without_sentinel_is_still_flagged():
    """(b) The same BLOCK_HTML occurrence WITHOUT the sentinel → the finding IS emitted."""
    f = lint_text("p.md", FM + _EMBED_LINE + "\n")
    block_findings = [x for x in f if x.code == "BLOCK_HTML"]
    assert len(block_findings) >= 1, (
        "Expected at least one BLOCK_HTML finding when no sentinel is present"
    )


def test_sentinel_is_per_occurrence_not_file_wide():
    """(c) A second un-annotated BLOCK_HTML occurrence in the same text → still flagged."""
    # First occurrence has sentinel (suppressed), second does not (flagged)
    body = (
        _SENTINEL + "\n"
        + _EMBED_LINE + "\n"
        + "<div>this div has no sentinel</div>\n"
    )
    f = lint_text("p.md", FM + body)
    block_findings = [x for x in f if x.code == "BLOCK_HTML"]
    assert len(block_findings) == 1, (
        f"Expected exactly 1 BLOCK_HTML finding (the un-annotated div), got: {block_findings}"
    )


def test_sentinel_does_not_affect_liquid_leak_or_missing_image(tmp_path):
    """(d) F-lint/F-norm unaffected: LIQUID_LEAK and MISSING_IMAGE paths unchanged."""
    (tmp_path / "assets").mkdir()
    body = (
        _SENTINEL + "\n"
        + _EMBED_LINE + "\n"
        + "{{ page.title }}\n"
        + "![img](/assets/missing.png)\n"
    )
    f = lint_text("p.md", FM + body, asset_root=tmp_path)
    codes_found = codes(f)
    # The sentinel-annotated BLOCK_HTML is suppressed
    assert "BLOCK_HTML" not in codes_found, (
        "Sentinel should suppress BLOCK_HTML on the annotated embed"
    )
    # But LIQUID_LEAK and MISSING_IMAGE are still emitted
    assert "LIQUID_LEAK" in codes_found, "LIQUID_LEAK should still be flagged"
    assert "MISSING_IMAGE" in codes_found, "MISSING_IMAGE should still be flagged"


# --- P5-A: new tests for i==0 guard and UNCLOSED_FENCE ---

def test_block_html_on_first_body_line_is_not_suppressed_by_last_line_sentinel():
    """i==0 guard: sentinel on the prev line (none) must not shadow from lines[-1]."""
    # Put a sentinel at the END of the body (which is lines[-1])
    # The BLOCK_HTML is on the FIRST body line (i=0). Must NOT be suppressed.
    body = (
        FM
        + "<div>this is first body line — no preceding sentinel</div>\n"
        + "some prose\n"
        + _SENTINEL + "\n"  # sentinel at end, NOT adjacent to the div
    )
    f = lint_text("p.md", body)
    block_findings = [x for x in f if x.code == "BLOCK_HTML"]
    assert len(block_findings) >= 1, (
        "BLOCK_HTML on first body line must not be suppressed by a sentinel "
        "elsewhere in the body (negative-index guard must hold)"
    )


def test_unclosed_fence_is_flagged():
    """UNCLOSED_FENCE: a fenced block never closed produces a finding at EOF."""
    body = FM + "```python\ndef foo():\n    pass\n# no closing fence\n"
    f = lint_text("p.md", body)
    codes_found = [x.code for x in f]
    assert "UNCLOSED_FENCE" in codes_found, (
        "An unclosed fenced code block must produce an UNCLOSED_FENCE finding"
    )


# --- P5-H: CLI smoke tests ---

import subprocess
import sys


def test_cli_clean_corpus_exits_zero():
    """CLI smoke: linting the real _posts corpus exits 0 (no findings)."""
    result = subprocess.run(
        [sys.executable, "-m", "scripts.fidelity.lint_content",
         "_posts", "--asset-root", "."],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Expected exit 0 for clean corpus; got {result.returncode}.\n"
        f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
    )
    assert result.stdout == "", (
        f"Expected no output for clean corpus; got: {result.stdout!r}"
    )


def test_cli_file_with_violation_exits_one(tmp_path):
    """CLI smoke: linting a file with a raw <div> exits 1 + finding in stdout."""
    bad = tmp_path / "badpost.md"
    bad.write_text(
        "---\ntitle: x\nlayout: post\n---\n"
        "<div>block HTML violation</div>\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "scripts.fidelity.lint_content",
         str(bad), "--asset-root", "."],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        f"Expected exit 1 for file with BLOCK_HTML; got {result.returncode}.\n"
        f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
    )
    assert "BLOCK_HTML" in result.stdout, (
        f"Expected BLOCK_HTML finding in stdout; got: {result.stdout!r}"
    )


def test_detects_hr_block_html():
    """<hr> and <hr/> must be detected as BLOCK_HTML (A-2c coverage extension)."""
    f_bare = lint_text("p.md", FM + "<hr>\n")
    assert "BLOCK_HTML" in codes(f_bare), "<hr> must be flagged as BLOCK_HTML"
    f_self = lint_text("p.md", FM + "<hr/>\n")
    assert "BLOCK_HTML" in codes(f_self), "<hr/> must be flagged as BLOCK_HTML"
    f_spaced = lint_text("p.md", FM + "<hr />\n")
    assert "BLOCK_HTML" in codes(f_spaced), "<hr /> must be flagged as BLOCK_HTML"
    # In a blockquote prefix context (as in timvideos-2016)
    f_bq = lint_text("p.md", FM + "> <hr/>\n")
    assert "BLOCK_HTML" in codes(f_bq), "> <hr/> inside blockquote must be flagged as BLOCK_HTML"
