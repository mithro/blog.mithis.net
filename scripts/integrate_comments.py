#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path

class CommentIntegrator:
    def __init__(self):
        self.posts_dir = Path("_posts")
        self.comments_file = Path("exports/comments.json")
        
    def load_comments(self):
        """Load comments from JSON file"""
        with open(self.comments_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_post_file(self, post_slug):
        """Find the Jekyll post file for a given slug"""
        # Try to find the post file based on slug
        for post_file in self.posts_dir.glob("*.md"):
            # Check if slug matches filename
            if post_slug in post_file.name:
                return post_file
                
            # Check if slug matches permalink in front matter
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if f"/{post_slug}" in content:
                        return post_file
            except:
                continue
        
        return None
    
    def add_comments_to_post(self, post_file, comments):
        """Add comments to a Jekyll post"""
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split front matter and content
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1]
                post_content = parts[2]
                
                # Add comments to front matter
                comments_yaml = "comments:\n"
                for comment in comments:
                    comments_yaml += f"  - id: {comment['id']}\n"
                    comments_yaml += f"    author: {comment['author']}\n"
                    comments_yaml += f"    date: {comment['date']}\n"
                    comments_yaml += f"    content: |\n"
                    # Indent comment content
                    comment_lines = comment['content'].split('\n')
                    for line in comment_lines:
                        comments_yaml += f"      {line}\n"
                
                # Add comments to front matter
                updated_front_matter = front_matter.rstrip() + "\n" + comments_yaml
                
                # Add comments section to post content
                comments_html = "\n\n## Comments\n\n"
                comments_html += "<div class=\"comments\">\n"
                
                for comment in comments:
                    comments_html += f"<div class=\"comment\" id=\"comment-{comment['id']}\">\n"
                    comments_html += f"  <div class=\"comment-meta\">\n"
                    comments_html += f"    <strong>{comment['author']}</strong> - "
                    comments_html += f"    <time datetime=\"{comment['date']}\">{comment['date'][:10]}</time>\n"
                    comments_html += f"  </div>\n"
                    comments_html += f"  <div class=\"comment-content\">\n"
                    comments_html += f"    {comment['content']}\n"
                    comments_html += f"  </div>\n"
                    comments_html += f"</div>\n\n"
                
                comments_html += "</div>\n\n"
                comments_html += "<style>\n"
                comments_html += ".comments {\n"
                comments_html += "  margin-top: 2rem;\n"
                comments_html += "  border-top: 1px solid #eee;\n"
                comments_html += "  padding-top: 2rem;\n"
                comments_html += "}\n\n"
                comments_html += ".comment {\n"
                comments_html += "  margin-bottom: 1.5rem;\n"
                comments_html += "  padding: 1rem;\n"
                comments_html += "  background: #f9f9f9;\n"
                comments_html += "  border-left: 4px solid #ddd;\n"
                comments_html += "}\n\n"
                comments_html += ".comment-meta {\n"
                comments_html += "  font-size: 0.9rem;\n"
                comments_html += "  color: #666;\n"
                comments_html += "  margin-bottom: 0.5rem;\n"
                comments_html += "}\n\n"
                comments_html += ".comment-content {\n"
                comments_html += "  line-height: 1.6;\n"
                comments_html += "}\n\n"
                comments_html += ".comment-content p {\n"
                comments_html += "  margin: 0.5rem 0;\n"
                comments_html += "}\n"
                comments_html += "</style>\n"
                
                # Reconstruct the file
                updated_content = "---\n" + updated_front_matter + "---" + post_content.rstrip() + comments_html
                
                # Write updated content
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
                return True
                
        except Exception as e:
            print(f"Error updating {post_file}: {e}")
            return False
    
    def integrate_comments(self):
        """Main function to integrate comments into posts"""
        print("🗨️  Integrating comments into Jekyll posts...")
        
        # Load comments
        comments = self.load_comments()
        print(f"Found {len(comments)} comments to integrate")
        
        # Group comments by post
        comments_by_post = {}
        for comment in comments:
            post_slug = comment['post_slug']
            if post_slug not in comments_by_post:
                comments_by_post[post_slug] = []
            comments_by_post[post_slug].append(comment)
        
        # Integrate comments into posts
        integrated_posts = 0
        failed_posts = []
        
        for post_slug, post_comments in comments_by_post.items():
            print(f"\n📝 Processing post: {post_slug}")
            print(f"   Comments: {len(post_comments)}")
            
            # Find the post file
            post_file = self.find_post_file(post_slug)
            if not post_file:
                print(f"   ❌ Could not find post file for {post_slug}")
                failed_posts.append(post_slug)
                continue
            
            print(f"   Found post file: {post_file}")
            
            # Sort comments by date
            post_comments.sort(key=lambda x: x['date'])
            
            # Add comments to post
            if self.add_comments_to_post(post_file, post_comments):
                print(f"   ✅ Successfully integrated {len(post_comments)} comments")
                integrated_posts += 1
            else:
                print(f"   ❌ Failed to integrate comments")
                failed_posts.append(post_slug)
        
        print(f"\n📊 Comment Integration Summary:")
        print(f"   - Posts with comments integrated: {integrated_posts}")
        print(f"   - Posts failed: {len(failed_posts)}")
        print(f"   - Total comments integrated: {len(comments)}")
        
        if failed_posts:
            print(f"\nFailed posts:")
            for post in failed_posts:
                print(f"   - {post}")

if __name__ == "__main__":
    integrator = CommentIntegrator()
    integrator.integrate_comments()