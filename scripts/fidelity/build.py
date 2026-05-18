# scripts/fidelity/build.py
"""Jekyll build gate. detect_problems() is pure and unit-tested; run_build()
wraps the same command CI runs and fails on any detected problem."""
from __future__ import annotations
import re
import shutil
import subprocess

# Jekyll's actual problem signatures (avoid matching benign "Generating..." etc.)
_PROBLEM = re.compile(
    r"(Liquid (Exception|Warning|syntax error))"
    r"|(^\s*Error:)"
    r"|(^\s*jekyll \d.*Error)"
    r"|(Deprecation:)"
    r"|(\bwarning:\s)"
    r"|(Build Warning:)"
    r"|(Conflict:)",
    re.IGNORECASE | re.MULTILINE,
)

def detect_problems(log: str) -> list[str]:
    return [ln.strip() for ln in log.splitlines() if _PROBLEM.search(ln)]

def bundler() -> str:
    """Resolve the Bundler executable. Debian names it 'bundle3.3'; most
    machines and CI provide 'bundle'. Portable across both."""
    return shutil.which("bundle") or shutil.which("bundle3.3") or "bundle"

def run_build(baseurl: str = "") -> tuple[bool, str]:
    cmd = [bundler(), "exec", "jekyll", "build", "--trace"]
    if baseurl:
        cmd += ["--baseurl", baseurl]
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = (p.stdout or "") + "\n" + (p.stderr or "")
    ok = p.returncode == 0 and not detect_problems(log)
    return ok, log
