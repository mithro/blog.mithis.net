# scripts/fidelity/report.py
"""Assemble tmp/fidelity/fidelity-report.md from component results."""
from __future__ import annotations
from .compare import StructuralResult
from .lint_content import Finding

def render_report(*, build_ok: bool, build_log_tail: str,
                  structural: list[StructuralResult],
                  lint: list[Finding]) -> str:
    s_ok = bool(structural) and all(r.passed for r in structural)
    n_ok = sum(1 for r in structural if r.passed)
    L: list[str] = ["# Fidelity Report", ""]
    L.append(f"- Build: {'PASS' if build_ok else 'FAIL'}")
    L.append(f"- Structural diff: {'PASS' if s_ok else 'FAIL'} "
             f"({n_ok}/{len(structural)} archetypes)")
    L.append(f"- Content linter: {'PASS' if not lint else 'FAIL'} "
             f"({len(lint)} finding(s))")
    L += ["", "## Structural", ""]
    for r in structural:
        L.append(f"### {r.archetype}: {'PASS' if r.passed else 'FAIL'}")
        for a in r.missing:
            L.append(f"- MISSING `{a.tag}{a.ident}`")
    L += ["", "## Content findings", ""]
    for f in lint:
        L.append(f"- {f.path}:{f.line} [{f.code}] {f.message}")
    if not build_ok and build_log_tail:
        L += ["", "## Build log (tail)", "", "```", build_log_tail, "```"]
    return "\n".join(L) + "\n"
