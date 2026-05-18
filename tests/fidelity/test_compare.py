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
