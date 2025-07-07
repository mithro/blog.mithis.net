#!/usr/bin/env python3

import os
import re
import yaml
from pathlib import Path

def extract_front_matter(file_path):
    """Extract YAML front matter from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML front matter
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if front_matter_match:
        try:
            return yaml.safe_load(front_matter_match.group(1))
        except yaml.YAMLError:
            return {}
    return {}

def verify_wordpress_url_compatibility():
    """Verify Jekyll permalinks match WordPress URLs"""
    posts_dir = Path('_posts')
    
    print("WordPress URL Compatibility Verification")
    print("=" * 50)
    
    total_posts = 0
    matching_urls = 0
    mismatches = []
    
    for post_file in posts_dir.glob('*.md'):
        front_matter = extract_front_matter(post_file)
        
        if 'wordpress_url' in front_matter and 'permalink' in front_matter:
            total_posts += 1
            
            wp_url = front_matter['wordpress_url']
            jekyll_permalink = front_matter['permalink']
            
            # Extract path from WordPress URL
            wp_path = wp_url.replace('https://blog.mithis.net', '')
            
            # Compare paths
            if wp_path == jekyll_permalink:
                matching_urls += 1
                print(f"✅ {post_file.name}")
                print(f"   URL: {wp_path}")
            else:
                mismatches.append({
                    'file': post_file.name,
                    'wordpress_path': wp_path,
                    'jekyll_permalink': jekyll_permalink
                })
                print(f"❌ {post_file.name}")
                print(f"   WordPress: {wp_path}")
                print(f"   Jekyll:    {jekyll_permalink}")
            print()
    
    print(f"SUMMARY:")
    print(f"Total posts: {total_posts}")
    print(f"Matching URLs: {matching_urls}")
    print(f"Mismatched URLs: {len(mismatches)}")
    
    if len(mismatches) == 0:
        print("\n🎉 SUCCESS: All URLs match perfectly!")
        print("No redirects needed - existing WordPress links will work seamlessly.")
    else:
        print(f"\n⚠️  {len(mismatches)} mismatches found.")
        
    return len(mismatches) == 0

if __name__ == "__main__":
    success = verify_wordpress_url_compatibility()
    exit(0 if success else 1)