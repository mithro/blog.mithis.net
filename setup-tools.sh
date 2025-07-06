#!/bin/bash

# WordPress to Jekyll Migration - Tool Setup Script
# This script installs the recommended tools for efficient migration work

set -e

echo "🚀 Setting up WordPress to Jekyll migration tools..."

# Check if we're in the right directory
if [ ! -f "MIGRATION_PLAN.md" ]; then
    echo "❌ Error: Please run this script from the blog.mithis.net project directory"
    exit 1
fi

echo "📦 Installing Ruby gems..."
if command -v gem &> /dev/null; then
    gem install bundler jekyll
    gem install jekyll-import
    gem install html-proofer
    echo "✅ Ruby gems installed"
else
    echo "⚠️  Ruby not found. Please install Ruby first:"
    echo "   curl -sSL https://get.rvm.io | bash"
    echo "   rvm install ruby-3.0"
fi

echo "📦 Installing Node.js packages..."
if command -v npm &> /dev/null; then
    npm install -g broken-link-checker
    npm install -g html-validate
    npm install -g lighthouse
    echo "✅ Node.js packages installed"
else
    echo "⚠️  Node.js not found. Please install Node.js first"
fi

echo "📦 Installing system tools..."
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y imagemagick pandoc wget curl
    echo "✅ System tools installed (apt)"
elif command -v brew &> /dev/null; then
    # macOS
    brew install imagemagick pandoc wget
    brew install imageoptim-cli
    echo "✅ System tools installed (brew)"
else
    echo "⚠️  Package manager not found. Please install manually:"
    echo "   - ImageMagick"
    echo "   - Pandoc" 
    echo "   - wget"
fi

echo "📦 Installing additional tools..."
if command -v cargo &> /dev/null; then
    cargo install ripgrep
    echo "✅ ripgrep installed"
else
    echo "⚠️  Rust/Cargo not found. Install ripgrep manually or install Rust first"
fi

# Create helpful directories
mkdir -p _scripts exports assets/images

echo "📁 Created project directories:"
echo "   - _scripts/ (for migration scripts)"
echo "   - exports/ (for WordPress exports)"
echo "   - assets/images/ (for optimized images)"

# Create a simple Jekyll Gemfile if it doesn't exist
if [ ! -f "Gemfile" ]; then
    cat > Gemfile << 'EOF'
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-feed"
gem "jekyll-sitemap"
gem "jekyll-redirect-from"
gem "html-proofer"
gem "jekyll-import"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
end
EOF
    echo "✅ Created Gemfile with essential Jekyll gems"
fi

echo ""
echo "🎉 Tool setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'bundle install' to install Jekyll dependencies"
echo "2. Check tool versions with:"
echo "   - jekyll --version"
echo "   - lighthouse --version"
echo "   - blc --version"
echo "3. Start migration with Phase 1 tasks in MIGRATION_PLAN.md"
echo ""
echo "💡 Tip: Use 'rg' instead of 'grep' for faster searching in the codebase"