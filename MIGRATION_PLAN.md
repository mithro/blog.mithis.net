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
**Main Task**: Set up Jekyll site structure and basic configuration

**Sub-tasks**:
- [ ] Install Ruby and Jekyll dependencies
  - Install Ruby 3.0+ using rbenv or rvm
  - Install Bundler gem
  - Install Jekyll gem
- [ ] Initialize Jekyll site with proper directory structure
  - Run `bundle exec jekyll new . --force`
  - Create `_layouts/`, `_includes/`, `_sass/`, `assets/` directories
  - Set up `Gemfile` with required gems
- [ ] Configure `_config.yml` with site metadata
  - Set site title, description, and URL
  - Configure permalink structure to match WordPress
  - Add timezone and locale settings
  - Configure markdown processor and syntax highlighting
- [ ] Set up development environment
  - Create development scripts
  - Configure local server settings
  - Set up hot reload for development

**Testing**:
- [ ] Verify Jekyll site builds without errors
- [ ] Test local development server starts correctly
- [ ] Validate directory structure matches Jekyll conventions
- [ ] Check `_config.yml` syntax and settings

**Resources**:
- Jekyll documentation: https://jekyllrb.com/docs/
- Bundler documentation: https://bundler.io/
- Ruby installation guides for specific OS

### 1.2 Content Export and Migration
**Main Tasks**: Export WordPress content and convert to Jekyll format

**Sub-tasks**:
- [ ] **Export WordPress content**
  - Access WordPress admin dashboard
  - Use Tools > Export to generate XML file
  - Alternative: Use WP-CLI if server access available
  - Download complete media library
  - Export database for comment migration
- [ ] **Convert WordPress posts to Jekyll markdown**
  - Use `wordpress-to-jekyll-exporter` plugin or custom scripts
  - Convert HTML content to Markdown
  - Preserve post formatting and embedded media
  - Handle shortcodes and WordPress-specific markup
- [ ] **Migrate post metadata**
  - Preserve categories and tags
  - Maintain publish dates and author information
  - Convert WordPress custom fields
  - Set up front matter for Jekyll posts
- [ ] **Export and convert comments**
  - Extract comments from WordPress database
  - Convert to static comment format or prepare for external system
  - Preserve comment threading and metadata
  - Handle comment moderation status

**Testing**:
- [ ] Verify all posts exported successfully
- [ ] Check post count matches WordPress admin
- [ ] Validate metadata preservation (categories, tags, dates)
- [ ] Test markdown rendering of converted content
- [ ] Verify comment data integrity

**Resources**:
- WordPress Export Tool: WordPress Admin > Tools > Export
- wordpress-to-jekyll-exporter plugin
- Custom conversion scripts in `_scripts/` directory
- WP-CLI documentation for advanced exports

### 1.3 Theme Recreation
**Main Task**: Recreate Barthelme theme styling in Jekyll

**Sub-tasks**:
- [ ] **Convert CSS to SCSS**
  - Extract styles from `theme_analysis/barthelme/style.css`
  - Organize into modular SCSS files
  - Create variables for colors, fonts, and spacing
  - Set up SCSS compilation pipeline
- [ ] **Create Jekyll layout templates**
  - Convert `header.php` to `_includes/header.html`
  - Convert `footer.php` to `_includes/footer.html`
  - Convert `sidebar.php` to `_includes/sidebar.html`
  - Create `_layouts/default.html` from WordPress templates
  - Create `_layouts/post.html` for single posts
  - Create `_layouts/page.html` for static pages
- [ ] **Implement responsive design**
  - Add mobile-first CSS media queries
  - Ensure sidebar works on mobile devices
  - Test responsive typography scaling
  - Optimize touch targets for mobile
- [ ] **Preserve theme functionality**
  - Implement navigation menus
  - Create widget-equivalent includes
  - Add search functionality
  - Maintain microformats support (hAtom, hCard)

**Testing**:
- [ ] Visual comparison with original WordPress theme
- [ ] Cross-browser compatibility testing
- [ ] Mobile responsiveness testing
- [ ] Performance testing (page load times)
- [ ] Accessibility testing (WCAG compliance)
- [ ] Validate HTML and CSS

**Resources**:
- Original Barthelme theme files in `theme_analysis/`
- SCSS documentation: https://sass-lang.com/
- Jekyll theming guide: https://jekyllrb.com/docs/themes/
- Responsive design best practices

