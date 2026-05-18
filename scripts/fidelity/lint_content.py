# scripts/fidelity/lint_content.py
"""Lint committed post content: no Liquid leakage, no hardcoded block HTML,
no missing local images. Encodes the spec's 'no hardcoded structural HTML' rule.
Inline HTML (a, abbr, code, em, strong, sup, sub, br, img, span, kbd, q, cite,
del, ins, mark, time) is allowed where Markdown can't express the original."""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

_BLOCK_HTML = re.compile(
    r"</?(?:div|section|article|header|footer|nav|aside|main|table|thead|tbody|"
    r"tfoot|tr|td|th|ul|ol|li|dl|dt|dd|h[1-6]|p|figure|figcaption|blockquote|"
    r"pre|form|fieldset|iframe|script|style|center|font|object|embed)\b",
    re.IGNORECASE,
)
_LIQUID = re.compile(r"\{\{|\{%")
_MD_IMG = re.compile(r"!\[[^\]]*\]\(\s*([^)\s]+)")
_HTML_IMG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.IGNORECASE)

def _split_front_matter(text: str) -> tuple[int, str]:
    """Return (1-based line where body starts, body text)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            if nl != -1:
                prefix = text[: nl + 1]
                return prefix.count("\n") + 1, text[nl + 1 :]
    return 1, text

def _check_image(path, lineno, src, asset_root, out):
    if src.startswith(("http://", "https://", "//", "data:", "mailto:")):
        return
    if asset_root is None:
        return
    rel = src.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    if rel and not (Path(asset_root) / rel).exists():
        out.append(Finding(path, lineno, "MISSING_IMAGE",
                            f"Local image not found: {src}"))

def lint_text(path: str, text: str, *, asset_root: Path | None = None) -> list[Finding]:
    out: list[Finding] = []
    body_start, body = _split_front_matter(text)
    in_fence = False
    for i, raw in enumerate(body.splitlines()):
        lineno = body_start + i
        s = raw.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _LIQUID.search(raw):
            out.append(Finding(path, lineno, "LIQUID_LEAK",
                               "Unrendered Liquid ({{ or {%) in committed content"))
        if _BLOCK_HTML.search(raw):
            out.append(Finding(path, lineno, "BLOCK_HTML",
                               "Hardcoded block-level HTML; express this in Markdown"))
        for m in _MD_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
        for m in _HTML_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
    return out

def lint_paths(paths, *, asset_root: Path | None = None) -> list[Finding]:
    out: list[Finding] = []
    for p in paths:
        p = Path(p)
        out.extend(lint_text(str(p), p.read_text(encoding="utf-8"),
                             asset_root=asset_root))
    return out
