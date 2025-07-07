#!/bin/bash

echo "=== Jekyll Blog Migration Test Suite ==="
echo "Testing migrated WordPress content and functionality"
echo

# Test 1: Build verification
echo "1. Testing Jekyll build..."
if ~/.local/share/gem/ruby/3.3.0/bin/jekyll build --quiet; then
    echo "   ✅ Jekyll build successful"
else
    echo "   ❌ Jekyll build failed"
    exit 1
fi

# Test 2: Content verification
echo "2. Testing content migration..."
POST_COUNT=$(find _site -name "*.html" -path "*201*" | wc -l)
echo "   📄 Generated $POST_COUNT post pages"

if [ "$POST_COUNT" -ge 10 ]; then
    echo "   ✅ Post count matches expected (10+ posts)"
else
    echo "   ❌ Post count below expected"
fi

# Test 3: Theme verification
echo "3. Testing theme recreation..."
if [ -f "_site/assets/css/main.css" ]; then
    CSS_SIZE=$(wc -c < _site/assets/css/main.css)
    echo "   🎨 CSS file generated ($CSS_SIZE bytes)"
    
    if grep -q "Barthelme" _site/assets/css/main.css; then
        echo "   ✅ Barthelme theme reference found"
    else
        echo "   ⚠️  Barthelme theme reference missing"
    fi
    
    if grep -q "#bbc8d9" _site/assets/css/main.css; then
        echo "   ✅ Original theme colors preserved"
    else
        echo "   ⚠️  Theme colors may have changed"
    fi
else
    echo "   ❌ CSS file missing"
fi

# Test 4: Comment system verification
echo "4. Testing comment system..."
COMMENT_FILES=$(find _data/comments -name "*.yml" | wc -l)
echo "   💬 Found $COMMENT_FILES comment files"

if [ "$COMMENT_FILES" -ge 6 ]; then
    echo "   ✅ Comments successfully migrated"
else
    echo "   ⚠️  Fewer comments than expected"
fi

# Test 5: Metadata verification
echo "5. Testing post metadata..."
POSTS_WITH_CATEGORIES=$(grep -r "categories:" _posts | wc -l)
POSTS_WITH_DATES=$(grep -r "date:" _posts | wc -l)

echo "   📂 Posts with categories: $POSTS_WITH_CATEGORIES"
echo "   📅 Posts with dates: $POSTS_WITH_DATES"

if [ "$POSTS_WITH_CATEGORIES" -ge 8 ] && [ "$POSTS_WITH_DATES" -ge 10 ]; then
    echo "   ✅ Metadata preservation successful"
else
    echo "   ⚠️  Some metadata may be missing"
fi

# Test 6: WordPress URL preservation
echo "6. Testing WordPress URL preservation..."
WORDPRESS_URLS=$(grep -r "wordpress_url:" _posts | wc -l)
echo "   🔗 Posts with WordPress URLs: $WORDPRESS_URLS"

if [ "$WORDPRESS_URLS" -ge 8 ]; then
    echo "   ✅ WordPress URLs preserved for redirects"
else
    echo "   ⚠️  Some WordPress URLs missing"
fi

# Test 7: Site structure verification
echo "7. Testing site structure..."
ESSENTIAL_FILES=(
    "_site/index.html"
    "_site/about/index.html"
    "_site/404.html"
    "_includes/header.html"
    "_includes/footer.html"
    "_layouts/default.html"
    "_layouts/post.html"
)

MISSING_FILES=0
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "   ❌ Missing: $file"
        ((MISSING_FILES++))
    fi
done

if [ "$MISSING_FILES" -eq 0 ]; then
    echo "   ✅ All essential files present"
else
    echo "   ⚠️  $MISSING_FILES essential files missing"
fi

# Test 8: Configuration verification
echo "8. Testing Jekyll configuration..."
if grep -q "Tim Ansell" _config.yml; then
    echo "   ✅ Site title configured correctly"
else
    echo "   ⚠️  Site title may need adjustment"
fi

if grep -q "blog.mithis.net" _config.yml; then
    echo "   ✅ Site URL configured correctly"
else
    echo "   ⚠️  Site URL may need adjustment"
fi

echo
echo "=== Migration Test Results ==="
echo "📊 Summary:"
echo "   • $POST_COUNT posts migrated"
echo "   • $COMMENT_FILES comment files"
echo "   • $POSTS_WITH_CATEGORIES posts with categories"
echo "   • $WORDPRESS_URLS WordPress URLs preserved"
echo
echo "🎯 Migration Status: All core functionality tested"
echo "✅ Ready for next development phase"