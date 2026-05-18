# scripts/fidelity/render.py
"""Local visual layer: screenshot + DOM snapshot per archetype against a served
Jekyll site. Uses the Playwright Python library (the Playwright MCP is the
separate interactive tool). Not a CI gate (spec §6.2)."""
from __future__ import annotations
from pathlib import Path
from .archetypes import ARCHETYPES

def capture_all(base_url: str, out_dir: str | Path,
                viewport=(1280, 1024)) -> dict[str, dict]:
    from playwright.sync_api import sync_playwright  # lazy: optional dep
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport[0],
                                           "height": viewport[1]})
        for a in ARCHETYPES:
            url = base_url.rstrip("/") + a.path
            png = out / f"{a.name}.png"
            html = out / f"{a.name}.html"
            try:
                # NOT 'networkidle': the original Picasa header hotlinks dead
                # Google CDN images, so the network never goes idle and every
                # capture would burn the full timeout. 'domcontentloaded' + a
                # short settle captures local CSS/layout without the stall.
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(1500)
                page.screenshot(path=str(png), full_page=True)
                html.write_text(page.content(), encoding="utf-8")
                results[a.name] = {"url": url, "png": str(png),
                                   "html": str(html), "ok": True}
            except Exception as e:  # record, never abort the sweep
                results[a.name] = {"url": url, "ok": False, "error": repr(e)}
        browser.close()
    return results
