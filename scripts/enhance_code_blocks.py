#!/usr/bin/env python3
"""
Enhance code blocks in migrated WordPress posts
Converts HTML code blocks to Jekyll/Rouge-compatible markdown
"""

import os
import re
import glob
from bs4 import BeautifulSoup

def detect_language(code_content):
    """Detect programming language from code content"""
    code_lower = code_content.lower().strip()
    
    # Shell/Bash detection
    if (code_lower.startswith('#!/bin/bash') or 
        code_lower.startswith('#!/bin/sh') or
        'ssh-add' in code_lower or
        'export ' in code_lower or
        'echo ' in code_lower and '$' in code_lower):
        return 'bash'
    
    # Python detection
    if (code_lower.startswith('#!/usr/bin/env python') or
        'import ' in code_lower or
        'def ' in code_lower or
        'class ' in code_lower):
        return 'python'
    
    # Config file detection
    if ('=' in code_lower and 
        ('\n' in code_lower or len(code_lower.split()) > 2)):
        if 'identitiesonly' in code_lower or 'identityfile' in code_lower:
            return 'config'
        return 'ini'
    
    # C/C++ detection
    if ('#include' in code_lower or
        'int main(' in code_lower or
        'printf(' in code_lower):
        return 'c'
    
    # Debug/log output
    if ('debug' in code_lower or
        'error:' in code_lower or
        'warning:' in code_lower):
        return 'text'
    
    # Default to text for short snippets or unknown content
    return 'text' if len(code_lower) < 50 else 'bash'

def clean_code_content(html_content):
    """Clean HTML entities and formatting from code content"""
    # Decode HTML entities
    content = html_content.replace('&gt;', '>')
    content = content.replace('&lt;', '<')
    content = content.replace('&amp;', '&')
    content = content.replace('&nbsp;', ' ')
    content = content.replace('<br/>', '\n')
    content = content.replace('<br>', '\n')
    
    # Remove any remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    content = content.strip()
    
    return content

def enhance_post_code_blocks(file_path):
    """Enhance code blocks in a single post file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  Skipping - no front matter found")
        return False
    
    front_matter = parts[1]
    post_content = parts[2]
    
    # Track changes
    changes_made = False
    
    # Pattern 1: <blockquote><pre><code>...</code></pre></blockquote>
    pattern1 = r'<blockquote>\s*<pre><code>(.*?)</code></pre>\s*</blockquote>'
    def replace_pattern1(match):
        nonlocal changes_made
        code_content = clean_code_content(match.group(1))
        if code_content:
            language = detect_language(code_content)
            changes_made = True
            return f'\n```{language}\n{code_content}\n```\n'
        return match.group(0)
    
    post_content = re.sub(pattern1, replace_pattern1, post_content, flags=re.DOTALL)
    
    # Pattern 2: Inline code in blockquotes
    pattern2 = r'<blockquote><p><code>(.*?)</code>\s*</p></blockquote>'
    def replace_pattern2(match):
        nonlocal changes_made
        code_content = clean_code_content(match.group(1))
        if code_content and len(code_content) > 10:  # Only for substantial code blocks
            language = detect_language(code_content)
            changes_made = True
            return f'\n```{language}\n{code_content}\n```\n'
        else:
            # Keep as inline code
            changes_made = True
            return f'\n`{code_content}`\n'
    
    post_content = re.sub(pattern2, replace_pattern2, post_content, flags=re.DOTALL)
    
    # Pattern 3: Multi-line code in paragraph blocks
    pattern3 = r'<p><code>(.*?)</code></p>'
    def replace_pattern3(match):
        nonlocal changes_made
        code_content = clean_code_content(match.group(1))
        if '\n' in code_content or len(code_content) > 50:
            language = detect_language(code_content)
            changes_made = True
            return f'\n```{language}\n{code_content}\n```\n'
        return match.group(0)  # Keep as-is for short inline code
    
    post_content = re.sub(pattern3, replace_pattern3, post_content, flags=re.DOTALL)
    
    if changes_made:
        # Write back the enhanced content
        enhanced_content = f"---{front_matter}---{post_content}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        print(f"  ✅ Enhanced code blocks")
        return True
    else:
        print(f"  ℹ️  No code blocks found to enhance")
        return False

def main():
    """Main function to process all posts"""
    posts_dir = "_posts"
    if not os.path.exists(posts_dir):
        print(f"Error: {posts_dir} directory not found")
        return
    
    post_files = glob.glob(os.path.join(posts_dir, "*.md"))
    print(f"Found {len(post_files)} post files to process")
    
    enhanced_count = 0
    for post_file in post_files:
        if enhance_post_code_blocks(post_file):
            enhanced_count += 1
    
    print(f"\nSummary:")
    print(f"- Total posts processed: {len(post_files)}")
    print(f"- Posts with enhanced code blocks: {enhanced_count}")
    print(f"- Posts unchanged: {len(post_files) - enhanced_count}")

if __name__ == "__main__":
    main()