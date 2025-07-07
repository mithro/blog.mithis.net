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

## Important: Working Directory

**CRITICAL**: Always check the current working directory before running any commands. Use `pwd` to verify you are in the correct location before executing any bash commands, file operations, or git commands.

## Git Workflow Guidelines

**CRITICAL**: Commit often with small, focused changes:

- **Commit frequently**: After completing each logical unit of work (fixing one issue, adding one feature, completing one sub-task)
- **Keep commits small**: Each commit should represent a single, atomic change that can be easily understood and reverted if needed
- **Write clear commit messages**: 
  - Use imperative mood ("Add feature" not "Added feature")
  - First line: brief summary (50 chars or less)
  - Include context about what changed and why
  - Reference task IDs or issue numbers when applicable
- **Stage changes thoughtfully**: Use `git add` to stage only related changes together
- **Review before committing**: Use `git diff --staged` to review what you're about to commit

### Example Good Commits:
```
Add Jekyll site structure and basic _config.yml
Convert Barthelme header.php to Jekyll include
Fix responsive navigation for mobile devices
Update migration plan with Phase 1 detailed sub-tasks
```

### Avoid:
- Large commits with multiple unrelated changes
- Vague commit messages like "fix stuff" or "update files"
- Committing work-in-progress or broken code
- Including multiple features or fixes in one commit

## Recommended Tools for Migration Project

### Essential Development Tools
```bash
# Install Ruby version manager
curl -sSL https://get.rvm.io | bash

# Install Jekyll dependencies
gem install bundler jekyll

# WordPress content export
gem install wordpress-to-jekyll-exporter

# Image optimization
brew install imageoptim-cli  # macOS
# or apt-get install imagemagick  # Linux

# Link checking
npm install -g broken-link-checker

# HTML/CSS validation
npm install -g html-validate
```

### Migration-Specific Tools
- **wordpress-to-jekyll-exporter**: WordPress plugin for content export
- **Jekyll Import**: Ruby gem for importing from various sources
- **Pandoc**: Universal document converter for complex content
- **ImageMagick**: Batch image processing and optimization
- **wget**: Download entire WordPress media library
- **ripgrep (rg)**: Fast text search for content analysis

### Testing and Validation Tools
- **Lighthouse CLI**: Performance and accessibility auditing
- **Pa11y**: Command-line accessibility testing
- **HTMLProofer**: Jekyll plugin for link/image validation
- **W3C Validator**: HTML/CSS validation service
- **SEO testing tools**: screaming-frog-seo-spider (for URL mapping)

### Development Environment Helpers
- **Live Server**: Real-time preview during development
- **Browser Developer Tools**: Essential for theme recreation
- **Git hooks**: Automated testing before commits
- **GitHub CLI (gh)**: Streamlined repository management

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

# Alternative: Use wordpress-to-jekyll-exporter plugin
# Install plugin in WordPress admin, then export

# Download WordPress media library
wget -r -np -k -E -p https://blog.mithis.net/wp-content/uploads/

# Convert WordPress export to Jekyll
bundle exec jekyll import wordpress --source exports/wordpress.xml

# Convert complex content with Pandoc
pandoc input.html -o output.md

# Batch process images
imageoptim **/*.{jpg,jpeg,png}

# Check for broken links
blc http://localhost:4000 --recursive
```

### Theme Development Helper Commands
```bash
# Extract CSS from live WordPress site
curl -s https://blog.mithis.net | grep -o 'href="[^"]*\.css[^"]*"' | sed 's/href="//;s/"//' | xargs -I {} curl -s {} > extracted-styles.css

# Compare theme files
diff -u theme_analysis/barthelme/style.css assets/css/main.scss

# Validate HTML output
html-validate _site/**/*.html

# Test responsive design
lighthouse http://localhost:4000 --view

# Check accessibility
pa11y http://localhost:4000
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

Reference `MIGRATION_PLAN.md` for the comprehensive migration plan with:
- **4 phases** with detailed sub-tasks and testing requirements
- **60+ specific action items** broken down from 25 main tasks
- **10-14 week timeline** with critical path identification
- **Quality assurance framework** with acceptance criteria
- **Resource lists** for tools, testing, and development environment

Key high-priority tasks include:
- Jekyll site initialization and configuration
- WordPress content export and conversion
- Theme recreation using files in `theme_analysis/barthelme/`
- Comment system migration and implementation
- Comprehensive testing and quality assurance

## Task Management Approach

When working on migration tasks:
1. **Check current todo list** for active tasks
2. **Reference MIGRATION_PLAN.md** for detailed sub-tasks and testing requirements
3. **Use recommended tools** listed above for efficient development
4. **Follow acceptance criteria** before marking tasks complete
5. **Update todo status** frequently to track progress
6. **Document issues** and solutions in project files

### Productivity Tips
- **Use ripgrep (rg)** instead of grep for faster searching
- **Install HTMLProofer** gem for automated link checking during builds
- **Set up live reload** for instant preview during theme development
- **Use browser dev tools** extensively for CSS extraction and debugging
- **Run validation tools** frequently to catch issues early
- **Batch process images** with ImageMagick for consistent optimization
- **Commit early and often** - don't wait until large features are complete
- **Use `git status`** frequently to track changes and ensure nothing is missed
- **Review staged changes** with `git diff --staged` before each commit

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