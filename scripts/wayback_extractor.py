#!/usr/bin/env python3

import json
import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path
import re
from datetime import datetime
import html

class WaybackExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BlogMigrationBot/1.0)'
        })
        
    def get_wayback_url(self, original_url):
        """Get the latest archived version of a URL from Wayback Machine"""
        # Check if URL is available
        api_url = f"http://archive.org/wayback/available?url={original_url}"
        
        try:
            response = self.session.get(api_url, timeout=10)
            data = response.json()
            
            if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                snapshot = data['archived_snapshots']['closest']
                if snapshot.get('available'):
                    return snapshot['url']
        except Exception as e:
            print(f"Error checking Wayback Machine: {e}")
            
        return None
    
    def extract_from_wayback(self, wayback_url):
        """Extract post content from Wayback Machine archive"""
        print(f"Extracting from Wayback: {wayback_url}")
        
        try:
            response = self.session.get(wayback_url, timeout=30)
            response.raise_for_status()
            
            # Remove wayback toolbar/banner
            content = response.text
            content = re.sub(r'<!--\s*BEGIN WAYBACK TOOLBAR.*?END WAYBACK TOOLBAR\s*-->', '', content, flags=re.DOTALL)
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract post data
            post_data = {
                'wayback_url': wayback_url,
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
                # Clean wayback machine artifacts
                for elem in content_elem.find_all(href=re.compile(r'web\.archive\.org')):
                    if 'href' in elem.attrs:
                        # Extract original URL from wayback URL
                        match = re.search(r'https?://web\.archive\.org/web/\d+/(https?://.*)', elem['href'])
                        if match:
                            elem['href'] = match.group(1)
                
                post_data['content'] = str(content_elem)
            else:
                post_data['content'] = ''
            
            # Categories
            categories = []
            cat_elems = soup.find_all('a', {'rel': 'category tag'})
            for cat in cat_elems:
                categories.append(cat.text.strip())
            post_data['categories'] = categories
            
            return post_data
            
        except Exception as e:
            print(f"Error extracting from Wayback: {e}")
            return None
    
    def extract_missing_posts(self):
        """Extract posts that failed with 500 errors using Wayback Machine"""
        
        # List of posts that failed with 500 errors
        failed_posts = [
            {"url": "https://blog.mithis.net/archives/tp/15-tp-protocol-overview", "id": 15, "category": "tp", "slug": "tp-protocol-overview"},
            {"url": "https://blog.mithis.net/archives/ideas/21-eagle-for-pcb", "id": 21, "category": "ideas", "slug": "eagle-for-pcb"},
            {"url": "https://blog.mithis.net/archives/pcb/23-eagle2geda-symbol-converter", "id": 23, "category": "pcb", "slug": "eagle2geda-symbol-converter"},
            {"url": "https://blog.mithis.net/archives/tp/35-using-tailor-to-go-to-git", "id": 35, "category": "tp", "slug": "using-tailor-to-go-to-git"},
            {"url": "https://blog.mithis.net/archives/uni/41-cfxs-all-done", "id": 41, "category": "uni", "slug": "cfxs-all-done"},
            {"url": "https://blog.mithis.net/archives/ideas/51-nm-autovpn", "id": 51, "category": "ideas", "slug": "nm-autovpn"},
            {"url": "https://blog.mithis.net/archives/ideas/54-nm-openvpn-dns", "id": 54, "category": "ideas", "slug": "nm-openvpn-dns"},
            {"url": "https://blog.mithis.net/archives/ideas/64-python-swap-var", "id": 64, "category": "ideas", "slug": "python-swap-var"},
            {"url": "https://blog.mithis.net/archives/uncategorized/77-epiphany2firefox", "id": 77, "category": "uncategorized", "slug": "epiphany2firefox"},
            {"url": "https://blog.mithis.net/archives/google/79-going-to-sydney", "id": 79, "category": "google", "slug": "going-to-sydney"},
            {"url": "https://blog.mithis.net/archives/uncategorized/80-rocks", "id": 80, "category": "uncategorized", "slug": "rocks"},
            {"url": "https://blog.mithis.net/archives/google/81-noogler-week-1", "id": 81, "category": "google", "slug": "noogler-week-1"},
            {"url": "https://blog.mithis.net/archives/ubuntu/84-my-three-weeks-on-a-mac", "id": 84, "category": "ubuntu", "slug": "my-three-weeks-on-a-mac"},
            {"url": "https://blog.mithis.net/archives/uncategorized/87-babylon-5-dvd-copy-protection", "id": 87, "category": "uncategorized", "slug": "babylon-5-dvd-copy-protection"},
            {"url": "https://blog.mithis.net/archives/python/90-firefox3-cookies-in-python", "id": 90, "category": "python", "slug": "firefox3-cookies-in-python"},
            {"url": "https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid", "id": 92, "category": "uncategorized", "slug": "power-scripts-in-intrepid"},
            {"url": "https://blog.mithis.net/archives/python/94-reading-cookies-firefox", "id": 94, "category": "python", "slug": "reading-cookies-firefox"},
            {"url": "https://blog.mithis.net/archives/tp/95-xcompiling-cygwin-on-linux-for-windows", "id": 95, "category": "tp", "slug": "xcompiling-cygwin-on-linux-for-windows"},
            {"url": "https://blog.mithis.net/archives/sci-fi/102-starhunter-fireflys-little-known-older-cousin", "id": 102, "category": "sci-fi", "slug": "starhunter-fireflys-little-known-older-cousin"}
        ]
        
        posts_dir = Path('_posts')
        posts_dir.mkdir(exist_ok=True)
        
        extracted = 0
        failed = []
        
        for post_info in failed_posts:
            print(f"\n[{failed_posts.index(post_info)+1}/{len(failed_posts)}] Checking Wayback Machine for: {post_info['url']}")
            
            # Get wayback URL
            wayback_url = self.get_wayback_url(post_info['url'])
            
            if wayback_url:
                # Extract from wayback
                scraped_data = self.extract_from_wayback(wayback_url)
                
                if scraped_data:
                    # Create Jekyll post
                    title = scraped_data.get('title', 'Untitled')
                    content = scraped_data.get('content', '')
                    date_str = scraped_data.get('date', '')
                    
                    # Clean content
                    content = html.unescape(content)
                    content = re.sub(r'class="[^"]*"', '', content)
                    content = re.sub(r'id="[^"]*"', '', content)
                    content = re.sub(r'style="[^"]*"', '', content)
                    
                    # Create filename
                    try:
                        if date_str and 'T' in date_str:
                            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        elif date_str:
                            date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
                        else:
                            date_obj = datetime(2007, 1, 1)  # Default date
                        date_part = date_obj.strftime('%Y-%m-%d')
                    except:
                        date_part = '2007-01-01'
                    
                    filename = f"{date_part}-{post_info['slug']}.md"
                    
                    # Create front matter
                    front_matter = {
                        'layout': 'post',
                        'title': title,
                        'date': date_str if date_str else f"{date_part} 00:00:00 +0000",
                        'categories': [post_info['category'].replace('-', ' ').title() if post_info['category'] != 'uncategorized' else 'Uncategorized'],
                        'author': 'mithro',
                        'excerpt': 'Recovered from Wayback Machine archive',
                        'wordpress_id': post_info['id'],
                        'wordpress_category': post_info['category'],
                        'wordpress_url': post_info['url'],
                        'permalink': post_info['url'].replace('https://blog.mithis.net', ''),
                        'wayback_recovered': True
                    }
                    
                    # Write Jekyll post
                    import yaml
                    file_path = posts_dir / filename
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('---\n')
                        f.write(yaml.dump(front_matter, default_flow_style=False, allow_unicode=True))
                        f.write('---\n\n')
                        f.write(content)
                    
                    print(f"✅ Recovered from Wayback: {filename}")
                    extracted += 1
                else:
                    print(f"❌ Failed to extract from Wayback")
                    failed.append(post_info['url'])
            else:
                print(f"❌ Not found in Wayback Machine")
                failed.append(post_info['url'])
            
            # Be nice to the Wayback Machine
            time.sleep(2)
        
        print(f"\n📊 Wayback Extraction Summary:")
        print(f"   - Posts recovered: {extracted}")
        print(f"   - Posts not found: {len(failed)}")
        
        if failed:
            print(f"\nStill missing:")
            for url in failed:
                print(f"   - {url}")

if __name__ == "__main__":
    extractor = WaybackExtractor()
    extractor.extract_missing_posts()