#!/bin/bash

# Download RSS feeds and sitemaps from blog.mithis.net for content analysis

echo "Downloading WordPress RSS feeds and sitemaps..."

# Create output directories
mkdir -p xml/feeds xml/sitemaps

# Download main RSS feed
echo "Downloading main RSS feed..."
wget -q "https://blog.mithis.net/feed/" -O xml/feeds/main-feed.xml

# Download comments RSS feed
echo "Downloading comments RSS feed..."
wget -q "https://blog.mithis.net/comments/feed/" -O xml/feeds/comments-feed.xml

# Download main sitemap
echo "Downloading main sitemap..."
wget -q "https://blog.mithis.net/sitemap.xml" -O xml/sitemaps/sitemap.xml

# Download sitemap index
echo "Downloading sitemap index..."
wget -q "https://blog.mithis.net/sitemap_index.xml" -O xml/sitemaps/sitemap_index.xml

# Try to download individual sitemaps (based on common patterns)
echo "Downloading individual sitemaps..."
for year in {2006..2020}; do
    for month in {01..12}; do
        sitemap_url="https://blog.mithis.net/sitemap-post-${year}-${month}.xml"
        output_file="xml/sitemaps/sitemap-post-${year}-${month}.xml"
        
        # Try to download, suppress errors for non-existent sitemaps
        if wget -q --spider "$sitemap_url" 2>/dev/null; then
            echo "Downloading sitemap for ${year}-${month}..."
            wget -q "$sitemap_url" -O "$output_file"
        fi
    done
done

# Download category sitemaps
echo "Downloading category sitemaps..."
wget -q "https://blog.mithis.net/sitemap-tax-category.xml" -O xml/sitemaps/sitemap-categories.xml 2>/dev/null

# Download pages sitemap  
echo "Downloading pages sitemap..."
wget -q "https://blog.mithis.net/sitemap-page.xml" -O xml/sitemaps/sitemap-pages.xml 2>/dev/null

echo "Download complete. Files saved to xml/ directory."
echo "Run 'ls -la xml/feeds/ xml/sitemaps/' to see downloaded files."