# WordPress Export Files

This directory contains exported content from the WordPress blog at https://blog.mithis.net

## Directory Structure

- `xml/` - WordPress XML export files
- `media/` - Downloaded images and attachments  
- `scripts/` - Custom conversion and migration scripts

## Export Process

1. **WordPress Admin Export**: Use Tools → Export in WordPress admin
2. **Media Download**: Download complete media library
3. **Validation**: Verify export completeness
4. **Conversion**: Transform to Jekyll format

## Files Expected

- `wordpress-export.xml` - Complete content export
- `posts-export.xml` - Posts-only export (if needed)
- `comments-export.xml` - Comments export
- `media/[year]/[month]/` - Organized media files

## Usage

These files will be processed by Jekyll import tools and custom scripts to migrate content to the new Jekyll-based blog.