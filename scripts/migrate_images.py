#!/usr/bin/env python3

import os
import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse, urljoin
import hashlib

class ImageMigrator:
    def __init__(self):
        self.base_url = "https://blog.mithis.net"
        self.posts_dir = Path("_posts")
        self.images_dir = Path("assets/images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Create session for better performance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BlogMigrationBot/1.0)'
        })
        
        # Track downloaded images to avoid duplicates
        self.downloaded_images = set()
        
    def find_image_urls(self):
        """Find all image URLs in Jekyll posts"""
        image_urls = set()
        
        for post_file in self.posts_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find various image patterns
                patterns = [
                    r'src="([^"]*wp-content/uploads/[^"]*)"',
                    r'href="([^"]*wp-content/uploads/[^"]*)"',
                    r'src="([^"]*web\.archive\.org[^"]*wp-content/uploads/[^"]*)"',
                    r'href="([^"]*web\.archive\.org[^"]*wp-content/uploads/[^"]*)"',
                    r'!\[.*?\]\(([^)]*wp-content/uploads/[^)]*)\)',
                    r'<img[^>]*src="([^"]*blog\.mithis\.net[^"]*uploads/[^"]*)"',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        image_urls.add((match, post_file.name))
                        
            except Exception as e:
                print(f"Error reading {post_file}: {e}")
        
        return image_urls
    
    def extract_original_url(self, url):
        """Extract original URL from Wayback Machine URL"""
        # Handle wayback machine URLs
        if 'web.archive.org' in url:
            # Extract the original URL from wayback format
            # http://web.archive.org/web/20090817225635/http://blog.mithis.net/wp-content/uploads/2007/03/board.png
            match = re.search(r'https?://web\.archive\.org/web/\d+(?:im_)?/(https?://.*)', url)
            if match:
                return match.group(1)
        
        # Handle relative URLs
        if url.startswith('/'):
            return f"{self.base_url}{url}"
        
        # Handle absolute URLs
        if url.startswith('http'):
            return url
        
        return None
    
    def get_local_path(self, url):
        """Get local path for image based on URL"""
        # Extract the path after wp-content/uploads/
        match = re.search(r'wp-content/uploads/(.+)', url)
        if match:
            relative_path = match.group(1)
            return self.images_dir / "wp-content" / "uploads" / relative_path
        
        # Fallback: use filename
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if filename:
            return self.images_dir / filename
        
        return None
    
    def download_image(self, url, local_path):
        """Download image from URL to local path"""
        try:
            # Create directory if it doesn't exist
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file already exists
            if local_path.exists():
                print(f"  Already exists: {local_path}")
                return True
            
            print(f"  Downloading: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Write image to file
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  Saved: {local_path}")
            return True
            
        except Exception as e:
            print(f"  Error downloading {url}: {e}")
            return False
    
    def update_post_image_urls(self, post_file, old_url, new_url):
        """Update image URLs in post file"""
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the old URL with the new one
            updated_content = content.replace(old_url, new_url)
            
            if updated_content != content:
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  Updated URLs in {post_file}")
                return True
            
        except Exception as e:
            print(f"  Error updating {post_file}: {e}")
            
        return False
    
    def migrate_images(self):
        """Main image migration function"""
        print("🖼️  Starting image migration...")
        
        # Find all image URLs
        image_urls = self.find_image_urls()
        print(f"Found {len(image_urls)} image references")
        
        if not image_urls:
            print("No images found to migrate")
            return
        
        downloaded_count = 0
        failed_count = 0
        updated_posts = set()
        
        for original_url, post_file in image_urls:
            print(f"\n📷 Processing: {original_url}")
            
            # Extract the actual URL to download
            download_url = self.extract_original_url(original_url)
            if not download_url:
                print(f"  ❌ Could not extract URL from: {original_url}")
                failed_count += 1
                continue
            
            # Get local path for image
            local_path = self.get_local_path(download_url)
            if not local_path:
                print(f"  ❌ Could not determine local path for: {download_url}")
                failed_count += 1
                continue
            
            # Download image
            if self.download_image(download_url, local_path):
                downloaded_count += 1
                
                # Calculate new URL relative to site root
                new_url = "/" + str(local_path).replace("assets/images/", "assets/images/")
                
                # Update post with new URL
                post_path = self.posts_dir / post_file
                if self.update_post_image_urls(post_path, original_url, new_url):
                    updated_posts.add(post_file)
            else:
                failed_count += 1
            
            # Be nice to the server
            time.sleep(0.5)
        
        print(f"\n📊 Image Migration Summary:")
        print(f"   - Images downloaded: {downloaded_count}")
        print(f"   - Images failed: {failed_count}")
        print(f"   - Posts updated: {len(updated_posts)}")
        
        if updated_posts:
            print(f"\nUpdated posts:")
            for post in sorted(updated_posts):
                print(f"   - {post}")

if __name__ == "__main__":
    migrator = ImageMigrator()
    migrator.migrate_images()