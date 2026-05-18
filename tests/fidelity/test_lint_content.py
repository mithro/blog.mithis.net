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
