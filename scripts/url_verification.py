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

def analyze_url_patterns():
    """Analyze WordPress URLs vs Jekyll URLs"""
    posts_dir = Path('_posts')
    
    print("URL Pattern Analysis")
    print("=" * 50)
    
    wordpress_patterns = []
    jekyll_urls = []
    mismatches = []
    
    for post_file in posts_dir.glob('*.md'):
        front_matter = extract_front_matter(post_file)
        
        if 'wordpress_url' in front_matter:
            wp_url = front_matter['wordpress_url']
            
            # Extract expected Jekyll URL from filename and date
            filename = post_file.stem
            date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.*)', filename)
            
            if date_match:
                year, month, day, slug = date_match.groups()
                jekyll_url = f"/{year}/{month}/{slug}/"
                
                wordpress_patterns.append(wp_url)
                jekyll_urls.append(jekyll_url)
                
                # Check if they match
                wp_path = wp_url.replace('https://blog.mithis.net', '')
                if wp_path != jekyll_url:
                    mismatches.append({
                        'file': post_file.name,
                        'wordpress': wp_url,
                        'jekyll': f"https://blog.mithis.net{jekyll_url}",
                        'wp_path': wp_path,
                        'jekyll_path': jekyll_url
                    })
    
    print(f"Total posts analyzed: {len(wordpress_patterns)}")
    print(f"URL mismatches found: {len(mismatches)}")
    print()
    
    if mismatches:
        print("MISMATCHED URLs:")
        print("-" * 50)
        for i, mismatch in enumerate(mismatches[:10]):  # Show first 10
            print(f"{i+1}. {mismatch['file']}")
            print(f"   WordPress: {mismatch['wp_path']}")
            print(f"   Jekyll:    {mismatch['jekyll_path']}")
            print()
        
        if len(mismatches) > 10:
            print(f"... and {len(mismatches) - 10} more mismatches")
    
    return mismatches

def generate_redirect_rules(mismatches):
    """Generate redirect rules for Apache/Nginx"""
    
    print("\nApache .htaccess redirect rules:")
    print("-" * 40)
    for mismatch in mismatches:
        wp_path = mismatch['wp_path']
        jekyll_path = mismatch['jekyll_path']
        print(f"Redirect 301 {wp_path} {jekyll_path}")
    
    print("\nNginx redirect rules:")
    print("-" * 40)
    for mismatch in mismatches:
        wp_path = mismatch['wp_path']
        jekyll_path = mismatch['jekyll_path']
        print(f"rewrite ^{re.escape(wp_path)}$ {jekyll_path} permanent;")

if __name__ == "__main__":
    mismatches = analyze_url_patterns()
    if mismatches:
        generate_redirect_rules(mismatches)
    else:
        print("✅ All URLs match! No redirects needed.")