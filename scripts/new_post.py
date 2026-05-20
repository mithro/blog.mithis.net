"""scripts/new_post.py — scaffold a new Jekyll blog post.

Usage:
    uv run python scripts/new_post.py \\
        --title "Post Title Here" \\
        --slug my-post-slug \\
        [--date YYYY-MM-DD] \\
        [--categories slug1,slug2]

Creates _posts/<date>-<slug>.md with correct new-post front matter.
Refuses to overwrite an existing file.
Warns on unrecognized category slugs.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

# The 22+1 known category slugs (established by P0–PSC migration phases).
KNOWN_CATEGORIES: set[str] = {
    "diary",
    "games",
    "gaming-miniconf",
    "google",
    "hardware",
    "hdmi2usb",
    "highlights",
    "ideas",
    "lca",
    "pcb",
    "python",
    "rcs-darcs",
    "rcs-tailor",
    "sci-fi",
    "scheme",
    "summer-of-code",
    "sydney",
    "timvideos-us",
    "tp",
    "ubuntu",
    "uncategorized",
    "uni",
    "useful-bits",
}

# Front matter template for new (non-WP-imported) posts.
# No wordpress_* keys — the post layout derives the comment slug from page.path.
TEMPLATE = """\
---
author: mithro
categories:
{categories_yaml}
date: {date} 12:00:00 +1000
excerpt: 'TODO: Add 1-2 sentence summary here ending with ...'
layout: post
permalink: /archives/{primary_category}/{slug}
title: {title}
---
TODO: Write your post content here.

Use Markdown formatting:
- Blank lines between paragraphs
- ``` fenced code blocks for code (with language tag)
- **bold** and *italic* for emphasis
- [link text](URL) for links
- ![alt text](/assets/images/YYYY/filename.png) for images

No hardcoded HTML block elements (div, ul, ol, li, p, h1-h6, table, pre, etc.)
— the content linter will fail the CI build if found.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new Jekyll blog post with correct front matter.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Post title (used verbatim in front matter title: field).",
    )
    parser.add_argument(
        "--slug",
        required=True,
        help="URL slug for the post filename and permalink.",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Post date as YYYY-MM-DD (default: today).",
    )
    parser.add_argument(
        "--categories",
        default="uncategorized",
        help="Comma-separated category slugs from the 22+1 list (default: uncategorized).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Normalize slug: lowercase, replace non-[a-z0-9-] with hyphens, strip leading/trailing hyphens
    raw_slug = args.slug
    normalized_slug = re.sub(r"[^a-z0-9-]+", "-", raw_slug.lower()).strip("-")
    if normalized_slug != raw_slug:
        print(
            f"WARNING: slug {raw_slug!r} normalized to {normalized_slug!r}.",
            file=sys.stderr,
        )
    if not normalized_slug:
        print("ERROR: --slug produced an empty string after normalization.", file=sys.stderr)
        return 1
    args.slug = normalized_slug

    # Resolve date
    if args.date:
        try:
            post_date = datetime.date.fromisoformat(args.date)
        except ValueError:
            print(f"ERROR: --date must be YYYY-MM-DD, got: {args.date!r}", file=sys.stderr)
            return 1
    else:
        post_date = datetime.date.today()

    date_str = post_date.isoformat()  # YYYY-MM-DD

    # Resolve categories
    slugs = [s.strip() for s in args.categories.split(",") if s.strip()]
    if not slugs:
        slugs = ["uncategorized"]

    # Warn on unrecognized slugs (not an error — allows future categories)
    for slug in slugs:
        if slug not in KNOWN_CATEGORIES:
            print(
                f"WARNING: unrecognized category slug {slug!r} — not in the 22+1 known list.",
                file=sys.stderr,
            )
            print(
                "  If this is a new category, create category/<slug>.md first (see docs/AUTHORING.md §4).",
                file=sys.stderr,
            )

    primary_category = slugs[0]
    categories_yaml = "\n".join(f"- {s}" for s in slugs)

    # Derive output path
    filename = f"{date_str}-{args.slug}.md"
    output_path = Path("_posts") / filename

    # Refuse to overwrite
    if output_path.exists():
        print(f"ERROR: file already exists: {output_path}", file=sys.stderr)
        print("  Use a different --slug or --date to avoid overwriting.", file=sys.stderr)
        return 1

    # Render template
    content = TEMPLATE.format(
        categories_yaml=categories_yaml,
        date=date_str,
        primary_category=primary_category,
        slug=args.slug,
        title=args.title,
    )

    # Write file
    output_path.write_text(content, encoding="utf-8")
    print(f"Created: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
