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
