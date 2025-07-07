#!/usr/bin/env python3
"""
WordPress comments extraction script for Jekyll static comments
Extracts comments from WordPress RSS feed and converts to Jekyll format
"""

import feedparser
import json
import re
import os
import yaml
from datetime import datetime
from urllib.parse import urlparse

class WordPressCommentsExtractor:
    def __init__(self, comments_rss_path, output_dir):
        self.comments_rss_path = comments_rss_path
        self.output_dir = output_dir
        self.comments = []
        
    def extract_comments(self):
        """Extract comments from WordPress RSS feed"""
        print(f"Parsing comments RSS feed: {self.comments_rss_path}")
        
        # Read local RSS file
        with open(self.comments_rss_path, 'r', encoding='utf-8') as f:
            feed_content = f.read()
        
        feed = feedparser.parse(feed_content)
        
        if not feed.entries:
            print("No comments found in RSS feed")
            return []
            
        print(f"Found {len(feed.entries)} comments in RSS feed")
        
        for entry in feed.entries:
            comment = self.extract_comment_data(entry)
            if comment:
                self.comments.append(comment)
                
        return self.comments
    
    def extract_comment_data(self, entry):
        """Extract structured data from RSS comment entry"""
        try:
            # Parse comment URL to extract post and comment ID
            comment_url = entry.link
            url_parts = urlparse(comment_url)
            
            # Extract post slug from URL path
            # URL format: /archives/category/post-name#comment-id
            path_parts = url_parts.path.split('/')
            if len(path_parts) >= 4:
                post_slug = path_parts[-1]  # Get the last part as post slug
            else:
                post_slug = "unknown"
            
            # Extract comment ID from fragment
            comment_id = url_parts.fragment.replace('comment-', '') if url_parts.fragment else "unknown"
            
            # Parse publication date
            pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
            
            # Extract author name from title
            # Format: "Comment on [Post Title] by [Author]"
            title_match = re.search(r'Comment on .+ by (.+)', entry.title)
            author_name = title_match.group(1) if title_match else entry.author
            
            # Clean content - prefer content:encoded over description
            content = entry.content[0].value if entry.content else entry.description
            content = self.clean_comment_content(content)
            
            comment_data = {
                'id': comment_id,
                'post_slug': post_slug,
                'author': author_name,
                'date': pub_date,
                'content': content,
                'url': comment_url,
                'post_url': comment_url.split('#')[0]  # Remove fragment for post URL
            }
            
            return comment_data
            
        except Exception as e:
            print(f"Error parsing comment: {e}")
            print(f"Entry: {entry.title}")
            return None
    
    def clean_comment_content(self, content):
        """Clean comment content"""
        # Remove WordPress-specific elements
        content = re.sub(r'<p>(&nbsp;|\s)*</p>', '', content)
        content = content.replace('&nbsp;', ' ')
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content
    
    def save_comments_json(self):
        """Save extracted comments as JSON for processing"""
        output_file = os.path.join(self.output_dir, 'comments.json')
        
        # Convert datetime objects to strings for JSON serialization
        comments_json = []
        for comment in self.comments:
            comment_copy = comment.copy()
            comment_copy['date'] = comment['date'].isoformat()
            comments_json.append(comment_copy)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comments_json, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(comments_json)} comments to {output_file}")
    
    def save_staticman_comments(self):
        """Save comments in Staticman-compatible format"""
        comments_dir = os.path.join(self.output_dir, '_data', 'comments')
        os.makedirs(comments_dir, exist_ok=True)
        
        # Group comments by post
        post_comments = {}
        for comment in self.comments:
            post_slug = comment['post_slug']
            if post_slug not in post_comments:
                post_comments[post_slug] = []
            post_comments[post_slug].append(comment)
        
        # Save each post's comments
        for post_slug, comments in post_comments.items():
            post_dir = os.path.join(comments_dir, post_slug)
            os.makedirs(post_dir, exist_ok=True)
            
            for comment in comments:
                # Create filename with comment ID and timestamp
                filename = f"comment-{comment['id']}-{comment['date'].strftime('%Y%m%d-%H%M%S')}.yml"
                filepath = os.path.join(post_dir, filename)
                
                # Prepare comment data for YAML
                comment_data = {
                    'id': comment['id'],
                    'name': comment['author'],
                    'date': comment['date'].strftime('%Y-%m-%d %H:%M:%S %z'),
                    'message': comment['content'],
                    'wordpress_url': comment['url']
                }
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(comment_data, f, default_flow_style=False, allow_unicode=True)
        
        print(f"Saved comments for {len(post_comments)} posts to {comments_dir}")
    
    def save_jekyll_comments(self):
        """Save comments in Jekyll-compatible YAML format"""
        comments_dir = os.path.join(self.output_dir, '_data', 'comments')
        os.makedirs(comments_dir, exist_ok=True)
        
        # Group comments by post
        post_comments = {}
        for comment in self.comments:
            post_slug = comment['post_slug']
            if post_slug not in post_comments:
                post_comments[post_slug] = []
            post_comments[post_slug].append(comment)
        
        # Save comments for each post as a single YAML file
        for post_slug, comments in post_comments.items():
            filename = f"{post_slug}.yml"
            filepath = os.path.join(comments_dir, filename)
            
            # Prepare comments data
            comments_data = []
            for comment in comments:
                comment_data = {
                    'id': comment['id'],
                    'name': comment['author'],
                    'date': comment['date'].strftime('%Y-%m-%d %H:%M:%S %z'),
                    'message': comment['content'],
                    'wordpress_url': comment['url']
                }
                comments_data.append(comment_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(comments_data, f, default_flow_style=False, allow_unicode=True)
        
        print(f"Saved comments for {len(post_comments)} posts to {comments_dir}")
    
    def generate_summary(self):
        """Generate summary of extracted comments"""
        if not self.comments:
            return
            
        print(f"\nComments Extraction Summary:")
        print(f"- Total comments: {len(self.comments)}")
        print(f"- Date range: {min(c['date'] for c in self.comments)} to {max(c['date'] for c in self.comments)}")
        
        # Group by post
        post_comments = {}
        for comment in self.comments:
            post_slug = comment['post_slug']
            if post_slug not in post_comments:
                post_comments[post_slug] = []
            post_comments[post_slug].append(comment)
        
        print(f"- Posts with comments: {len(post_comments)}")
        for post_slug, comments in post_comments.items():
            print(f"  - {post_slug}: {len(comments)} comments")
        
        # Authors
        authors = set(c['author'] for c in self.comments)
        print(f"- Comment authors: {len(authors)}")
        for author in sorted(authors):
            author_comments = [c for c in self.comments if c['author'] == author]
            print(f"  - {author}: {len(author_comments)} comments")
    
    def run_extraction(self):
        """Run complete comments extraction process"""
        print(f"Starting WordPress comments extraction")
        
        # Extract comments from RSS
        self.extract_comments()
        
        if not self.comments:
            print("No comments found to process")
            return
        
        # Save in multiple formats
        self.save_comments_json()
        self.save_jekyll_comments()
        self.save_staticman_comments()
        
        # Generate summary
        self.generate_summary()
        
        print(f"Comments extraction complete. Found {len(self.comments)} comments.")
        return self.comments

if __name__ == "__main__":
    extractor = WordPressCommentsExtractor(
        "xml/feeds/comments-feed.xml", 
        "."
    )
    comments = extractor.run_extraction()