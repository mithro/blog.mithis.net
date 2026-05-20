# scripts/fidelity/lint_content.py
"""Lint committed post content: no Liquid leakage, no hardcoded block HTML,
no missing local images. Encodes the spec's 'no hardcoded structural HTML' rule.
Inline HTML (a, abbr, code, em, strong, sup, sub, br, img, span, kbd, q, cite,
del, ins, mark, time) is allowed where Markdown can't express the original.

Sentinel: a line containing
  <!-- fidelity-allow: BLOCK_HTML necessary-embed — <reason> -->
immediately before a BLOCK_HTML line (or on the same line) suppresses that
one finding. It is per-occurrence, not file-wide. Used for genuine necessary-
embed HTML (e.g. Flash `<object>` in techtalk-gamingforfreedom). All other
findings (LIQUID_LEAK, MISSING_IMAGE) are unaffected by the sentinel.

UNCLOSED_FENCE: a fenced code block (``` or ~~~) that is never closed causes
in_fence=True to remain at EOF, silently suppressing all findings below the
opening fence. When this condition is detected, an UNCLOSED_FENCE finding is
emitted at the line of the opening fence marker (or the last line of the body
as a proxy). Authors must close all fenced blocks.
"""
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
_FIDELITY_ALLOW_BLOCK_HTML = re.compile(
    r"<!--\s*fidelity-allow:\s*BLOCK_HTML", re.IGNORECASE  # \b was redundant — prefix already prevents partial matches
)

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
    lines = body.splitlines()
    in_fence = False
    fence_open_lineno: int | None = None  # track where the unclosed fence started
    for i, raw in enumerate(lines):
        lineno = body_start + i
        s = raw.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            if in_fence:
                fence_open_lineno = lineno  # record opening line for UNCLOSED_FENCE reporting
            else:
                fence_open_lineno = None   # fence properly closed
            continue
        if in_fence:
            continue
        if _LIQUID.search(raw):
            out.append(Finding(path, lineno, "LIQUID_LEAK",
                               "Unrendered Liquid ({{ or {%) in committed content"))
        if _BLOCK_HTML.search(raw):
            prev_line = lines[i - 1] if i > 0 else ""  # fence predecessors are harmless (closing ``` is not BLOCK_HTML)
            allowed = (
                _FIDELITY_ALLOW_BLOCK_HTML.search(raw)
                or _FIDELITY_ALLOW_BLOCK_HTML.search(prev_line)
            )
            if not allowed:
                out.append(Finding(path, lineno, "BLOCK_HTML",
                                   "Hardcoded block-level HTML; express this in Markdown"))
        for m in _MD_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
        for m in _HTML_IMG.finditer(raw):
            _check_image(path, lineno, m.group(1), asset_root, out)
    # UNCLOSED_FENCE: if in_fence is still True at EOF, the opening fence was never closed
    if in_fence and fence_open_lineno is not None:
        out.append(Finding(path, fence_open_lineno, "UNCLOSED_FENCE",
                           "Fenced code block was never closed"))
    return out

def lint_paths(paths, *, asset_root: Path | None = None) -> list[Finding]:
    out: list[Finding] = []
    for p in paths:
        p = Path(p)
        out.extend(lint_text(str(p), p.read_text(encoding="utf-8"),
                             asset_root=asset_root))
    return out


def _cli_main(argv=None) -> int:
    import argparse
    import glob
    import sys as _sys

    parser = argparse.ArgumentParser(
        description="Lint post Markdown files for LIQUID_LEAK, BLOCK_HTML, "
                    "MISSING_IMAGE, and UNCLOSED_FENCE.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["_posts"],
        help="Files or directories to lint (default: _posts). "
             "Directories are expanded to *.md (sorted).",
    )
    parser.add_argument(
        "--asset-root",
        default=".",
        metavar="DIR",
        help="Root directory for resolving local image paths (default: .).",
    )
    args = parser.parse_args(argv)

    # Resolve paths: expand directories → sorted *.md glob; files → as-is.
    resolved: list[str] = []
    for raw in args.paths:
        p = Path(raw)
        if not p.exists():
            print(f"error: path does not exist: {raw}", file=_sys.stderr)
            return 1
        if p.is_dir():
            md_files = sorted(glob.glob(str(p / "*.md")))
            if not md_files:
                # Empty directory is not an error — just nothing to lint.
                pass
            resolved.extend(md_files)
        else:
            resolved.append(str(p))

    asset_root = Path(args.asset_root)
    findings = lint_paths(resolved, asset_root=asset_root)

    for f in findings:
        print(f"{f.path}:{f.line} [{f.code}] {f.message}")

    return 1 if findings else 0


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(_cli_main())
