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
