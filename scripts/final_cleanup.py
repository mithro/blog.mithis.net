#!/usr/bin/env python3
"""
Final cleanup script to handle remaining HTML issues in converted posts.
"""

import os
import re
from pathlib import Path

def final_html_cleanup(content):
    """Final cleanup of remaining HTML elements."""
    
    # Fix table-based code blocks that weren't caught before
    def fix_table_code(match):
        table_content = match.group(1)
        # Remove all HTML tags and extract just the text content
        clean_content = re.sub(r'<[^>]+>', '', table_content)
        # Clean up whitespace
        clean_content = re.sub(r'\n\s*\n', '\n', clean_content)
        clean_content = clean_content.strip()
        
        # If it looks like code, wrap it in code fences
        if clean_content and (
            'def ' in clean_content or 
            'import ' in clean_content or 
            '#!' in clean_content or
            'function' in clean_content or
            clean_content.count('\n') > 3
        ):
            # Try to detect language
            language = ''
            if 'python' in clean_content.lower() or 'def ' in clean_content or 'import ' in clean_content:
                language = 'python'
            elif 'bash' in clean_content.lower() or clean_content.strip().startswith('#!'):
                language = 'bash'
            elif 'function' in clean_content or 'var ' in clean_content:
                language = 'javascript'
            
            return f"```{language}\n{clean_content}\n```"
        else:
            return clean_content
    
    # Fix remaining table elements
    content = re.sub(r'<table[^>]*>(.*?)</table>', fix_table_code, content, flags=re.DOTALL)
    
    # Remove any remaining HTML table elements
    content = re.sub(r'</?table[^>]*>', '', content)
    content = re.sub(r'</?tr[^>]*>', '', content)
    content = re.sub(r'</?td[^>]*>', '', content)
    content = re.sub(r'</?th[^>]*>', '', content)
    
    # Remove span elements but preserve content
    content = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', content, flags=re.DOTALL)
    
    # Clean up blockquotes that might have extra content
    content = re.sub(r'>\s*\n\s*<', '> ', content)
    
    # Fix any remaining HTML entities
    html_entities = {
        '&#8216;': "'",
        '&#8217;': "'", 
        '&#8220;': '"',
        '&#8221;': '"',
        '&#8211;': '–',
        '&#8212;': '—',
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&nbsp;': ' '
    }
    
    for entity, replacement in html_entities.items():
        content = content.replace(entity, replacement)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)
    
    return content

def process_post_file(filepath):
    """Process a single post file for final cleanup."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Split front matter from content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        front_matter = parts[1]
        post_content = parts[2]
        
        # Apply final cleanup
        cleaned_content = final_html_cleanup(post_content)
        
        # Ensure proper spacing after front matter
        if not cleaned_content.startswith('\n'):
            cleaned_content = '\n' + cleaned_content
        
        # Reassemble the file
        new_content = f"---{front_matter}---{cleaned_content}"
        
        # Only write if content changed
        if new_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Applied final cleanup")
            return True
        else:
            print(f"  - No changes needed")
            return False
    else:
        print(f"  ✗ Could not parse front matter")
        return False

def main():
    """Main function to process all posts."""
    posts_dir = Path('_posts')
    
    if not posts_dir.exists():
        print("Error: _posts directory not found. Run this script from the Jekyll root directory.")
        return
    
    # Get all markdown files in _posts
    post_files = list(posts_dir.glob('*.md'))
    
    print(f"Found {len(post_files)} post files to process...")
    
    converted_count = 0
    for post_file in post_files:
        if process_post_file(post_file):
            converted_count += 1
    
    print(f"\nCompleted! Cleaned up {converted_count} out of {len(post_files)} files.")

if __name__ == '__main__':
    main()