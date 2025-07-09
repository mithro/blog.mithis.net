# Jekyll Plugins

This directory contains custom Jekyll plugins for automating site generation.

## Note: GitHub Pages Limitation

**Important**: GitHub Pages does not support custom Jekyll plugins for security reasons. The plugins in this directory will only work if you:

1. Build the site locally and push the generated `_site` folder
2. Use GitHub Actions to build the site with custom plugins
3. Host on a platform that supports custom Jekyll plugins (Netlify, Vercel, etc.)

## Plugins

### category_feed_generator.rb

Automatically generates RSS feeds for each category found in posts. This eliminates the need to manually create feed.xml files in each category directory.

**Usage**: The plugin automatically runs during site generation and creates feed pages at `/category/[category-name]/feed/` for each category.

**Template**: Uses the `category_feed.xml` layout in `_layouts/`.