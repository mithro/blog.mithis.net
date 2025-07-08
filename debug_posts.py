#!/usr/bin/env python3

import json
import re

def extract_post_info(url):
    """Extract post information from WordPress URL"""
    # Pattern: https://blog.mithis.net/archives/category/id-title
    match = re.search(r'/archives/([^/]+)/(\d+)-(.+)$', url)
    if match:
        category = match.group(1)
        post_id = match.group(2)
        slug = match.group(3)
        return {
            'category': category,
            'id': int(post_id),
            'slug': slug
        }
    return None

# Load all posts
with open('exports/all_post_urls.json') as f:
    sitemap_posts = json.load(f)

with open('exports/missing_post.json') as f:
    missing_posts = json.load(f)

all_posts = []
all_posts.extend(sitemap_posts)
for post in missing_posts:
    all_posts.append({
        'url': post['url'],
        'lastmod': post['lastmod']
    })

print(f"Total posts loaded: {len(all_posts)}")

processed = 0
failed = 0

for post_data in all_posts:
    url = post_data['url']
    post_info = extract_post_info(url)
    if post_info:
        processed += 1
    else:
        failed += 1
        print(f"Failed to parse: {url}")

print(f"Successfully processed: {processed}")
print(f"Failed to process: {failed}")