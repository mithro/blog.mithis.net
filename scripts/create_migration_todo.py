#!/usr/bin/env python3

import json
import os
from pathlib import Path
from datetime import datetime
import re

def load_all_wordpress_posts():
    """Load all WordPress posts from sitemap data and known missing posts"""
    posts = []
    
    # Load posts from sitemap
    try:
        with open('exports/all_post_urls.json', 'r') as f:
            posts.extend(json.load(f))
    except FileNotFoundError:
        print("❌ all_post_urls.json not found - need to run sitemap scraper first")
    
    # Load known missing posts
    try:
        with open('exports/missing_post.json', 'r') as f:
            missing_posts = json.load(f)
            for post in missing_posts:
                posts.append({
                    'url': post['url'],
                    'lastmod': post['lastmod']
                })
    except FileNotFoundError:
        print("⚠️  missing_post.json not found - using sitemap data only")
    
    return posts

def get_migrated_posts():
    """Get list of already migrated posts"""
    migrated = {}
    posts_dir = Path('_posts')
    
    if not posts_dir.exists():
        return migrated
    
    for post_file in posts_dir.glob('*.md'):
        # Extract front matter to get WordPress URL
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for wordpress_url in front matter (with or without quotes)
        url_match = re.search(r'wordpress_url:\s*["\']?([^"\'\n]+)["\']?', content)
        if url_match:
            wp_url = url_match.group(1).strip()
            migrated[wp_url] = {
                'file': post_file.name,
                'status': 'migrated'
            }
    
    return migrated

def extract_post_info(url):
    """Extract post information from WordPress URL"""
    # Pattern: https://blog.mithis.net/archives/category/id-title
    # Handle both single category and nested categories (e.g., rcs/darcs)
    match = re.search(r'/archives/(.+)/(\d+)-(.+)$', url)
    if match:
        category_path = match.group(1)
        post_id = match.group(2)
        slug = match.group(3)
        
        # For nested categories, use the full path but with dashes
        category = category_path.replace('/', '-')
        
        return {
            'category': category,
            'category_path': category_path,
            'id': int(post_id),
            'slug': slug
        }
    return None

def create_migration_todo():
    """Create comprehensive migration TODO list"""
    print("Creating Migration TODO List...")
    print("=" * 50)
    
    # Load all WordPress posts
    all_posts = load_all_wordpress_posts()
    if not all_posts:
        print("No WordPress posts found to migrate")
        return
    
    # Get migrated posts
    migrated_posts = get_migrated_posts()
    
    # Analyze migration status
    migration_status = []
    categories = {}
    
    for post_data in all_posts:
        url = post_data['url']
        lastmod = post_data.get('lastmod', '')
        
        post_info = extract_post_info(url)
        if not post_info:
            continue
        
        category = post_info['category']
        if category not in categories:
            categories[category] = {'total': 0, 'migrated': 0, 'pending': 0}
        categories[category]['total'] += 1
        
        if url in migrated_posts:
            status = 'migrated'
            categories[category]['migrated'] += 1
            file_name = migrated_posts[url]['file']
        else:
            status = 'pending'
            categories[category]['pending'] += 1
            file_name = f"MISSING: {post_info['id']}-{post_info['slug']}.md"
        
        migration_status.append({
            'url': url,
            'category': category,
            'id': post_info['id'],
            'slug': post_info['slug'],
            'lastmod': lastmod,
            'status': status,
            'file': file_name
        })
    
    # Sort by ID for chronological order
    migration_status.sort(key=lambda x: x['id'])
    
    # Generate markdown report
    report = f"""# WordPress to Jekyll Migration TODO List

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

**Total Posts Found**: {len(migration_status)}
**Posts Migrated**: {len(migrated_posts)}
**Posts Pending**: {len(migration_status) - len(migrated_posts)}
**Migration Progress**: {len(migrated_posts)}/{len(migration_status)} ({len(migrated_posts)/len(migration_status)*100:.1f}%)

## Category Breakdown

| Category | Total | Migrated | Pending | Progress |
|----------|-------|----------|---------|----------|
"""
    
    for category, stats in sorted(categories.items()):
        progress = stats['migrated'] / stats['total'] * 100 if stats['total'] > 0 else 0
        report += f"| {category} | {stats['total']} | {stats['migrated']} | {stats['pending']} | {progress:.1f}% |\n"
    
    report += """
## Detailed Post Status

### Legend
- ✅ **Migrated**: Post successfully converted to Jekyll
- ❌ **Pending**: Post needs to be extracted and converted

### Posts by ID (Chronological Order)

"""
    
    for post in migration_status:
        status_icon = "✅" if post['status'] == 'migrated' else "❌"
        date_str = post['lastmod'][:10] if post['lastmod'] else "Unknown"
        
        report += f"**{status_icon} Post {post['id']}** (`{post['category']}`)\n"
        report += f"- **URL**: {post['url']}\n"
        report += f"- **Date**: {date_str}\n"
        report += f"- **File**: `{post['file']}`\n"
        report += f"- **Status**: {post['status'].title()}\n\n"
    
    report += """
## Next Steps

### For Pending Posts:
1. Run the full site scraper to extract remaining posts
2. Convert HTML content to Jekyll markdown format  
3. Extract and preserve metadata (categories, tags, dates)
4. Set WordPress-compatible permalinks
5. Test all extracted posts

### Extraction Priority:
- Focus on posts with higher IDs (more recent content)
- Ensure all categories are represented
- Verify content quality and formatting

### Commands to Extract Remaining Posts:
```bash
# Run the full site scraper with timeout handling
python3 exports/scripts/full_site_scraper.py

# Check extraction progress
ls -1 _posts/ | wc -l

# Verify URL compatibility
python3 scripts/verify_wordpress_urls.py
```
"""
    
    # Save report
    with open('MIGRATION_TODO.md', 'w') as f:
        f.write(report)
    
    # Also save machine-readable JSON
    with open('migration_status.json', 'w') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_posts': len(migration_status),
                'migrated': len(migrated_posts),
                'pending': len(migration_status) - len(migrated_posts),
                'progress_percent': len(migrated_posts)/len(migration_status)*100
            },
            'categories': categories,
            'posts': migration_status
        }, f, indent=2)
    
    print(f"📊 Migration TODO List Created!")
    print(f"   - Markdown report: MIGRATION_TODO.md")
    print(f"   - JSON data: migration_status.json")
    print(f"   - Found {len(migration_status)} total posts (verified count: {len(all_posts)})")
    print(f"   - {len(migrated_posts)} migrated, {len(migration_status) - len(migrated_posts)} pending")
    print(f"   - {len(migrated_posts)/len(migration_status)*100:.1f}% complete")

if __name__ == "__main__":
    create_migration_todo()