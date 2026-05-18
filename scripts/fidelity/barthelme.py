# scripts/fidelity/barthelme.py
"""Extract structural anchors (tag#id, tag.class) from the static portions of a
Barthelme PHP template. PHP blocks are stripped; attribute values containing PHP
are treated as dynamic and produce no static anchor."""
from __future__ import annotations
import re
from dataclasses import dataclass
from html.parser import HTMLParser

_PHP = re.compile(r"<\?php.*?\?>", re.DOTALL)
_PHP_ECHO = re.compile(r"<\?=.*?\?>", re.DOTALL)

@dataclass(frozen=True, order=True)
class Anchor:
    tag: str
    ident: str  # "#id" or ".class"

class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[Anchor] = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cid = d.get("id")
        if cid and "<?" not in cid:
            self.anchors.add(Anchor(tag, f"#{cid.strip()}"))
        cls = d.get("class")
        if cls and "<?" not in cls:
            for c in cls.split():
                if c:
                    self.anchors.add(Anchor(tag, f".{c}"))

def strip_php(php_text: str) -> str:
    return _PHP_ECHO.sub("", _PHP.sub("", php_text))

def extract_anchors(php_text: str) -> set[Anchor]:
    c = _Collector()
    c.feed(strip_php(php_text))
    return c.anchors

def anchors_in_html(html: str) -> set[Anchor]:
    c = _Collector()
    c.feed(html)
    return c.anchors
