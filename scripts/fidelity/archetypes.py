# scripts/fidelity/archetypes.py
"""Single source of truth for the page archetypes the harness verifies."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Archetype:
    name: str
    path: str                # URL path on the served Jekyll site
    barthelme_template: str  # reference .php in theme_analysis/barthelme/ ("" = none)
    structural: bool         # participates in the structural diff gate

# Stable representative pages. The post is the 2020 nMigen post (exists, fixed slug).
ARCHETYPES: tuple[Archetype, ...] = (
    Archetype("home",     "/",                                                        "index.php",   True),
    Archetype("post",     "/archives/hardware/2186-nmigen-new-improved-by-whitequark", "single.php",  True),
    Archetype("category", "/category/hardware/",                                       "archive.php", True),
    Archetype("page",     "/about/",                                                   "page.php",    True),
    Archetype("notfound", "/404.html",                                                 "404.php",     True),
    Archetype("search",   "/search.html",                                              "search.php",  True),
    Archetype("feed",     "/feed.xml",                                                 "",            False),
)

# Barthelme templates deliberately OUT of scope for the structural diff (spec §6.2):
# no equivalent live surface in this blog.
EXCLUDED_BARTHELME_TEMPLATES = frozenset(
    {"archives.php", "attachment.php", "image.php", "links.php", "sitemap.php"}
)

def structural_archetypes() -> tuple[Archetype, ...]:
    return tuple(a for a in ARCHETYPES if a.structural)
