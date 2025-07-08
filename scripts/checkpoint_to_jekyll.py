#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path
from datetime import datetime
import html

def clean_content(content):
    """Clean HTML content for Jekyll conversion"""
    if not content:
        return ""
    
    # Unescape HTML entities
    content = html.unescape(content)
    
    # Basic HTML cleanup while preserving structure
    # Remove WordPress-specific classes and attributes
    content = re.sub(r'class="[^"]*"', '', content)
    content = re.sub(r'id="[^"]*"', '', content)
    content = re.sub(r'style="[^"]*"', '', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s+\n', '\n\n', content)
    content = re.sub(r'>\s+<', '><', content)
    
    return content.strip()

def extract_wordpress_metadata(url, content):
    """Extract WordPress ID and category from URL and content"""
    # Extract from URL: /archives/category/id-title
    match = re.search(r'/archives/(.+)/(\d+)-(.+)$', url)
    if match:
        category_path = match.group(1)
        post_id = match.group(2)
        slug = match.group(3)
        
        # Handle nested categories
        category = category_path.replace('/', '-')
        
        return {
            'wordpress_id': int(post_id),
            'wordpress_category': category,
            'slug': slug,
            'permalink': url.replace('https://blog.mithis.net', '')
        }
    return {}

def create_jekyll_filename(date_str, slug):
    """Create Jekyll filename from date and slug"""
    try:
        # Parse date
        if 'T' in date_str:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
        
        # Format as YYYY-MM-DD-slug.md
        date_part = date_obj.strftime('%Y-%m-%d')
        return f"{date_part}-{slug}.md"
    except:
        # Fallback
        return f"unknown-date-{slug}.md"

def convert_post_to_jekyll(post_data):
    """Convert scraped post data to Jekyll front matter and content"""
    
    # Extract metadata
    url = post_data.get('url', '')
    title = post_data.get('title', 'Untitled').strip()
    content = post_data.get('content', '')
    date_str = post_data.get('date', post_data.get('published', ''))
    excerpt = post_data.get('excerpt', '')
    categories = post_data.get('categories', [])
    
    wp_metadata = extract_wordpress_metadata(url, content)
    
    # Clean content
    clean_content_text = clean_content(content)
    
    # Prepare front matter
    front_matter = {
        'layout': 'post',
        'title': title,
        'date': date_str,
        'categories': categories if categories else [wp_metadata.get('wordpress_category', 'uncategorized')],
        'author': 'mithro',
        'excerpt': excerpt[:200] + '...' if len(excerpt) > 200 else excerpt
    }
    
    # Add WordPress metadata
    if wp_metadata:
        front_matter.update({
            'wordpress_id': wp_metadata['wordpress_id'],
            'wordpress_category': wp_metadata['wordpress_category'],
            'wordpress_url': url,
            'permalink': wp_metadata['permalink']
        })
    
    # Create filename
    filename = create_jekyll_filename(date_str, wp_metadata.get('slug', 'unknown'))
    
    return filename, front_matter, clean_content_text

def convert_checkpoint_to_posts(checkpoint_file):
    """Convert checkpoint JSON to Jekyll posts"""
    
    if not os.path.exists(checkpoint_file):
        print(f"❌ Checkpoint file {checkpoint_file} not found")
        return
    
    # Load checkpoint data
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"Converting {len(posts_data)} posts from {checkpoint_file}")
    
    # Ensure _posts directory exists
    posts_dir = Path('_posts')
    posts_dir.mkdir(exist_ok=True)
    
    # Get existing post files
    existing_files = set(f.name for f in posts_dir.glob('*.md'))
    
    converted = 0
    skipped = 0
    
    for post_data in posts_data:
        try:
            filename, front_matter, content = convert_post_to_jekyll(post_data)
            
            # Skip if file already exists
            if filename in existing_files:
                skipped += 1
                continue
            
            # Write Jekyll post
            file_path = posts_dir / filename
            
            # Format front matter as YAML
            import yaml
            front_matter_yaml = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('---\n')
                f.write(front_matter_yaml)
                f.write('---\n\n')
                f.write(content)
            
            print(f"✅ Created: {filename}")
            converted += 1
            
        except Exception as e:
            print(f"❌ Error converting post: {e}")
    
    print(f"\n📊 Conversion Summary:")
    print(f"   - Posts converted: {converted}")
    print(f"   - Posts skipped (already exist): {skipped}")
    print(f"   - Total posts in checkpoint: {len(posts_data)}")

if __name__ == "__main__":
    import sys
    
    # Find latest checkpoint or use specified one
    if len(sys.argv) > 1:
        checkpoint_file = sys.argv[1]
    else:
        # Find latest checkpoint
        checkpoints = [f for f in os.listdir('.') if f.startswith('checkpoint_') and f.endswith('.json')]
        if checkpoints:
            # Sort by number
            checkpoints.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
            checkpoint_file = checkpoints[-1]
            print(f"Using latest checkpoint: {checkpoint_file}")
        else:
            print("❌ No checkpoint files found")
            sys.exit(1)
    
    convert_checkpoint_to_posts(checkpoint_file)