"""
Spot-check that entry-interact text agrees with comments-section presence.
Posts with comment data -> 'post a comment'; posts without -> 'closed'.
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).parent.parent.parent / "_site"

CHECKS = [
    # (path_relative_to_site, expect_comments, label)
    ("archives/ideas/51-nm-autovpn.html", True, "nm-autovpn (HAS comments)"),
    ("archives/sci-fi/102-starhunter-fireflys-little-known-older-cousin.html", True,
     "starhunter (HAS comments)"),
    ("archives/ideas/20-graphical-programming.html", False,
     "graphical-programming (NO comments)"),
]

ok = True
for rel, expect_comments, label in CHECKS:
    path = SITE / rel
    if not path.exists():
        print(f"SKIP {label}: file not found at {path}")
        continue
    content = path.read_text()
    interact_m = re.search(r'<span class="entry-interact">(.*?)</span>', content, re.DOTALL)
    has_comments_section = bool(re.search(r'<div class="comments-section">', content))

    interact_text = interact_m.group(1).strip() if interact_m else "(not found)"
    interact_open = "post a comment" in interact_text
    interact_closed = "closed" in interact_text

    agree = (expect_comments == has_comments_section) and (expect_comments == interact_open) and (not expect_comments == interact_closed)
    status = "OK" if agree else "FAIL"
    print(f"{status}  {label}")
    print(f"      entry-interact: {interact_text!r}")
    print(f"      comments-section present: {has_comments_section} (expected: {expect_comments})")
    print(f"      entry-interact says open={interact_open}, closed={interact_closed}")
    if not agree:
        ok = False

sys.exit(0 if ok else 1)
