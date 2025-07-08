#!/usr/bin/env python3

import json
import requests
import os
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re
from datetime import datetime
import html

class MissingPostExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BlogMigrationBot/1.0)'
        })
        
    def load_missing_posts(self):
        """Load list of posts that still need extraction"""
        with open('migration_status.json', 'r') as f:
            data = json.load(f)
        
        missing = []
        for post in data['posts']:
            if post['status'] == 'pending':
                missing.append(post)
        
        return missing
    
    def scrape_post(self, url):
        """Scrape a single WordPress post"""
        print(f"Scraping: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract post data
            post_data = {
                'url': url,
                'scraped': True
            }
            
            # Title
            title_elem = soup.find('h2', class_='entry-title')
            if not title_elem:
                title_elem = soup.find('h1', class_='entry-title')
            post_data['title'] = title_elem.text.strip() if title_elem else 'Untitled'
            
            # Date
            date_elem = soup.find('div', class_='entry-date')
            if date_elem:
                abbr = date_elem.find('abbr')
                if abbr and 'title' in abbr.attrs:
                    post_data['date'] = abbr['title']
                else:
                    post_data['date'] = date_elem.text.strip()
            
            # Content
            content_elem = soup.find('div', class_='entry-content')
            if content_elem:
                post_data['content'] = str(content_elem)
            else:
                post_data['content'] = ''
            
            # Categories
            categories = []
            cat_elems = soup.find_all('a', {'rel': 'category tag'})
            for cat in cat_elems:
                categories.append(cat.text.strip())
            post_data['categories'] = categories
            
            # Excerpt - try to generate if not found
            excerpt_elem = soup.find('div', class_='entry-excerpt')
            if excerpt_elem:
                post_data['excerpt'] = excerpt_elem.text.strip()
            else:
                # Generate from content
                text = BeautifulSoup(post_data['content'], 'html.parser').get_text()
                post_data['excerpt'] = text[:200].strip() + '...' if len(text) > 200 else text
            
            return post_data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def create_jekyll_post(self, post_info, scraped_data):
        """Create Jekyll post from scraped data"""
        if not scraped_data:
            return None
            
        # Get metadata from post_info
        wp_id = post_info['id']
        category = post_info['category']
        slug = post_info['slug']
        
        # Get content from scraped data
        title = scraped_data.get('title', 'Untitled')
        content = scraped_data.get('content', '')
        date_str = scraped_data.get('date', post_info.get('lastmod', ''))
        excerpt = scraped_data.get('excerpt', '')
        
        # Clean content
        content = html.unescape(content)
        content = re.sub(r'class="[^"]*"', '', content)
        content = re.sub(r'id="[^"]*"', '', content)
        content = re.sub(r'style="[^"]*"', '', content)
        
        # Create filename
        try:
            if 'T' in date_str:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
            date_part = date_obj.strftime('%Y-%m-%d')
        except:
            date_part = 'unknown-date'
        
        filename = f"{date_part}-{slug}.md"
        
        # Create front matter
        front_matter = {
            'layout': 'post',
            'title': title,
            'date': date_str,
            'categories': [category.replace('-', ' ').title() if category != 'uncategorized' else 'Uncategorized'],
            'author': 'mithro',
            'excerpt': excerpt[:200] + '...' if len(excerpt) > 200 else excerpt,
            'wordpress_id': wp_id,
            'wordpress_category': category,
            'wordpress_url': post_info['url'],
            'permalink': post_info['url'].replace('https://blog.mithis.net', '')
        }
        
        return filename, front_matter, content
    
    def extract_missing_posts(self):
        """Main extraction function"""
        missing_posts = self.load_missing_posts()
        print(f"Found {len(missing_posts)} posts to extract")
        
        # Ensure _posts directory exists
        posts_dir = Path('_posts')
        posts_dir.mkdir(exist_ok=True)
        
        extracted = 0
        failed = []
        
        for i, post_info in enumerate(missing_posts):
            print(f"\n[{i+1}/{len(missing_posts)}] Processing: {post_info['url']}")
            
            # Check if file already exists
            expected_file = f"{post_info.get('lastmod', '')[:10]}-{post_info['slug']}.md"
            if (posts_dir / expected_file).exists():
                print(f"✓ Already exists: {expected_file}")
                continue
            
            # Scrape the post
            scraped_data = self.scrape_post(post_info['url'])
            
            if scraped_data:
                # Convert to Jekyll
                result = self.create_jekyll_post(post_info, scraped_data)
                
                if result:
                    filename, front_matter, content = result
                    
                    # Write Jekyll post
                    import yaml
                    file_path = posts_dir / filename
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('---\n')
                        f.write(yaml.dump(front_matter, default_flow_style=False, allow_unicode=True))
                        f.write('---\n\n')
                        f.write(content)
                    
                    print(f"✅ Created: {filename}")
                    extracted += 1
                else:
                    print(f"❌ Failed to convert post")
                    failed.append(post_info['url'])
            else:
                failed.append(post_info['url'])
            
            # Be nice to the server
            time.sleep(1)
            
            # Save progress every 5 posts
            if (i + 1) % 5 == 0:
                print(f"\nProgress: {extracted} extracted, {len(failed)} failed")
        
        print(f"\n📊 Extraction Summary:")
        print(f"   - Posts extracted: {extracted}")
        print(f"   - Posts failed: {len(failed)}")
        
        if failed:
            print(f"\nFailed URLs:")
            for url in failed:
                print(f"   - {url}")

if __name__ == "__main__":
    extractor = MissingPostExtractor()
    extractor.extract_missing_posts()