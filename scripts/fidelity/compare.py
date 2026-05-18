# scripts/fidelity/compare.py
"""Structural containment diff: Jekyll output must contain every structural
anchor present in the corresponding Barthelme template. Extra Jekyll anchors are
allowed. See plan 'Containment model'."""
from __future__ import annotations
from dataclasses import dataclass
from .barthelme import Anchor, extract_anchors, anchors_in_html

@dataclass(frozen=True)
class StructuralResult:
    archetype: str
    missing: tuple[Anchor, ...]
    @property
    def passed(self) -> bool:
        return not self.missing

def structural_diff(archetype: str, barthelme_php: str, jekyll_html: str,
                    *, ignore: frozenset[Anchor] | set[Anchor] = frozenset()
                    ) -> StructuralResult:
    expected = extract_anchors(barthelme_php) - set(ignore)
    actual = anchors_in_html(jekyll_html)
    missing = tuple(sorted(expected - actual))
    return StructuralResult(archetype, missing)
