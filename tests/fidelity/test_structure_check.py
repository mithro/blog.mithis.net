# tests/fidelity/test_structure_check.py
from pathlib import Path
from scripts.fidelity.structure_check import (
    ARCHETYPE_SITE_PATHS, PHANTOM_ANCHORS, check_html, all_pass,
)
from scripts.fidelity.compare import StructuralResult
from scripts.fidelity.barthelme import Anchor

def test_every_structural_archetype_has_a_site_path():
    from scripts.fidelity.archetypes import structural_archetypes
    for a in structural_archetypes():
        assert a.name in ARCHETYPE_SITE_PATHS
        assert ARCHETYPE_SITE_PATHS[a.name].endswith(".html")

def test_phantom_anchors_are_barthelme_dynamic_id_artifacts():
    # #post- is a genuine PHP artifact (id="post-<?php the_ID()?>") — keep ignored
    assert Anchor("div", "#post-") in PHANTOM_ANCHORS
    # #post-0 is a static literal in 404.php/search.php — a real structural
    # element, must NOT be silently ignored (it must appear in the built HTML)
    assert Anchor("div", "#post-0") not in PHANTOM_ANCHORS

def test_check_html_passes_when_anchors_present():
    php = '<div id="container"><div class="entry-content">x</div></div>'
    html = '<html><div id="container"><div class="entry-content"><p>hi</p></div></div></html>'
    r = check_html("page", php, html)
    assert isinstance(r, StructuralResult) and r.passed

def test_check_html_reports_missing_and_ignores_phantoms():
    php = ('<div id="container"><div id="post-">p</div>'
           '<div id="sidebar">s</div></div>')
    html = '<div id="container"></div>'
    r = check_html("home", php, html)
    assert not r.passed
    assert Anchor("div", "#sidebar") in r.missing
    assert Anchor("div", "#post-") not in r.missing

def test_all_pass_true_only_when_every_result_passes():
    assert all_pass([StructuralResult("a", ()), StructuralResult("b", ())])
    assert not all_pass([StructuralResult("a", ()),
                         StructuralResult("b", (Anchor("div", "#x"),))])
    assert not all_pass([])