## Phase 2: Core Functionality (Medium Priority)

### 2.1 Site Structure
**Main Tasks**: Set up Jekyll collections and archive pages

**Sub-tasks**:
- [ ] **Set up Jekyll collections**
  - Configure collections in `_config.yml`
  - Create collection directories (`_posts/`, `_pages/`)
  - Set up collection-specific front matter defaults
  - Configure collection output and permalinks
- [ ] **Implement category and tag archive pages**
  - Create `_layouts/category.html` template
  - Create `_layouts/tag.html` template
  - Generate category and tag index pages
  - Set up category/tag pagination if needed
- [ ] **Create navigation structure**
  - Build main navigation menu
  - Implement breadcrumb navigation
  - Create sidebar navigation elements
  - Add "previous/next post" navigation
- [ ] **Configure permalink structure**
  - Match WordPress URL patterns
  - Set up custom permalinks in `_config.yml`
  - Create redirect rules for changed URLs
  - Test URL consistency with WordPress

**Testing**:
- [ ] Verify all collection pages render correctly
- [ ] Test category and tag archive functionality
- [ ] Validate navigation links work properly
- [ ] Check permalink structure matches WordPress
- [ ] Test pagination on archive pages

**Resources**:
- Jekyll Collections documentation
- Jekyll Pagination plugin
- URL structure planning spreadsheet

### 2.2 Dynamic Features
**Main Tasks**: Implement search, RSS, syntax highlighting, and static pages

**Sub-tasks**:
- [ ] **Create search functionality**
  - Evaluate options: Lunr.js, Algolia, or Simple-Jekyll-Search
  - Implement client-side search index generation
  - Create search results page layout
  - Add search box to header/sidebar
  - Test search accuracy and performance
- [ ] **Set up RSS feed generation**
  - Configure `jekyll-feed` plugin
  - Create custom RSS templates if needed
  - Set up category-specific RSS feeds
  - Add RSS links to header and sidebar
  - Validate RSS feed format
- [ ] **Implement syntax highlighting**
  - Configure Rouge or Prism.js for code highlighting
  - Set up language-specific highlighting
  - Style code blocks to match theme
  - Test various programming languages
  - Add copy-to-clipboard functionality
- [ ] **Create static pages**
  - Create About page with author information
  - Create Contact page with contact form or information
  - Create Archives page with post timeline
  - Create Privacy Policy and Terms pages if needed

**Testing**:
- [ ] Test search functionality across different queries
- [ ] Validate RSS feeds in feed readers
- [ ] Test syntax highlighting with various code languages
- [ ] Verify static pages render correctly
- [ ] Test contact form functionality (if implemented)

**Resources**:
- Jekyll plugins: jekyll-feed, jekyll-sitemap
- Search solutions: Lunr.js, Simple-Jekyll-Search
- Syntax highlighting: Rouge, Prism.js documentation
- Contact form services: Formspree, Netlify Forms

### 2.3 Comment System
**Main Tasks**: Evaluate, implement, and migrate comment system

**Sub-tasks**:
- [ ] **Evaluate comment system options**
  - Research Disqus integration and privacy concerns
  - Evaluate Utterances (GitHub-based comments)
  - Consider static comment systems (Staticman)
  - Assess comment moderation needs
  - Consider comment-free approach with contact alternatives
- [ ] **Implement chosen comment system**
  - Set up third-party service accounts
  - Integrate comment system into post layouts
  - Configure comment moderation settings
  - Style comments to match theme design
  - Implement comment notifications
- [ ] **Migrate existing WordPress comments**
  - Export comments from WordPress database
  - Convert comments to chosen system format
  - Preserve comment threading and relationships
  - Handle comment author information
  - Import comments to new system
- [ ] **Set up comment management**
  - Configure spam protection
  - Set up comment moderation workflow
  - Create comment policy page
  - Test comment submission and display

**Testing**:
- [ ] Test comment submission and display
- [ ] Verify comment threading works correctly
- [ ] Test comment moderation functionality
- [ ] Validate migrated comments display properly
- [ ] Test spam protection effectiveness
- [ ] Check comment notifications work

**Resources**:
- Disqus documentation and setup guide
- Utterances GitHub app setup
- Staticman documentation
- WordPress comment export tools
- Comment migration scripts

