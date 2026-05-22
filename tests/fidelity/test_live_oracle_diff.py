"""Unit tests for the live-oracle diff helpers (the subtle normalization logic).

The diff tool itself needs the live site + a build (manual diligence), but its
pure helpers — entry-content slicing, URL normalization, text folding — are
the regression-prone parts and are tested here without network.
"""
from scripts.fidelity.live_oracle_diff import (
    entry_content,
    _norm_url,
    _fold_text,
    _extract,
)


def test_entry_content_slices_to_first_footer_marker():
    html = (
        '<div class="post"><div class="entry-content"><p>body</p>'
        '<ul><li>x</li></ul></div>'
        '<div class="entry-meta">FOOTER NOT COUNTED</div>'
        '<div id="comments"><h2>Comments</h2></div></div>'
    )
    seg = entry_content(html)
    assert "body" in seg
    assert "FOOTER NOT COUNTED" not in seg  # stops at entry-meta
    assert "Comments" not in seg


def test_norm_url_folds_domain_scheme_and_local_image_hosting():
    # built local-hosting path == live wp-content path
    assert (_norm_url("/assets/images/wp-content/uploads/2009/01/x.pdf")
            == _norm_url("https://blog.mithis.net/wp-content/uploads/2009/01/x.pdf"))
    # http vs https on external hosts folds
    assert _norm_url("http://example.com/a") == _norm_url("https://example.com/a/")
    # nested wayback prefix is unwrapped down to the mithis.net path
    wb = "https://web.archive.org/web/20110311im_/https://blog.mithis.net/wp-content/x.png"
    assert _norm_url(wb) == "/wp-content/x.png"


def test_fold_text_normalizes_typography_and_entities():
    assert _fold_text("don’t “quote” end") == 'don\'t "quote" end'
    assert _fold_text("a &amp; b") == "a & b"


def test_extract_counts_structure_and_targets_in_entry_content_only():
    html = (
        '<div class="entry-content">'
        '<p>hi</p>'
        '<a href="https://blog.mithis.net/wp-content/uploads/p.pdf">paper</a>'
        '<img src="/assets/images/wp-content/uploads/x.png" alt="A Pic">'
        '</div>'
        '<div class="entry-meta"><a href="/ignored">meta</a></div>'
    )
    e = _extract(html)
    assert e.tags["p"] == 1 and e.tags["img"] == 1
    assert _norm_url("/wp-content/uploads/p.pdf") in e.hrefs
    assert "/ignored" not in e.hrefs  # footer link excluded
    assert e.alts == ["A Pic"]
    assert e.words()["paper"] == 1
