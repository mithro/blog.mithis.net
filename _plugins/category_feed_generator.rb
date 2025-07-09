# Category Feed Generator Plugin
# Automatically generates RSS feeds for each category

module CategoryFeedGenerator
  class Generator < Jekyll::Generator
    safe true
    priority :normal

    def generate(site)
      # Get all categories from site posts
      categories = site.posts.docs.map { |post| post.data['categories'] }.flatten.compact.uniq

      categories.each do |category|
        # Create a new page for each category feed
        site.pages << CategoryFeedPage.new(site, category)
      end
    end
  end

  class CategoryFeedPage < Jekyll::Page
    def initialize(site, category)
      @site = site
      @base = site.source
      @dir = "category/#{category.downcase.gsub(/[^a-z0-9\-_]/, '-')}"
      @name = 'feed.xml'

      self.process(@name)
      self.read_yaml(File.join(@base, '_layouts'), 'category_feed.xml')
      
      self.data['category'] = category
      self.data['permalink'] = "/category/#{category.downcase.gsub(/[^a-z0-9\-_]/, '-')}/feed/"
      self.data['layout'] = nil
    end
  end
end