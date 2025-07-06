# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the migration project for converting Tim "mithro" Ansell's WordPress blog (https://blog.mithis.net) to a Jekyll-based static site. The project preserves existing content, comments, and theme styling while removing broken integrations.

## Architecture

The project follows a 4-phase migration approach:

1. **Foundation Setup**: Jekyll initialization, WordPress content export, theme recreation
2. **Core Functionality**: Site structure, dynamic features, comment system
3. **Enhancement**: Cleanup, analytics, performance optimization  
4. **Deployment**: Testing, URL management, hosting setup

## Key Migration Requirements

- **Content Preservation**: All WordPress posts, metadata (categories, tags, dates), and user comments must be preserved
- **Theme Fidelity**: Recreate the Barthelme WordPress theme appearance in Jekyll
- **URL Structure**: Maintain WordPress permalink structure with proper redirects
- **Content Focus**: Technical blog about open source hardware, software development, and tech projects
- **Remove Broken Features**: Twitter integration and Google Picasa integration

## Development Commands

### Jekyll Development
```bash
# Initialize Jekyll site
bundle exec jekyll new . --force

# Serve development site
bundle exec jekyll serve

# Build production site
bundle exec jekyll build

# Build with environment
JEKYLL_ENV=production bundle exec jekyll build
```

### Content Migration
```bash
# Export WordPress content (when WordPress access available)
wp export --dir=exports/

# Convert WordPress to Jekyll (using wordpress-to-jekyll-exporter or custom scripts)
# Scripts should be placed in _scripts/ directory
```

## Technical Stack

- **Static Site Generator**: Jekyll
- **Ruby Management**: rbenv or rvm recommended
- **Required Gems**: jekyll, jekyll-feed, jekyll-sitemap, jekyll-redirect-from
- **Hosting Options**: GitHub Pages, Netlify, Vercel, or traditional VPS
- **Comment System**: Disqus, Utterances, or static comments (to be determined)

## Content Structure

- **Source Blog**: WordPress with Barthelme theme
- **Content Types**: Technical posts with code highlighting, categories, tags
- **Special Features**: Syntax highlighting, RSS feeds, search functionality
- **Assets**: Images from WordPress uploads directory need migration and optimization

## Migration Checklist

Reference `MIGRATION_PLAN.md` for the complete 25-task checklist organized by priority. Key high-priority tasks include:
- Jekyll site initialization and configuration
- WordPress content export and conversion
- Theme recreation and responsive design
- Comment system migration
- Testing and quality assurance

## SEO and URL Considerations

- Preserve existing WordPress URL structure where possible
- Implement proper 301 redirects for changed URLs  
- Maintain meta descriptions, titles, and internal linking
- Ensure RSS feeds continue working at expected URLs

## Performance Goals

- Improve loading times over WordPress version
- Optimize images during migration
- Implement CDN if needed
- Static generation should provide significant performance benefits