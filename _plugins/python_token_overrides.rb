# frozen_string_literal: true
#
# python_token_overrides.rb
#
# Rouge's Python lexer classifies certain tokens that live's GeSHi colored
# differently. We can't differentiate them via CSS class alone (since CSS
# can't match by text content), so post-process the rendered HTML to
# inject inline styles on specific token-text combinations.
#
# Live's GeSHi color map (extracted via DOM inspection):
#   `open`, `raw_input`  → #008000 (green, builtin) — Rouge tags as .nf
#   `,`                  → #66cc66 (light green op) — Rouge tags as .p
#   `pysqlite2`, `dbapi2` (non-stdlib modules)
#                        → #110000 (plain text)    — Rouge tags as .n
#                          (so REMOVE crimson coloring my CSS would apply via .kn + .n)
#
# Scoped to `.language-python` code blocks only.

PY_TOKEN_OVERRIDES = {
  # Builtins that Rouge wrongly classifies as .nf (Function call)
  # Live colored bold/normal green like other builtins
  %r{<span class="nf">(open|raw_input)</span>} =>
    '<span class="nf" style="color: #008000;">\1</span>',

  # Comma (.p punctuation) — live colored light green
  %r{<span class="p">,</span>} =>
    '<span class="p" style="color: #66cc66;">,</span>',

  # Non-stdlib module names in `from X import Y` that live left plain.
  # My CSS colors these crimson via `.kn + .n`. Override back to plain
  # text (inherits #110000 from .wp_syntax). Currently only `pysqlite2`,
  # `dbapi2` known.
  %r{<span class="n">(pysqlite2|dbapi2)</span>} =>
    '<span class="n" style="color: inherit;">\1</span>',
}.freeze

Jekyll::Hooks.register %i[documents pages], :post_render do |item|
  next if item.output.nil?
  next unless item.output_ext == ".html"
  # Quick bail-out if no python code block on the page
  next unless item.output.include?("language-python")

  PY_TOKEN_OVERRIDES.each do |pattern, replacement|
    item.output = item.output.gsub(pattern, replacement)
  end
end
