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

  # Known stdlib module names that live's GeSHi colored crimson when
  # used as `module.attribute` (e.g. `os.path.join`, `logging.error`).
  # Rouge tags them as `.n` and the `.has(+ .p + .nc)` rule misses them
  # because `.attribute` is `.n` (not `.nc`) — color via plugin instead.
  %r{<span class="n">(os|logging|_winreg|sys|re|json|urllib|urllib2|urlparse|httplib|sqlite3)</span>} =>
    '<span class="n" style="color: #dc143c;">\1</span>',

  # Known stdlib class names that live's GeSHi colored crimson when used
  # as `module.ClassName` constructor calls. Rouge tags as `.nc` and my
  # default `.nc { color: #000 }` makes them black. List explicit names
  # to differentiate from method calls like `winreg.OpenKey(...)` where
  # live colored OpenKey BLACK (not in GeSHi's class list).
  %r{<span class="nc">(ConfigParser|StringIO)</span>} =>
    '<span class="nc" style="color: #dc143c;">\1</span>',
}.freeze

# Live's GeSHi highlights `\X` (backslash + letter) inside ALL strings —
# even raw strings (`r'...'`) where Python skips escape interpretation.
# Rouge correctly skips these in raw strings, so we have to inject the
# .se highlighting inside `.s` (and .s1, .s2) spans manually. Live's
# color: #000099 bold.
STRING_ESCAPE_RE = %r{(<span class="(?:s|s1|s2)">)([^<]*)(</span>)}.freeze
ESCAPE_CHAR_RE = %r{(\\[A-Za-z])}.freeze

Jekyll::Hooks.register %i[documents pages], :post_render do |item|
  next if item.output.nil?
  next unless item.output_ext == ".html"
  # Quick bail-out if no python code block on the page
  next unless item.output.include?("language-python")

  PY_TOKEN_OVERRIDES.each do |pattern, replacement|
    item.output = item.output.gsub(pattern, replacement)
  end

  # Wrap `\X` (backslash+letter) inside .s strings with .se spans —
  # matches live's escape highlighting even in raw strings.
  item.output = item.output.gsub(STRING_ESCAPE_RE) do
    open_tag = Regexp.last_match(1)
    content = Regexp.last_match(2)
    close_tag = Regexp.last_match(3)
    new_content = content.gsub(ESCAPE_CHAR_RE) do
      esc = Regexp.last_match(1)
      "</span><span class=\"se\" style=\"color: #000099; font-weight: bold;\">#{esc}</span>#{open_tag}"
    end
    "#{open_tag}#{new_content}#{close_tag}"
  end
end