## Phase 3: Enhancement and Optimization (Low Priority)

### 3.1 Cleanup and Removal
**Main Tasks**: Remove broken integrations and deprecated code

**Sub-tasks**:
- [ ] **Remove broken Twitter integration**
  - Identify Twitter widget/feed code in WordPress
  - Remove Twitter-related PHP functions and CSS
  - Clean up any Twitter API calls or credentials
  - Replace with static social media links if desired
  - Test that removal doesn't break layout
- [ ] **Remove broken Google Picasa integration**
  - Identify Picasa/Google Photos integration code
  - Remove Picasa-related WordPress plugins or functions
  - Clean up any Picasa API calls or authentication
  - Migrate any essential images to local storage
  - Remove Picasa-related CSS and JavaScript
- [ ] **Clean up deprecated WordPress code**
  - Remove WordPress-specific shortcodes
  - Clean up deprecated HTML and CSS
  - Remove unused WordPress hooks and filters
  - Update any outdated HTML5 practices
  - Remove WordPress-specific JavaScript dependencies

**Testing**:
- [ ] Verify no broken links or missing assets
- [ ] Test that layout remains intact after cleanup
- [ ] Validate HTML and CSS after removal
- [ ] Check for JavaScript errors in browser console
- [ ] Test site functionality across different browsers

**Resources**:
- WordPress code documentation for identifying integrations
- Original WordPress site backup for reference
- Browser developer tools for debugging

### 3.2 Analytics and Tracking
**Main Tasks**: Implement analytics, monitoring, and error tracking

**Sub-tasks**:
- [ ] **Implement Google Analytics tracking**
  - Set up Google Analytics 4 (GA4) property
  - Configure goals and conversion tracking
  - Add tracking code to Jekyll layouts
  - Set up enhanced ecommerce tracking if needed
  - Configure custom events for important actions
- [ ] **Set up performance monitoring**
  - Implement Google PageSpeed monitoring
  - Set up Core Web Vitals tracking
  - Configure uptime monitoring (UptimeRobot or similar)
  - Monitor loading times and performance metrics
  - Set up alerts for performance degradation
- [ ] **Configure error tracking**
  - Implement error logging system
  - Set up 404 error monitoring
  - Monitor broken links and missing assets
  - Track JavaScript errors and exceptions
  - Set up email alerts for critical errors

**Testing**:
- [ ] Verify Google Analytics tracking is working
- [ ] Test event tracking and goal conversions
- [ ] Validate performance monitoring data
- [ ] Test error tracking and alert systems
- [ ] Check privacy compliance (GDPR/CCPA)

**Resources**:
- Google Analytics 4 setup documentation
- Google Search Console setup
- Performance monitoring tools: GTmetrix, WebPageTest
- Error tracking services: Sentry, LogRocket
- Privacy compliance guidelines

### 3.3 Performance Optimization
**Main Tasks**: Optimize performance, images, and implement CDN

**Sub-tasks**:
- [ ] **Optimize site performance**
  - Minimize and compress CSS and JavaScript
  - Implement critical CSS loading
  - Optimize font loading and reduce font files
  - Enable Gzip compression on server
  - Implement browser caching headers
- [ ] **Implement image optimization**
  - Compress and resize images for web
  - Implement responsive images with srcset
  - Convert images to modern formats (WebP, AVIF)
  - Implement lazy loading for images
  - Optimize SVG icons and graphics
- [ ] **Set up Content Delivery Network (CDN)**
  - Evaluate CDN options (Cloudflare, AWS CloudFront)
  - Configure CDN for static assets
  - Set up global edge caching
  - Configure CDN SSL certificates
  - Test CDN performance from different locations
- [ ] **Create optimized 404 error page**
  - Design custom 404 page matching theme
  - Add helpful navigation and search
  - Implement automatic redirect suggestions
  - Track 404 errors for analysis
  - Test 404 page functionality

**Testing**:
- [ ] Run performance audits (Lighthouse, PageSpeed)
- [ ] Test image loading and lazy loading
- [ ] Verify CDN functionality and caching
- [ ] Test 404 page user experience
- [ ] Validate performance improvements over WordPress
- [ ] Test site speed from multiple geographic locations

