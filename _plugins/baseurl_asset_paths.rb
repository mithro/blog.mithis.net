# frozen_string_literal: true
#
# baseurl_asset_paths.rb
#
# WordPress-exported posts embed images as raw HTML with hardcoded,
# root-relative paths, e.g.:
#
#     <img src="/assets/images/wp-content/uploads/2014/07/foo.jpg" .../>
#     <a href="/assets/images/.../foo.jpg"><img srcset="/assets/.../foo.jpg 225w"></a>
#
# Those paths are correct when the site is served at the domain root
# (baseurl: "" -- the blog.mithis.net custom-domain cutover) but 404 when the
# site is served under a project subpath
# (baseurl: "/blog.mithis.net" -- the mithro.github.io staging deploy).
#
# Template-authored URLs already go through Jekyll's `relative_url` filter, so
# they pick up site.baseurl automatically; only the raw post-body HTML (16 refs
# across 15 posts, all under /assets/) needs fixing. Editing the posts would
# mean injecting Liquid into the markdown, so instead we rewrite the *rendered*
# output here and keep the source markdown clean.
#
#   * HTML pages  -> relative prefix  "#{baseurl}/assets/"        (matches the
#                    rest of the page, which uses relative_url)
#   * XML feeds   -> absolute prefix  "#{url}#{baseurl}/assets/"  (feeds are
#                    consumed out of page context, so URLs must be absolute)
#
# Strict no-op when baseurl is empty, so the custom-domain cutover output stays
# byte-for-byte identical to what the fidelity passes validated. Already-prefixed
# paths (e.g. /blog.mithis.net/assets/... emitted by relative_url) don't match
# the `="/assets/` anchor, so they are never double-prefixed.
#
# NB: runs only under the Actions-based Pages build; the legacy branch builder
# runs Jekyll in safe mode and ignores _plugins entirely.

ASSET_ATTR_RE = %r{\b(src|href|srcset)=("|')/assets/}.freeze

Jekyll::Hooks.register %i[documents pages], :post_render do |item|
  baseurl = item.site.config["baseurl"].to_s
  next if baseurl.empty? # no-op at the custom-domain cutover
  next if item.output.nil?

  prefix =
    case item.output_ext
    when ".html" then "#{baseurl}/assets/"
    when ".xml"  then "#{item.site.config['url']}#{baseurl}/assets/"
    else next
    end

  item.output = item.output.gsub(ASSET_ATTR_RE) do
    "#{Regexp.last_match(1)}=#{Regexp.last_match(2)}#{prefix}"
  end
end
