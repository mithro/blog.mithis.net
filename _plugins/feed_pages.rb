# frozen_string_literal: true

# feed_pages.rb — generate the site's RSS feeds instead of carrying ~24
# hand-written, near-identical XML template files in the repo (issue #6).
#
# Generates:
#   * One RSS2 feed per category page (layout: category) at
#     "<category permalink>feed/" — e.g. /archives/category/python/feed/ —
#     matching live WordPress's per-category feed URLs. Redirect stubs are
#     derived from the category page's own redirect_from entries
#     (e.g. /category/python/ -> /category/python/feed/), so legacy feed
#     URLs keep redirecting exactly as the hand-written files did.
#   * The site-wide RSS2 feed at /feed/ (live WP's main feed URL, written
#     as /feed/index.xml) and its Jekyll-era alias /feed.xml.
#
# Templates live in _includes/feed-category.xml and _includes/feed-main.xml.
#
# priority :high — jekyll-redirect-from's generator runs at :normal, and it
# only creates redirect stubs for pages that exist when it runs. Generating
# the feed pages first is what makes their redirect_from entries take effect.
#
# The generated pages set sitemap: false. That matters: site.html_pages
# includes any page whose URL ends in "/" (even XML feeds), so without the
# flag jekyll-sitemap would list every feed in sitemap.xml.

module Blog
  class FeedPages < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      category_template = template(site, "feed-category.xml")
      main_template = template(site, "feed-main.xml")

      site.pages.select { |page| page.data["layout"] == "category" }.each do |cat|
        redirects = Array(cat.data["redirect_from"]).map { |from| "#{from}feed/" }
        site.pages << feed_page(site, category_template,
                                "permalink" => "#{cat.data["permalink"]}feed/",
                                "category" => cat.data["cat_slug"],
                                "redirect_from" => redirects)
      end

      ["/feed/index.xml", "/feed.xml"].each do |permalink|
        site.pages << feed_page(site, main_template, "permalink" => permalink)
      end
    end

    private

    def feed_page(site, content, data)
      # Each page needs a UNIQUE dir/name: Jekyll's LiquidRenderer caches the
      # parsed template per page path (cache[@filename] ||= parse), so pages
      # sharing a path would all render whichever page got parsed first.
      permalink = data["permalink"]
      if permalink.end_with?("/")
        dir, name = permalink, "index.xml"
      else
        dir, name = File.dirname(permalink), File.basename(permalink)
      end
      page = Jekyll::PageWithoutAFile.new(site, site.source, dir, name)
      page.content = content
      page.data.merge!("layout" => nil, "sitemap" => false)
      page.data.merge!(data)
      page
    end

    def template(site, name)
      File.read(site.in_source_dir("_includes", name))
    end
  end
end
