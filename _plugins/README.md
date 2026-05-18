# Jekyll Plugins

This directory contains custom Jekyll plugins for automating site generation.

## Note: GitHub Pages Limitation

**Important**: GitHub Pages does not support custom Jekyll plugins for security reasons. Any plugins added to this directory will only work if you:

1. Build the site locally and push the generated `_site` folder
2. Use GitHub Actions to build the site with custom plugins
3. Host on a platform that supports custom Jekyll plugins (Netlify, Vercel, etc.)

## Plugins

_None currently._

### Category feeds (no plugin)

Per-category RSS feeds are produced by the committed static
`category/<category>/feed.xml` source files (front matter
`permalink: /category/<category>/feed/`), not by a generator plugin.

A previous `category_feed_generator.rb` plugin was removed because it
registered a second page at the identical destination
(`_site/category/<category>/feed/index.xml`) as those static files,
causing nondeterministic `Conflict:` build warnings. The static files
are portable (they also work on GitHub Pages, where custom plugins do
not run) and render the same RSS content, so they are the single
source of truth for category feeds.
