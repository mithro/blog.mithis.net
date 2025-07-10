#!/usr/bin/env python3
"""
Convert HTML elements in Jekyll posts to pure Markdown.
This script processes WordPress-imported posts to clean up HTML and use proper Markdown syntax.
"""

import os
import re
import glob
from pathlib import Path

def convert_html_to_markdown(content):
    """Convert common HTML elements to Markdown equivalents."""
    
    # Remove wrapper divs that don't add semantic value
    content = re.sub(r'<div[^>]*>\s*', '', content)
    content = re.sub(r'\s*</div>', '', content)
    
    # Convert paragraph tags to double newlines
    content = re.sub(r'<p[^>]*>', '', content)
    content = re.sub(r'</p>', '\n\n', content)
    
    # Convert line breaks
    content = re.sub(r'<br\s*/?>', '\n', content)
    
    # Convert bold and italic
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    
    # Convert links (preserve existing markdown links)
    content = re.sub(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
    
    # Convert unordered lists
    content = re.sub(r'<ul[^>]*>', '', content)
    content = re.sub(r'</ul>', '', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', content, flags=re.DOTALL)
    
    # Convert ordered lists
    content = re.sub(r'<ol[^>]*>', '', content)
    content = re.sub(r'</ol>', '', content)
    # For ordered lists, we'll use a simple counter approach
    ol_counter = 1
    def replace_ol_item(match):
        nonlocal ol_counter
        result = f"{ol_counter}. {match.group(1)}"
        ol_counter += 1
        return result
    
    # Convert headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.DOTALL)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.DOTALL)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content, flags=re.DOTALL)
    content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', content, flags=re.DOTALL)
    content = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', content, flags=re.DOTALL)
    
    # Convert blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1', content, flags=re.DOTALL)
    
    # Convert code elements (inline code)
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
    
    # Convert pre blocks to code fences (this is tricky with syntax highlighting)
    def convert_pre_block(match):
        code_content = match.group(1)
        # Try to detect language from class or other attributes
        pre_tag = match.group(0)
        language = ''
        
        # Look for language hints in class attributes
        lang_match = re.search(r'class="[^"]*(?:language-|lang-)([^"\s]+)', pre_tag)
        if lang_match:
            language = lang_match.group(1)
        elif 'python' in code_content.lower() or 'def ' in code_content or 'import ' in code_content:
            language = 'python'
        elif 'bash' in code_content.lower() or code_content.strip().startswith('$'):
            language = 'bash'
        elif '<' in code_content and '>' in code_content:
            language = 'html'
        
        # Clean up the code content
        code_content = re.sub(r'<[^>]+>', '', code_content)  # Remove any remaining HTML tags
        code_content = code_content.strip()
        
        return f"```{language}\n{code_content}\n```"
    
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', convert_pre_block, content, flags=re.DOTALL)
    
    # Handle span tags with syntax highlighting (common in code blocks)
    # Remove span tags but preserve content
    content = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', content, flags=re.DOTALL)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Multiple newlines to double
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)  # Leading whitespace on lines
    
    # Clean up any remaining HTML entities
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    content = content.replace('&quot;', '"')
    content = content.replace('&#8216;', "'")
    content = content.replace('&#8217;', "'")
    content = content.replace('&#8220;', '"')
    content = content.replace('&#8221;', '"')
    content = content.replace('&#8211;', '–')
    content = content.replace('&#8212;', '—')
    
    return content

def process_post_file(filepath):
    """Process a single post file to convert HTML to Markdown."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter from content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        front_matter = parts[1]
        post_content = parts[2]
        
        # Convert HTML in post content
        converted_content = convert_html_to_markdown(post_content)
        
        # Reassemble the file
        new_content = f"---{front_matter}---{converted_content}"
        
        # Only write if content changed
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Converted HTML to Markdown")
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
    
    print(f"\nCompleted! Converted {converted_count} out of {len(post_files)} files.")

if __name__ == '__main__':
    main()