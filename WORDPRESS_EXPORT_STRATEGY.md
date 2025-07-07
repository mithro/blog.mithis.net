# WordPress Export Strategy for blog.mithis.net

## Content Analysis Summary

### Blog Overview
- **Timeline**: 2006-2020 (14+ years of content)
- **Content Focus**: Technical blog about open source hardware/software development
- **Author**: Tim "mithro" Ansell
- **Primary Projects**: HDMI2USB, TimVideos.us, GSoC work

### Content Structure
- **Post Count**: Estimated 100+ posts across 14 years
- **Recent Activity**: 10 posts in RSS feed, latest May 2, 2020
- **Categories**: Hardware, Python, TimVideos.us, HDMI2USB, Summer of Code, Useful Bits, Linux.conf.au
- **URL Pattern**: `/archives/[category]/[descriptive-title]/`
- **Comments**: WordPress native comment system

### Content Types to Export
1. **Blog Posts** - Main content with technical articles
2. **Pages** - Static pages (About, Contact, etc.)
3. **Comments** - User comments and interactions
4. **Media** - Images, attachments, project photos
5. **Categories & Tags** - Taxonomies for organization
6. **Custom Fields** - Any WordPress metadata

## Export Methods

### Method 1: WordPress Admin Export (Recommended)
**Requirements**: Access to WordPress admin dashboard

**Steps**:
1. Log into WordPress admin at `https://blog.mithis.net/wp-admin/`
2. Navigate to Tools → Export
3. Select "All content" or specific content types
4. Download the WordPress XML export file
5. Place in `exports/` directory

**Exports**:
- `wordpress-export.xml` - Complete content export
- Media files - Download separately via FTP/admin

### Method 2: RSS Feed Extraction (Fallback)
**Use Case**: If admin access unavailable

**Steps**:
1. Extract recent posts from RSS feed
2. Use web scraping for older content
3. Manual categorization and metadata extraction

### Method 3: WP-CLI Export (If Server Access Available)
**Requirements**: SSH access to hosting server

**Commands**:
```bash
wp export --dir=exports/
wp media export --dir=exports/media/
```

## Export Preparation Checklist

### Pre-Export Setup
- [ ] Create `exports/` directory
- [ ] Verify backup of current WordPress site
- [ ] Document current permalink structure
- [ ] List all categories and tags
- [ ] Identify custom post types or fields

### Content Export Process
- [ ] Export all posts and pages
- [ ] Export comments and metadata
- [ ] Download media library
- [ ] Export user accounts (author info)
- [ ] Export theme customizations
- [ ] Export plugin data (if relevant)

### Post-Export Validation
- [ ] Verify post count matches expectations
- [ ] Check category/tag preservation
- [ ] Validate image references
- [ ] Confirm comment associations
- [ ] Test XML file integrity

## Migration Priorities

### Phase 1: Core Content
1. **Posts** - All blog posts with metadata
2. **Categories/Tags** - Taxonomy preservation
3. **Publication Dates** - Maintain chronological order
4. **URLs** - Preserve permalink structure

### Phase 2: Enhanced Content
1. **Comments** - Migrate to chosen comment system
2. **Media** - Download and optimize images
3. **Pages** - Static content migration
4. **Author Info** - Profile and metadata

### Phase 3: Optimization
1. **URL Redirects** - Map old URLs to new structure
2. **Image Optimization** - Compress and resize
3. **Content Cleanup** - Remove WordPress-specific markup
4. **SEO Preservation** - Meta tags and descriptions

## Technical Considerations

### WordPress-Specific Elements to Convert
- **Shortcodes** - Convert to Markdown/HTML equivalents
- **WordPress Embeds** - Convert to standard embeds
- **Custom Fields** - Map to Jekyll front matter
- **Featured Images** - Convert to Jekyll post images
- **Excerpts** - Preserve in Jekyll front matter

### URL Structure Mapping
```
WordPress: /archives/[category]/[post-name]/
Jekyll:    /[year]/[month]/[post-name]/
```

### Content Format Conversion
- **HTML → Markdown** - Primary content conversion
- **Categories → Jekyll Categories** - Direct mapping
- **Tags → Jekyll Tags** - Direct mapping
- **Custom Fields → Front Matter** - YAML conversion

## Expected Output Structure

### Jekyll Directory Structure
```
_posts/
  2020-05-02-gsoc-2020-nmigen-projects.md
  2020-04-15-hdmi2usb-production-board.md
  [year-month-date-title.md]

assets/
  images/
    2020/
    2019/
    [year-based organization]

_data/
  comments/
    [post-slug]/
      [comment-files]
```

### Front Matter Template
```yaml
---
layout: post
title: "Post Title"
date: 2020-05-02 10:30:00 -0700
categories: [Hardware, Python]
tags: [hdmi2usb, gsoc, open-source]
author: mithro
excerpt: "Post excerpt for listings"
---
```

## Tools and Scripts Needed

### Conversion Tools
- `wordpress-to-jekyll-exporter` - WordPress plugin
- `jekyll-import` - Ruby gem for various import sources
- `pandoc` - Document format conversion
- Custom scripts for specific content transformations

### Download Scripts
- `wget` - Recursive media download
- Custom image optimization scripts
- URL mapping generators

## Success Metrics

### Content Integrity
- [ ] 100% of posts migrated
- [ ] All categories/tags preserved
- [ ] Publication dates maintained
- [ ] Author information preserved

### URL Preservation
- [ ] All old URLs redirect properly
- [ ] Internal links updated
- [ ] External links maintained
- [ ] SEO rankings preserved

### Visual Fidelity
- [ ] All images display correctly
- [ ] Formatting preserved
- [ ] Code blocks rendered properly
- [ ] Embeds working correctly

## Next Steps

1. **Immediate**: Gain access to WordPress admin or explore RSS-based extraction
2. **Content Export**: Execute chosen export method
3. **Validation**: Verify export completeness
4. **Conversion**: Begin Jekyll format transformation
5. **Testing**: Validate converted content accuracy

This strategy provides multiple paths for content export while ensuring comprehensive migration of 14+ years of technical blog content.