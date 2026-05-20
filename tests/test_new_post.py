# tests/test_new_post.py
"""Tests for scripts/new_post.py scaffold script."""
import subprocess
import sys
from pathlib import Path

import pytest


def _copy_script(tmp_path: Path) -> None:
    """Copy the script to tmp_path so it runs from there."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    src = Path("scripts/new_post.py").read_text(encoding="utf-8")
    (scripts_dir / "new_post.py").write_text(src, encoding="utf-8")


@pytest.fixture
def post_env(tmp_path: Path) -> Path:
    """Set up a minimal environment: tmp_path with scripts/ and _posts/."""
    _copy_script(tmp_path)
    (tmp_path / "_posts").mkdir(exist_ok=True)
    return tmp_path


def test_scaffold_emits_valid_yaml_front_matter(post_env: Path) -> None:
    """Scaffold creates a file with parseable YAML front matter."""
    result = subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "Test Post",
         "--slug", "test-post",
         "--date", "2026-05-20",
         "--categories", "hardware"],
        capture_output=True, text=True, cwd=str(post_env),
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    output_file = post_env / "_posts" / "2026-05-20-test-post.md"
    assert output_file.exists(), "Expected output file to be created"
    content = output_file.read_text(encoding="utf-8")
    # Front matter must start with ---
    assert content.startswith("---\n"), "File must start with YAML front matter"
    # Required keys must be present
    for key in ("author: mithro", "layout: post", "title: Test Post",
                 "categories:", "- hardware", "permalink: /archives/hardware/test-post"):
        assert key in content, f"Missing expected front matter key/value: {key!r}"
    # No wordpress_* keys in new posts
    for wp_key in ("wordpress_id", "wordpress_url", "wordpress_category"):
        assert wp_key not in content, f"New post must not contain {wp_key!r}"


def test_scaffold_refuses_to_overwrite_existing_file(post_env: Path) -> None:
    """Scaffold exits non-zero when the output file already exists."""
    existing = post_env / "_posts" / "2026-05-20-my-post.md"
    existing.write_text("existing content\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "My Post",
         "--slug", "my-post",
         "--date", "2026-05-20"],
        capture_output=True, text=True, cwd=str(post_env),
    )
    assert result.returncode != 0, "Script must exit non-zero when file exists"
    assert "already exists" in result.stderr.lower() or "ERROR" in result.stderr, (
        "Script must print an error about the existing file"
    )
    # Original file must be untouched
    assert existing.read_text(encoding="utf-8") == "existing content\n"


def test_scaffold_warns_on_unknown_category(post_env: Path) -> None:
    """Scaffold prints a WARNING (not an error) for unrecognized category slugs."""
    result = subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "Future Post",
         "--slug", "future-post",
         "--date", "2026-05-20",
         "--categories", "not-a-known-category"],
        capture_output=True, text=True, cwd=str(post_env),
    )
    # Must succeed (warning, not error)
    assert result.returncode == 0, f"Unknown category must warn, not fail: {result.stderr}"
    assert "WARNING" in result.stderr, "Must print a WARNING for unknown category"
    # File must still be created
    assert (post_env / "_posts" / "2026-05-20-future-post.md").exists()


def test_scaffold_output_passes_lint_content(post_env: Path) -> None:
    """Generated file passes the lint_content linter (zero findings)."""
    subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "Lint Test Post",
         "--slug", "lint-test-post",
         "--date", "2026-05-20",
         "--categories", "uncategorized"],
        capture_output=True, text=True, cwd=str(post_env), check=True,
    )
    # Import lint_text from the repo (not from post_env, which lacks the module)
    from scripts.fidelity.lint_content import lint_text
    content = (post_env / "_posts" / "2026-05-20-lint-test-post.md").read_text(encoding="utf-8")
    findings = lint_text("test-post.md", content)
    assert findings == [], (
        f"Scaffold output must pass lint_content with zero findings, got: {findings}"
    )


def test_scaffold_default_category_is_uncategorized(post_env: Path) -> None:
    """When --categories is omitted, defaults to uncategorized."""
    result = subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "Default Cat",
         "--slug", "default-cat",
         "--date", "2026-05-20"],
        capture_output=True, text=True, cwd=str(post_env),
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    content = (post_env / "_posts" / "2026-05-20-default-cat.md").read_text(encoding="utf-8")
    assert "- uncategorized" in content
    assert "/archives/uncategorized/default-cat" in content


def test_scaffold_normalizes_slug(post_env: Path) -> None:
    """Slug with uppercase/spaces is auto-normalized to lowercase-hyphenated form."""
    result = subprocess.run(
        [sys.executable, "scripts/new_post.py",
         "--title", "Normalization Test",
         "--slug", "My Post Slug!",
         "--date", "2026-05-20"],
        capture_output=True, text=True, cwd=str(post_env),
    )
    # Must succeed (normalize, not reject)
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    # Normalized slug: lowercase, spaces → hyphens, '!' stripped
    normalized = "my-post-slug"
    assert (post_env / "_posts" / f"2026-05-20-{normalized}.md").exists(), (
        f"Expected file 2026-05-20-{normalized}.md after slug normalization"
    )
    # Warning must be printed to stderr
    assert "WARNING" in result.stderr and normalized in result.stderr, (
        "Must print a WARNING with the normalized slug"
    )
