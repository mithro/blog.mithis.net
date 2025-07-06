# WordPress to Jekyll Migration Plan

## Project Overview
This document outlines the comprehensive plan for migrating the WordPress blog at https://blog.mithis.net to a new Jekyll-based static site while preserving existing content, comments, and theme styling.

## Current WordPress Blog Analysis
- **Theme**: Barthelme WordPress theme
- **Author**: Tim "mithro" Ansell
- **Content Focus**: Open source hardware, software development, tech projects
- **Key Features**: Technical posts, code highlighting, categories/tags, comments, RSS feeds
- **Broken Features**: Twitter integration, Google Picasa integration (to be removed)

## Migration Objectives
1. Preserve all existing blog content and metadata
2. Maintain current theme appearance and styling
3. Migrate user comments to new system
4. Remove broken integrations (Twitter, Google Picasa)
5. Improve site performance with static generation
6. Maintain SEO and URL structure

## Phase 1: Foundation Setup (High Priority)

### 1.1 Jekyll Site Structure
- [ ] Initialize Jekyll site with proper directory structure
- [ ] Configure `_config.yml` with site metadata
- [ ] Set up development environment and dependencies
- [ ] Create basic layout templates

### 1.2 Content Export and Migration
- [ ] Export WordPress content using WP-CLI or WordPress export tool
- [ ] Convert WordPress posts to Jekyll markdown format
- [ ] Preserve all post metadata (categories, tags, publish dates, authors)
- [ ] Export and migrate WordPress comments to Jekyll-compatible format
- [ ] Migrate and optimize all images from WordPress uploads directory

### 1.3 Theme Recreation
- [ ] Recreate Barthelme theme styling in Jekyll/CSS
- [ ] Implement responsive layout matching current design
- [ ] Ensure cross-browser compatibility
- [ ] Optimize CSS for performance

## Phase 2: Core Functionality (Medium Priority)

### 2.1 Site Structure
- [ ] Set up Jekyll collections for different content types
- [ ] Implement category and tag archive pages
- [ ] Create proper navigation structure
- [ ] Set up permalink structure to match WordPress URLs

### 2.2 Dynamic Features
- [ ] Create search functionality (client-side or plugin-based)
- [ ] Set up RSS feed generation for posts
- [ ] Implement syntax highlighting for code blocks
- [ ] Create contact page and about page

### 2.3 Comment System
- [ ] Evaluate comment system options (Disqus, Utterances, static comments)
- [ ] Implement chosen comment system
- [ ] Migrate existing WordPress comments
- [ ] Test comment functionality

## Phase 3: Enhancement and Optimization (Low Priority)

### 3.1 Cleanup and Removal
- [ ] Remove broken Twitter integration
- [ ] Remove broken Google Picasa integration
- [ ] Clean up any deprecated WordPress-specific code

### 3.2 Analytics and Tracking
- [ ] Implement Google Analytics tracking
- [ ] Set up performance monitoring
- [ ] Configure error tracking

### 3.3 Performance Optimization
- [ ] Optimize site performance and loading times
- [ ] Implement image optimization
- [ ] Set up content delivery network (CDN) if needed
- [ ] Create 404 error page

## Phase 4: Deployment and Testing (Medium-High Priority)

### 4.1 Deployment Setup
- [ ] Set up automated deployment pipeline (GitHub Actions, Netlify, etc.)
- [ ] Configure domain and hosting
- [ ] Set up SSL certificates
- [ ] Create backup and rollback plan

### 4.2 URL Management
- [ ] Set up URL redirects for WordPress permalink structure
- [ ] Test all internal and external links
- [ ] Verify SEO metadata preservation

### 4.3 Testing and Quality Assurance
- [ ] Test all migrated content and functionality
- [ ] Verify comment system works correctly
- [ ] Test responsive design across devices
- [ ] Validate HTML/CSS/JavaScript
- [ ] Performance testing and optimization

## Technical Considerations

### Migration Tools
- **WordPress Export**: Use WP-CLI or WordPress admin export
- **Content Conversion**: Custom scripts or tools like `wordpress-to-jekyll-exporter`
- **Image Migration**: Batch download and optimization scripts
- **Comment Migration**: Disqus import or custom comment export

### Jekyll Setup
- **Ruby Version**: Use rbenv or rvm for version management
- **Gems**: jekyll, jekyll-feed, jekyll-sitemap, jekyll-redirect-from
- **Plugins**: Syntax highlighting, search, SEO optimization

### Hosting Options
- **GitHub Pages**: Free hosting with Jekyll support
- **Netlify**: Advanced features, build optimization
- **Vercel**: Fast deployment and edge optimization
- **Traditional hosting**: VPS with Jekyll build process

## Risk Mitigation

### Data Loss Prevention
- Complete WordPress database backup before migration
- Export all media files and attachments
- Version control all migration scripts and content

### SEO Preservation
- Maintain URL structure where possible
- Implement proper redirects for changed URLs
- Preserve meta descriptions and titles
- Maintain internal linking structure

### User Experience
- Test thoroughly before going live
- Plan for gradual rollout if possible
- Monitor for broken links post-migration
- Ensure comment system works seamlessly

## Timeline Estimate

- **Phase 1**: 2-3 weeks (Foundation Setup)
- **Phase 2**: 2-3 weeks (Core Functionality)
- **Phase 3**: 1-2 weeks (Enhancement)
- **Phase 4**: 1-2 weeks (Deployment & Testing)

**Total Estimated Time**: 6-10 weeks

## Success Criteria

1. All WordPress content successfully migrated
2. All existing comments preserved and functional
3. Theme appearance matches original WordPress site
4. Site performance improved over WordPress version
5. All URLs working with proper redirects
6. SEO rankings maintained
7. Broken integrations removed
8. New comment system functional

## Next Steps

1. Begin with Phase 1 foundation setup
2. Set up development environment
3. Export WordPress content for analysis
4. Start Jekyll site initialization

This migration plan provides a comprehensive roadmap for successfully transitioning from WordPress to Jekyll while maintaining content integrity and user experience.