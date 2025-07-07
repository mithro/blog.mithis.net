#!/usr/bin/env python3

import os
import re
import yaml
from pathlib import Path

def extract_front_matter(file_path):
    """Extract YAML front matter and content from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML front matter
    front_matter_match = re.match(r'^(---\n.*?\n---\n)(.*)', content, re.DOTALL)
    if front_matter_match:
        front_matter_text = front_matter_match.group(1)
        body_content = front_matter_match.group(2)
        
        # Parse YAML
        yaml_content = front_matter_text[4:-4]  # Remove --- markers
        try:
            front_matter_data = yaml.safe_load(yaml_content)
            return front_matter_data, body_content, front_matter_text
        except yaml.YAMLError:
            return {}, body_content, front_matter_text
    return {}, content, ""

def extract_wordpress_id_and_category(wordpress_url):
    """Extract WordPress ID and category from URL"""
    # Pattern: /archives/category/id-slug
    match = re.search(r'/archives/([^/]+)/(\d+)-', wordpress_url)
    if match:
        category = match.group(1)
        post_id = match.group(2)
        return post_id, category
    return None, None

def update_post_front_matter():
    """Add WordPress IDs and set individual permalinks"""
    posts_dir = Path('_posts')
    
    print("Extracting WordPress IDs and updating permalinks...")
    
    for post_file in posts_dir.glob('*.md'):
        front_matter, body_content, original_fm = extract_front_matter(post_file)
        
        if 'wordpress_url' in front_matter:
            wordpress_url = front_matter['wordpress_url']
            post_id, wp_category = extract_wordpress_id_and_category(wordpress_url)
            
            if post_id and wp_category:
                # Add WordPress ID and category to front matter
                front_matter['wordpress_id'] = int(post_id)
                front_matter['wordpress_category'] = wp_category
                
                # Extract slug from WordPress URL
                slug_match = re.search(r'/\d+-(.+)$', wordpress_url.replace('https://blog.mithis.net', ''))
                if slug_match:
                    slug = slug_match.group(1)
                    # Set individual permalink to match WordPress
                    front_matter['permalink'] = f"/archives/{wp_category}/{post_id}-{slug}"
                
                # Write updated front matter
                new_front_matter = "---\n" + yaml.dump(front_matter, default_flow_style=False, allow_unicode=True) + "---\n"
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_front_matter + body_content)
                
                print(f"✅ Updated {post_file.name}: ID={post_id}, category={wp_category}")
            else:
                print(f"❌ Could not extract ID from {wordpress_url}")
        else:
            print(f"⚠️  No wordpress_url in {post_file.name}")
    
    print("\nDone! All posts updated with WordPress IDs and permalinks.")

if __name__ == "__main__":
    update_post_front_matter()