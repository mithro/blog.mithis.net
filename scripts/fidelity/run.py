# scripts/fidelity/run.py
"""P0 exit-gate runner: build -> serve -> render -> structural diff vs Barthelme
-> lint posts -> write tmp/fidelity/fidelity-report.md.

Exit policy (spec P0 gate): exit 1 if the build is NOT clean OR the content
linter has findings. Structural results are REPORTED (P1 input) and do not, by
themselves, fail P0 — P0's job is to measure, not to be all-green."""
from __future__ import annotations
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

from .archetypes import structural_archetypes
from .build import bundler, run_build
from .compare import structural_diff
from .lint_content import lint_paths
from .report import render_report

OUT = Path("tmp/fidelity")
BARTHELME = Path("theme_analysis/barthelme")

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    build_ok, log = run_build()

    structural = []
    render_error = ""
    # spec §6.2: the P0 CI-able gate is build + linter + structural-comparator
    # — NO browser, and therefore NO served site. The jekyll serve exists ONLY
    # to feed the Playwright visual layer, so it lives entirely inside the
    # render branch. Skipping render skips the serve too: this keeps the gate
    # path server-free (no orphaned jekyll-serve to keep the process group
    # alive). The render path is the local, non-gating step (not meaningful
    # until P4 sets baseurl="" so served URLs resolve).
    if os.environ.get("FIDELITY_SKIP_RENDER"):
        rendered = {}
        render_error = "skipped via FIDELITY_SKIP_RENDER (spec §6.2 local layer)"
    else:
        rendered = {}
        proc = None
        serve_log = open(OUT / "jekyll-serve.log", "w", encoding="utf-8")
        try:
            # --skip-initial-build serves the _site produced by run_build().
            # serve output -> log file (NOT DEVNULL) so a flaky serve is
            # debuggable and stderr stays visible.
            proc = subprocess.Popen(
                [bundler(), "exec", "jekyll", "serve", "--port", "4000",
                 "--skip-initial-build", "--no-watch"],
                stdout=serve_log, stderr=subprocess.STDOUT)
            time.sleep(6)
            try:
                from .render import capture_all
                rendered = capture_all("http://localhost:4000", OUT / "jekyll")
            except Exception as e:
                render_error = repr(e)
        finally:
            # Reliably reap the server (terminate -> wait -> hard kill) so it
            # never orphans and hangs the caller's process group.
            if proc:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
            serve_log.close()

    for a in structural_archetypes():
        r = rendered.get(a.name, {})
        html = (Path(r["html"]).read_text(encoding="utf-8")
                if r.get("ok") else "")
        php = (BARTHELME / a.barthelme_template).read_text(
            encoding="utf-8", errors="replace")
        structural.append(structural_diff(a.name, php, html))

    findings = lint_paths(sorted(glob.glob("_posts/*.md")), asset_root=".")

    report = render_report(build_ok=build_ok, build_log_tail=log[-1500:],
                           structural=structural, lint=findings)
    if render_error:
        report += ("\n## Renderer\n\nPlaywright visual layer NOT RUN "
                   "(spec §6.2: local, non-gating). Structural results above "
                   "reflect NO rendered HTML (every Barthelme anchor shows as "
                   "missing) — re-run locally with a browser (after P4 sets "
                   "baseurl=\"\" so served URLs resolve) for the real "
                   f"structural diff.\nReason: {render_error}\n")
    (OUT / "fidelity-report.md").write_text(report, encoding="utf-8")
    print(report)

    return 0 if (build_ok and not findings) else 1

if __name__ == "__main__":
    sys.exit(main())