**Resources**:
- Google Lighthouse performance auditing
- Image optimization tools: ImageOptim, TinyPNG
- CDN providers: Cloudflare, AWS CloudFront
- Performance optimization guides
- Jekyll performance optimization plugins

## Phase 4: Deployment and Testing (Medium-High Priority)

### 4.1 Deployment Setup
**Main Tasks**: Set up hosting, deployment pipeline, and backup systems

**Sub-tasks**:
- [ ] **Set up automated deployment pipeline**
  - Choose deployment platform (GitHub Pages, Netlify, Vercel, or custom)
  - Configure GitHub Actions or platform-specific CI/CD
  - Set up staging and production environments
  - Configure build process and environment variables
  - Set up automated testing in deployment pipeline
- [ ] **Configure domain and hosting**
  - Transfer domain DNS to new hosting provider
  - Configure DNS records for blog.mithis.net
  - Set up subdomain redirects if needed
  - Configure hosting environment for Jekyll
  - Test domain propagation and resolution
- [ ] **Set up SSL certificates**
  - Configure Let's Encrypt or hosting provider SSL
  - Set up automatic SSL renewal
  - Force HTTPS redirects for all traffic
  - Test SSL certificate validity and security
  - Configure HSTS headers for security
- [ ] **Create backup and rollback plan**
  - Set up automated content backups
  - Create database backup procedures
  - Document rollback procedures to WordPress
  - Test backup restoration process
  - Set up monitoring for backup failures

**Testing**:
- [ ] Test deployment pipeline with sample changes
- [ ] Verify domain and hosting configuration
- [ ] Test SSL certificate functionality
- [ ] Validate backup and restore procedures
- [ ] Test rollback plan functionality

**Resources**:
- GitHub Actions documentation
- Netlify/Vercel deployment guides
- DNS management documentation
- SSL certificate setup guides
- Backup solution documentation

### 4.2 URL Management
**Main Tasks**: Set up redirects, validate links, and preserve SEO

**Sub-tasks**:
- [ ] **Set up URL redirects**
  - Map all WordPress URLs to Jekyll equivalents
  - Configure 301 redirects for changed URLs
  - Set up redirect rules in hosting configuration
  - Handle category and tag URL changes
  - Redirect WordPress admin and wp-content URLs
- [ ] **Test all internal and external links**
  - Audit all internal links in content
  - Update hard-coded WordPress URLs
  - Test navigation and menu links
  - Validate RSS feed URLs
  - Check image and asset links
- [ ] **Verify SEO metadata preservation**
  - Ensure meta titles and descriptions are preserved
  - Validate Open Graph and Twitter Card tags
  - Set up canonical URLs properly
  - Configure XML sitemap generation
  - Test structured data markup

**Testing**:
- [ ] Test redirect functionality for all old URLs
- [ ] Validate all internal links work correctly
- [ ] Test external link functionality
- [ ] Verify SEO tags with testing tools
- [ ] Check XML sitemap generation and submission

**Resources**:
- Redirect mapping spreadsheet
- SEO testing tools (Google Search Console)
- Link checking tools (Broken Link Checker)
- Structured data testing tools
- XML sitemap generators

### 4.3 Testing and Quality Assurance
**Main Tasks**: Comprehensive testing of migrated site functionality

**Sub-tasks**:
- [ ] **Test all migrated content and functionality**
  - Verify all posts display correctly
  - Test post formatting and images
  - Validate category and tag functionality
  - Test search functionality thoroughly
  - Verify RSS feeds work properly
- [ ] **Verify comment system functionality**
  - Test comment submission process
  - Verify migrated comments display correctly
  - Test comment moderation workflow
  - Validate comment notifications
  - Test spam protection measures
- [ ] **Test responsive design across devices**
  - Test on mobile phones (iOS/Android)
  - Test on tablets (iPad/Android tablets)
  - Test on desktop browsers (Chrome, Firefox, Safari, Edge)
  - Verify touch interactions work properly
  - Test print stylesheets
- [ ] **Validate HTML/CSS/JavaScript**
  - Run HTML validation (W3C Validator)
  - Run CSS validation (W3C CSS Validator)
  - Test JavaScript functionality
  - Check for console errors
  - Validate accessibility (WCAG 2.1 AA)
- [ ] **Performance and optimization testing**
  - Run Lighthouse audits for performance
  - Test Core Web Vitals metrics
  - Validate loading times across different networks
  - Test image optimization and lazy loading
  - Verify CDN functionality

