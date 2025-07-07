#!/usr/bin/env python3
"""
RSS-based WordPress content extraction script for blog.mithis.net
Fallback method when admin export is not available
"""

import feedparser
import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import os

class WordPressRSSExtractor:
    def __init__(self, site_url, output_dir):
        self.site_url = site_url.rstrip('/')
        self.output_dir = output_dir
        self.posts = []
        
    def extract_from_rss(self, rss_url=None):
        """Extract posts from RSS feed"""
        if not rss_url:
            rss_url = f"{self.site_url}/feed/"
            
        print(f"Fetching RSS feed: {rss_url}")
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            print("No entries found in RSS feed")
            return []
            
        print(f"Found {len(feed.entries)} posts in RSS feed")
        
        for entry in feed.entries:
            post = self.extract_post_data(entry)
            self.posts.append(post)
            
        return self.posts
    
    def extract_post_data(self, entry):
        """Extract structured data from RSS entry"""
        # Parse publication date
        pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
        
        # Extract categories and tags
        categories = []
        tags = []
        
        if hasattr(entry, 'tags'):
            for tag in entry.tags:
                if tag.scheme:
                    categories.append(tag.term)
                else:
                    tags.append(tag.term)
        
        # Clean content
        content = self.clean_html_content(entry.content[0].value if entry.content else entry.summary)
        
        # Extract excerpt
        excerpt = self.extract_excerpt(content)
        
        # Generate slug from title
        slug = self.generate_slug(entry.title)
        
        post_data = {
            'title': entry.title,
            'slug': slug,
            'url': entry.link,
            'date': pub_date,
            'content': content,
            'excerpt': excerpt,
            'categories': categories,
            'tags': tags,
            'author': getattr(entry, 'author', 'mithro'),
            'guid': getattr(entry, 'id', entry.link)
        }
        
        return post_data
    
    def clean_html_content(self, html_content):
        """Clean HTML content for Jekyll conversion"""
        # Remove WordPress-specific elements
        content = re.sub(r'<p>(&nbsp;|\s)*</p>', '', html_content)
        content = re.sub(r'<div[^>]*class="[^"]*wp-[^"]*"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        
        # Clean up common HTML issues
        content = content.replace('&nbsp;', ' ')
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content
    
    def extract_excerpt(self, content, max_length=160):
        """Extract excerpt from content"""
        # Remove HTML tags for excerpt
        text = re.sub(r'<[^>]+>', '', content)
        text = text.strip()
        
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'
            
        return text
    
    def generate_slug(self, title):
        """Generate URL slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def save_posts_json(self):
        """Save extracted posts as JSON for processing"""
        output_file = os.path.join(self.output_dir, 'rss_posts.json')
        
        # Convert datetime objects to strings for JSON serialization
        posts_json = []
        for post in self.posts:
            post_copy = post.copy()
            post_copy['date'] = post['date'].isoformat()
            posts_json.append(post_copy)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts_json, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(posts_json)} posts to {output_file}")
    
    def save_jekyll_posts(self):
        """Convert and save posts as Jekyll markdown files"""
        posts_dir = os.path.join(self.output_dir, '_posts')
        os.makedirs(posts_dir, exist_ok=True)
        
        for post in self.posts:
            filename = f"{post['date'].strftime('%Y-%m-%d')}-{post['slug']}.md"
            filepath = os.path.join(posts_dir, filename)
            
            front_matter = {
                'layout': 'post',
                'title': post['title'],
                'date': post['date'].strftime('%Y-%m-%d %H:%M:%S %z'),
                'categories': post['categories'],
                'tags': post['tags'],
                'author': post['author'],
                'excerpt': post['excerpt'],
                'wordpress_url': post['url']
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('---\n')
                for key, value in front_matter.items():
                    if isinstance(value, list):
                        f.write(f'{key}: {value}\n')
                    else:
                        f.write(f'{key}: "{value}"\n')
                f.write('---\n\n')
                f.write(post['content'])
                
        print(f"Saved {len(self.posts)} Jekyll posts to {posts_dir}")
    
    def download_media(self):
        """Download media files referenced in posts"""
        media_dir = os.path.join(self.output_dir, 'media')
        os.makedirs(media_dir, exist_ok=True)
        
        image_urls = set()
        
        # Extract image URLs from all posts
        for post in self.posts:
            img_matches = re.findall(r'<img[^>]+src="([^"]+)"', post['content'])
            for img_url in img_matches:
                if img_url.startswith(self.site_url):
                    image_urls.add(img_url)
        
        print(f"Found {len(image_urls)} unique images to download")
        
        # Download images (implement based on need)
        for img_url in image_urls:
            print(f"Would download: {img_url}")
            # TODO: Implement actual download logic
    
    def run_extraction(self):
        """Run complete extraction process"""
        print(f"Starting WordPress content extraction from {self.site_url}")
        
        # Extract from RSS
        self.extract_from_rss()
        
        # Save in multiple formats
        self.save_posts_json()
        self.save_jekyll_posts()
        
        # Download media
        self.download_media()
        
        print(f"Extraction complete. Found {len(self.posts)} posts.")
        return self.posts

if __name__ == "__main__":
    extractor = WordPressRSSExtractor("https://blog.mithis.net", "exports")
    posts = extractor.run_extraction()
    
    print("\nExtraction Summary:")
    print(f"- Total posts: {len(posts)}")
    if posts:
        print(f"- Date range: {min(p['date'] for p in posts)} to {max(p['date'] for p in posts)}")
        print(f"- Categories: {set(cat for p in posts for cat in p['categories'])}")
        print(f"- Authors: {set(p['author'] for p in posts)}")