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
