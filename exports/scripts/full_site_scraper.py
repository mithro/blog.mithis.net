#!/usr/bin/env python3
"""
Complete WordPress blog scraper for blog.mithis.net
Extracts all posts from sitemap index and individual post pages
"""

import requests
import xml.etree.ElementTree as ET
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime
import html
from bs4 import BeautifulSoup

class WordPressBlogScraper:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.posts = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BlogMigrationBot/1.0)'
        })
        
    def download_sitemap_index(self):
        """Download and parse the main sitemap index"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        print(f"Downloading sitemap index: {sitemap_url}")
        
        try:
            response = self.session.get(sitemap_url)
            response.raise_for_status()
            
            # Save raw sitemap
            with open(os.path.join(self.output_dir, 'sitemap_index.xml'), 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Parse XML
            root = ET.fromstring(response.content)
            sitemap_urls = []
            
            # Find all sitemap URLs for posts
            for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None and 'sitemap-pt-post' in loc.text:
                    sitemap_urls.append(loc.text)
            
            print(f"Found {len(sitemap_urls)} post sitemaps")
            return sitemap_urls
            
        except Exception as e:
            print(f"Error downloading sitemap index: {e}")
            return []
    
    def download_individual_sitemaps(self, sitemap_urls):
        """Download individual sitemap files and extract post URLs"""
        all_post_urls = []
        
        for sitemap_url in sitemap_urls:
            print(f"Processing sitemap: {sitemap_url}")
            
            try:
                response = self.session.get(sitemap_url)
                response.raise_for_status()
                
                # Save individual sitemap
                filename = sitemap_url.split('/')[-1]
                with open(os.path.join(self.output_dir, f'xml/sitemaps/{filename}'), 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Parse XML
                root = ET.fromstring(response.content)
                
                # Extract post URLs
                for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                    loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    lastmod = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
                    
                    if loc is not None:
                        post_url = loc.text
                        last_modified = lastmod.text if lastmod is not None else None
                        all_post_urls.append({
                            'url': post_url,
                            'lastmod': last_modified
                        })
                
                # Small delay to be polite
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error processing {sitemap_url}: {e}")
                continue
        
        print(f"Found {len(all_post_urls)} total post URLs")
        return all_post_urls
    
    def scrape_post_content(self, post_url):
        """Scrape individual post content from WordPress"""
        try:
            print(f"Scraping: {post_url}")
            response = self.session.get(post_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract post data
            post_data = {
                'url': post_url,
                'title': None,
                'content': None,
                'date': None,
                'categories': [],
                'tags': [],
                'author': 'mithro',
                'excerpt': None
            }
            
            # Extract title
            title_elem = soup.find('h2', class_='entry-title') or soup.find('h1', class_='entry-title')
            if title_elem:
                post_data['title'] = title_elem.get_text().strip()
            
            # Extract content
            content_elem = soup.find('div', class_='entry-content')
            if content_elem:
                # Remove WordPress-specific elements
                for elem in content_elem.find_all(['script', 'style']):
                    elem.decompose()
                post_data['content'] = str(content_elem)
            
            # Extract date
            date_elem = soup.find('abbr', class_='published') or soup.find('time', class_='published')
            if date_elem:
                date_str = date_elem.get('title') or date_elem.get('datetime') or date_elem.get_text()
                try:
                    # Try various date formats
                    for fmt in ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S %z']:
                        try:
                            post_data['date'] = datetime.strptime(date_str.strip(), fmt)
                            break
                        except ValueError:
                            continue
                except:
                    pass
            
            # Extract categories from URL or meta
            url_parts = post_url.split('/')
            if 'archives' in url_parts:
                try:
                    category_index = url_parts.index('archives') + 1
                    if category_index < len(url_parts):
                        category = url_parts[category_index].replace('-', ' ').title()
                        post_data['categories'] = [category]
                except:
                    pass
            
            # Extract categories from breadcrumbs or meta
            cat_links = soup.find_all('a', href=re.compile(r'/archives/[^/]+/?$'))
            for link in cat_links:
                category = link.get_text().strip()
                if category and category not in post_data['categories']:
                    post_data['categories'].append(category)
            
            # Generate excerpt
            if post_data['content']:
                text_content = BeautifulSoup(post_data['content'], 'html.parser').get_text()
                words = text_content.split()
                if len(words) > 30:
                    post_data['excerpt'] = ' '.join(words[:30]) + '...'
                else:
                    post_data['excerpt'] = text_content
            
            # Generate slug from URL
            url_parts = post_url.rstrip('/').split('/')
            slug_part = url_parts[-1]
            # Remove numeric ID prefix if present
            slug_match = re.search(r'(\d+-)?(.*)', slug_part)
            if slug_match:
                post_data['slug'] = slug_match.group(2) or slug_part
            else:
                post_data['slug'] = slug_part
            
            return post_data
            
        except Exception as e:
            print(f"Error scraping {post_url}: {e}")
            return None
    
    def scrape_all_posts(self, post_urls, max_posts=None):
        """Scrape all posts with optional limit for testing"""
        scraped_posts = []
        
        # Limit for testing if specified
        if max_posts:
            post_urls = post_urls[:max_posts]
            print(f"Limiting to {max_posts} posts for testing")
        
        for i, post_info in enumerate(post_urls, 1):
            post_url = post_info['url']
            
            print(f"[{i}/{len(post_urls)}] Processing: {post_url}")
            
            post_data = self.scrape_post_content(post_url)
            if post_data:
                scraped_posts.append(post_data)
            
            # Polite delay
            time.sleep(1)
            
            # Progress checkpoint every 10 posts
            if i % 10 == 0:
                self.save_checkpoint(scraped_posts, f"checkpoint_{i}")
        
        return scraped_posts
    
    def save_checkpoint(self, posts, filename):
        """Save progress checkpoint"""
        checkpoint_file = os.path.join(self.output_dir, f'{filename}.json')
        posts_json = []
        for post in posts:
            post_copy = post.copy()
            if post_copy.get('date'):
                post_copy['date'] = post_copy['date'].isoformat()
            posts_json.append(post_copy)
        
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(posts_json, f, indent=2, ensure_ascii=False)
        print(f"Checkpoint saved: {checkpoint_file}")
    
    def save_jekyll_posts(self, posts):
        """Convert and save posts as Jekyll markdown files"""
        posts_dir = os.path.join(self.output_dir, '_posts_scraped')
        os.makedirs(posts_dir, exist_ok=True)
        
        for post in posts:
            if not post.get('title') or not post.get('date'):
                continue
                
            # Generate filename
            date_str = post['date'].strftime('%Y-%m-%d')
            slug = post.get('slug', 'untitled')
            slug = re.sub(r'[^a-zA-Z0-9\-]', '-', slug).strip('-')
            filename = f"{date_str}-{slug}.md"
            filepath = os.path.join(posts_dir, filename)
            
            # Prepare front matter
            front_matter = {
                'layout': 'post',
                'title': post['title'],
                'date': post['date'].strftime('%Y-%m-%d %H:%M:%S %z'),
                'categories': post.get('categories', []),
                'tags': post.get('tags', []),
                'author': post.get('author', 'mithro'),
                'excerpt': post.get('excerpt', ''),
                'wordpress_url': post['url']
            }
            
            # Write Jekyll post
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('---\n')
                for key, value in front_matter.items():
                    if isinstance(value, list):
                        if value:
                            f.write(f'{key}:\n')
                            for item in value:
                                f.write(f'  - {item}\n')
                    else:
                        f.write(f'{key}: "{value}"\n')
                f.write('---\n\n')
                f.write(post.get('content', ''))
        
        print(f"Saved {len(posts)} Jekyll posts to {posts_dir}")
    
    def run_full_extraction(self, max_posts=None):
        """Run complete site extraction"""
        print(f"Starting full WordPress site extraction from {self.base_url}")
        
        # Create output directories
        os.makedirs(os.path.join(self.output_dir, 'xml/sitemaps'), exist_ok=True)
        
        # Download sitemap index
        sitemap_urls = self.download_sitemap_index()
        if not sitemap_urls:
            print("No sitemaps found. Exiting.")
            return []
        
        # Download individual sitemaps and extract post URLs
        post_urls = self.download_individual_sitemaps(sitemap_urls)
        if not post_urls:
            print("No post URLs found. Exiting.")
            return []
        
        # Save post URLs list
        with open(os.path.join(self.output_dir, 'all_post_urls.json'), 'w', encoding='utf-8') as f:
            json.dump(post_urls, f, indent=2, ensure_ascii=False)
        
        # Scrape all posts
        scraped_posts = self.scrape_all_posts(post_urls, max_posts)
        
        # Save final results
        self.save_checkpoint(scraped_posts, 'all_posts_final')
        self.save_jekyll_posts(scraped_posts)
        
        print(f"Extraction complete. Found {len(scraped_posts)} posts.")
        return scraped_posts

if __name__ == "__main__":
    # Full extraction of all posts
    scraper = WordPressBlogScraper("https://blog.mithis.net", ".")
    
    # Extract all posts (no limit)
    posts = scraper.run_full_extraction(max_posts=None)
    
    print(f"\nExtraction Summary:")
    print(f"- Total posts: {len(posts)}")
    if posts:
        dates = [p['date'] for p in posts if p.get('date')]
        if dates:
            print(f"- Date range: {min(dates)} to {max(dates)}")
        categories = set(cat for p in posts for cat in p.get('categories', []))
        print(f"- Categories: {categories}")