**Testing**:
- [ ] Create comprehensive testing checklist
- [ ] Document all discovered issues
- [ ] Test user workflows end-to-end
- [ ] Validate against original WordPress site
- [ ] Get user acceptance testing from stakeholders

**Resources**:
- W3C HTML/CSS validators
- Browser developer tools
- Device testing labs (BrowserStack)
- Accessibility testing tools (axe, WAVE)
- Performance testing tools (Lighthouse, WebPageTest)
- User testing feedback forms

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

## Timeline Estimate (Revised)

Based on the detailed task breakdown:

- **Phase 1**: 3-4 weeks (Foundation Setup)
  - Jekyll setup and configuration: 1 week
  - Content export and conversion: 1-2 weeks
  - Theme recreation and responsive design: 1-2 weeks
- **Phase 2**: 3-4 weeks (Core Functionality)
  - Site structure and collections: 1 week
  - Dynamic features implementation: 1-2 weeks
  - Comment system setup and migration: 1-2 weeks
- **Phase 3**: 2-3 weeks (Enhancement and Optimization)
  - Cleanup and removal: 1 week
  - Analytics and tracking: 1 week
  - Performance optimization: 1-2 weeks
- **Phase 4**: 2-3 weeks (Deployment and Testing)
  - Deployment setup: 1 week
  - URL management and SEO: 1 week
  - Comprehensive testing and QA: 1-2 weeks

**Total Estimated Time**: 10-14 weeks

### Critical Path Items
1. WordPress content export (blocks other content work)
2. Jekyll site setup (enables theme development)
3. Theme recreation (required for visual testing)
4. Comment system decision (affects migration strategy)
5. Hosting/deployment setup (required for final testing)

### Parallel Work Opportunities
- Theme development can happen alongside content conversion
- Performance optimization can be done while testing
- Analytics setup can happen during deployment phase
- Documentation can be written throughout the process

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

## Quality Assurance and Testing Framework

### Testing Checklist by Phase
- **Phase 1**: Content integrity, Jekyll build process, theme visual fidelity
- **Phase 2**: Navigation functionality, search accuracy, RSS feed validation
- **Phase 3**: Performance benchmarks, error monitoring, cleanup verification
- **Phase 4**: End-to-end user workflows, cross-device compatibility, SEO preservation

### Acceptance Criteria
Each task must meet these criteria before being marked complete:
- **Functionality**: Feature works as intended across all supported browsers
- **Performance**: Meets or exceeds WordPress site performance
- **Visual Fidelity**: Matches original design within acceptable tolerances
- **Content Integrity**: No data loss or corruption during migration
- **SEO Compliance**: Maintains or improves search engine optimization
- **Accessibility**: Meets WCAG 2.1 AA standards

### Testing Tools and Resources
- **Development**: Jekyll, Ruby, Bundler, Git
- **Content Migration**: wordpress-to-jekyll-exporter, custom scripts
- **Design**: Browser developer tools, responsive design testing
- **Performance**: Lighthouse, WebPageTest, GTmetrix
- **SEO**: Google Search Console, SEO testing tools
- **Accessibility**: axe, WAVE, manual testing
- **Cross-browser**: BrowserStack, local device testing

## Project Resources and Tools

### Development Environment
- **Ruby**: Version 3.0+ with rbenv or rvm
- **Jekyll**: Latest stable version
- **Git**: Version control and collaboration
- **Text Editor**: VS Code or similar with Jekyll/Liquid syntax support
- **Package Management**: Bundler for Ruby gems

### Migration Tools
- **Content Export**: WordPress admin export tool, WP-CLI
- **Image Processing**: ImageOptim, TinyPNG for optimization
- **Link Checking**: Broken Link Checker, manual validation
- **Comment Migration**: Custom scripts or third-party services

### Hosting and Deployment
- **Development**: Local Jekyll server
- **Staging**: Netlify, Vercel, or GitHub Pages
- **Production**: Same platform as staging for consistency
- **Domain Management**: DNS provider for blog.mithis.net
- **SSL**: Let's Encrypt or hosting provider certificates

This comprehensive migration plan provides a detailed roadmap for successfully transitioning from WordPress to Jekyll while maintaining content integrity, preserving SEO value, and improving site performance.