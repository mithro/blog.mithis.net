#!/usr/bin/env python3

import requests
import json
import re
import time
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse

class ComprehensiveCommentExtractor:
    def __init__(self):
        self.base_url = "https://blog.mithis.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BlogMigrationBot/1.0)'
        })
        self.all_comments = []
        
    def get_post_urls(self):
        """Get all post URLs from migration status"""
        with open('migration_status.json', 'r') as f:
            data = json.load(f)
        
        post_urls = []
        for post in data['posts']:
            post_urls.append(post['url'])
        
        return post_urls
    
    def extract_comments_from_post(self, post_url):
        """Extract comments from a single post page"""
        print(f"Checking comments on: {post_url}")
        
        try:
            response = self.session.get(post_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find comments section
            comments_section = soup.find('div', id='comments') or soup.find('div', class_='comments')
            
            if not comments_section:
                # Try alternative selectors
                comments_section = soup.find('ol', class_='commentlist') or soup.find('div', class_='comment-list')
            
            if not comments_section:
                print(f"  No comments section found")
                return []
            
            # Extract individual comments
            comments = []
            
            # Try different comment selectors
            comment_elements = (
                comments_section.find_all('li', class_='comment') or
                comments_section.find_all('div', class_='comment') or
                comments_section.find_all('article', class_='comment')
            )
            
            for comment_elem in comment_elements:
                comment_data = self.parse_comment_element(comment_elem, post_url)
                if comment_data:
                    comments.append(comment_data)
            
            print(f"  Found {len(comments)} comments")
            return comments
            
        except Exception as e:
            print(f"  Error extracting comments: {e}")
            return []
    
    def parse_comment_element(self, comment_elem, post_url):
        """Parse a single comment element"""
        try:
            # Extract comment ID
            comment_id = comment_elem.get('id', '')
            if comment_id.startswith('comment-'):
                comment_id = comment_id.replace('comment-', '')
            elif comment_id.startswith('li-comment-'):
                comment_id = comment_id.replace('li-comment-', '')
            else:
                comment_id = str(hash(str(comment_elem)))[:8]
            
            # Extract author
            author_elem = (
                comment_elem.find('cite') or 
                comment_elem.find('span', class_='comment-author') or
                comment_elem.find('header', class_='comment-meta').find('cite') if comment_elem.find('header', class_='comment-meta') else None
            )
            
            author = author_elem.text.strip() if author_elem else "Anonymous"
            
            # Extract date
            date_elem = (
                comment_elem.find('time') or
                comment_elem.find('span', class_='comment-date') or
                comment_elem.find('a', class_='comment-date')
            )
            
            if date_elem:
                date_str = date_elem.get('datetime') or date_elem.text.strip()
                try:
                    # Try to parse the date
                    if 'T' in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        # Try common date formats
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%B %d, %Y at %I:%M %p', '%B %d, %Y']:
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                break
                            except:
                                continue
                        else:
                            date_obj = datetime.now()
                except:
                    date_obj = datetime.now()
            else:
                date_obj = datetime.now()
            
            # Extract content
            content_elem = (
                comment_elem.find('div', class_='comment-content') or
                comment_elem.find('div', class_='comment-body') or
                comment_elem.find('p')
            )
            
            content = str(content_elem) if content_elem else ""
            
            # Clean up content
            content = re.sub(r'<div[^>]*class="comment-meta"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div[^>]*class="reply"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
            content = content.strip()
            
            if not content:
                return None
            
            # Extract post slug from URL
            post_slug = post_url.split('/')[-1]
            
            comment_data = {
                'id': comment_id,
                'post_slug': post_slug,
                'author': author,
                'date': date_obj.isoformat(),
                'content': content,
                'url': f"{post_url}#comment-{comment_id}",
                'post_url': post_url
            }
            
            return comment_data
            
        except Exception as e:
            print(f"    Error parsing comment: {e}")
            return None
    
    def extract_all_comments(self):
        """Extract comments from all posts"""
        print("🗨️  Starting comprehensive comment extraction...")
        
        post_urls = self.get_post_urls()
        print(f"Found {len(post_urls)} posts to check for comments")
        
        all_comments = []
        posts_with_comments = 0
        
        for i, post_url in enumerate(post_urls):
            print(f"\n[{i+1}/{len(post_urls)}] Checking: {post_url}")
            
            comments = self.extract_comments_from_post(post_url)
            if comments:
                all_comments.extend(comments)
                posts_with_comments += 1
            
            # Be nice to the server
            time.sleep(1)
        
        print(f"\n📊 Comment Extraction Summary:")
        print(f"   - Total posts checked: {len(post_urls)}")
        print(f"   - Posts with comments: {posts_with_comments}")
        print(f"   - Total comments found: {len(all_comments)}")
        
        # Save comments
        if all_comments:
            self.save_comments(all_comments)
        
        return all_comments
    
    def save_comments(self, comments):
        """Save extracted comments to JSON file"""
        output_file = Path("exports/all_comments.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(comments)} comments to {output_file}")
        
        # Also save by post
        comments_by_post = {}
        for comment in comments:
            post_slug = comment['post_slug']
            if post_slug not in comments_by_post:
                comments_by_post[post_slug] = []
            comments_by_post[post_slug].append(comment)
        
        print(f"📝 Comments found on {len(comments_by_post)} posts:")
        for post_slug, post_comments in comments_by_post.items():
            print(f"   - {post_slug}: {len(post_comments)} comments")

if __name__ == "__main__":
    extractor = ComprehensiveCommentExtractor()
    comments = extractor.extract_all_comments()