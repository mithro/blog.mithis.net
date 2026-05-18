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
