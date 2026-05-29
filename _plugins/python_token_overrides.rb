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
  # Live's GeSHi only highlights the `\u` portion of `\uXXXX` Unicode
  # escapes (where XXXX is 4 hex digits) — the hex chars stay as string
  # color. Rouge wraps the whole `☺` in `.se`. Split the span so
  # only `\u` gets the bold blue, the hex chars get string color.
  %r{<span class="se">(\\u)([0-9A-Fa-f]{4})</span>} =>
    '<span class="se">\1</span><span class="s2" style="color: #483d8b;">\2</span>',

  # String affix `r` `b` `u` (raw/bytes/unicode prefix) — live emitted
  # the prefix as plain PRE text (no span). DOM probe confirmed: live's
  # `r` parent is the PRE itself, local's is a `<span class="sa">`.
  # Even with matching color, the extra span boundary on local causes
  # sub-pixel anti-aliasing drift on the adjacent quote character.
  # Strip the span entirely — leave the prefix as bare text.
  %r{<span class="sa">(r|R|b|B|u|U)</span>} => '\1',

  # Merge string quote spans into the string content span. Rouge wraps
  # short strings as <sh>'</sh><s>X</s><sh>'</sh> (3 spans). Live had
  # one span for the whole string. Merging reduces sub-pixel rendering
  # differences at the span boundaries.
  %r{<span class="sh">(['"])</span><span class="s">([^<]*)</span><span class="sh">(['"])</span>} =>
    '<span class="s">\1\2\3</span>',

  # Builtins that Rouge wrongly classifies as .nf (Function call)
  # Live colored bold/normal green like other builtins
  %r{<span class="nf">(open|raw_input)</span>} =>
    '<span class="nf" style="color: #008000;">\1</span>',

  # Comma and semicolon (.p punctuation) — live colored every `,` and `;`
  # light green. Standalone case: Rouge emits its own .p span.
  %r{<span class="p">,</span>} =>
    '<span class="p" style="color: #66cc66;">,</span>',
  %r{<span class="p">;</span>} =>
    '<span class="p" style="color: #66cc66;">;</span>',

  # Merged-punctuation case: Rouge collapses adjacent punctuation into a
  # single `.p` span like `],` `)],` `]],` `])` `]))` `();` etc — the
  # comma/semicolon inside loses its green (whole span renders black via
  # `.p`). Live emitted one span per character so each got green
  # individually. Split the span around any `,` or `;`. The replacement
  # is applied repeatedly until no more matches (greedy gsub handles
  # multiple separators in one span).
  %r{<span class="p">([^<,;]*)([,;])([^<]*)</span>} =>
    '<span class="p">\1</span>' \
    '<span class="p" style="color: #66cc66;">\2</span>' \
    '<span class="p">\3</span>',

  # Arithmetic `%` operator — Rouge tags as `.o` (operator) which my CSS
  # paints green like `=`. Live's GeSHi left arithmetic operators
  # UNWRAPPED so they inherit `.wp_syntax`'s base #110000 (essentially
  # black). Override to inherit. (Assignment `=` and comparison `==`
  # stay green — they appear in their own .o spans and live DID wrap
  # them green.)
  %r{<span class="o">(%)</span>} =>
    '<span class="o" style="color: inherit;">\1</span>',

  # Non-stdlib module names AND names not in live's GeSHi stdlib list
  # in `from X import Y` patterns. Live left these plain; my CSS colors
  # crimson via `.kn + .n`. Override back to plain (inherits #110000
  # from .wp_syntax).
  %r{<span class="n">(pysqlite2|dbapi2|win32api|ctypes|pythonapi|py_object|c_char_p)</span>} =>
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

# Bash-specific token overrides — live's GeSHi colored these but Rouge
# either leaves them plain or tags them as generic .p punctuation:
#   `/` (path separator)  → #000 bold (in plain text, not in strings)
#   `;;` (case end)       → #000 bold
BASH_TOKEN_OVERRIDES = {
  # `;;` is plain `.p` punctuation but live colored it bold black
  %r{<span class="p">;;</span>} =>
    '<span class="p" style="color: #000; font-weight: bold;">;;</span>',

  # `"$VAR"` (variable inside double-quoted string) — live wrapped the
  # WHOLE thing in one red `<span>` (string color). Rouge splits it into
  # 3 spans: s2 opening-quote / nv variable / s2 closing-quote, and my
  # CSS makes the `.nv` green. Recolor the `.nv` to red when it's
  # sandwiched between two `.s2"` quotes.
  %r{(<span class="s2">"</span>)<span class="nv">(\$\w+)</span>(<span class="s2">"</span>)} =>
    '\1<span class="nv" style="color: #ff0000;">\2</span>\3',
}.freeze

# `/` chars appear as plain text inside `<code>...</code>` of bash
# blocks. Live wraps each `/` in a bold-black span. We need to wrap them
# without affecting `/` inside string spans (where they're part of the
# string content). Match plain text segments between </span> or <code>
# and <span> or </code>, wrap `/` chars inside those segments.
BASH_PLAIN_SEGMENT_RE = %r{
  (>)                       # close of preceding tag (</span> or <code>)
  ([^<]*?/[^<]*?)           # plain text containing at least one /
  (?=<)                     # next opening tag
}x.freeze
SLASH_RE = %r{(/)}.freeze

Jekyll::Hooks.register %i[documents pages], :post_render do |item|
  next if item.output.nil?
  next unless item.output_ext == ".html"

  if item.output.include?("language-python")
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

    # Pre-style `.n` spans that the existing CSS would have colored crimson
    # via complex selectors. These need INLINE style to survive the strip-
    # plain-.n pass below.
    #
    # Pattern 1: `.kn + .n` — name immediately after an import keyword
    #            (e.g. `from cookielib`, `import StringIO` → cookielib/StringIO).
    item.output = item.output.gsub(
      %r{(<span class="kn">(?:from|import)</span>\s+)<span class="n">(\w+)</span>}
    ) do
      "#{Regexp.last_match(1)}<span class=\"n\" style=\"color: #dc143c;\">#{Regexp.last_match(2)}</span>"
    end
    # Pattern 2: `.n` followed by `.p .` then `.nc` (module.ClassName).
    # ONLY for known stdlib module names — Rouge incorrectly tags any
    # capitalized identifier as `.nc`, so a method call like
    # `key.Close()` matches `.n + .p + .nc` and would mis-color `key`
    # crimson if we matched broadly. Live's GeSHi only colored true
    # module→Class chains (e.g. `ConfigParser.ConfigParser`,
    # `cookielib.MozillaCookieJar`); object.method() stayed plain.
    item.output = item.output.gsub(
      %r{<span class="n">(ConfigParser|StringIO|cookielib|cStringIO|pysqlite2)</span>(<span class="p">\.</span><span class="nc"[^>]*>)}
    ) do
      "<span class=\"n\" style=\"color: #dc143c;\">#{Regexp.last_match(1)}</span>#{Regexp.last_match(2)}"
    end

    # Strip remaining PLAIN `.n` spans (those with no inline style — Rouge's
    # generic Name tag on every variable, attribute, parameter). Live's
    # GeSHi left these UNWRAPPED so the inherited `.wp_syntax` color
    # (#110000) applied directly. The wrapper spans cause sub-pixel anti-
    # aliasing drift at every character boundary. Removing them lets
    # Chromium raster contiguous text runs the same way live does. Pre-
    # styled `.n` spans (with inline `style="color: ..."`) survive
    # untouched since their attribute set differs from the bare pattern.
    item.output = item.output.gsub(
      %r{<span class="n">([^<]*)</span>}, '\1'
    )
  end

  if item.output.include?("language-bash")
    BASH_TOKEN_OVERRIDES.each do |pattern, replacement|
      item.output = item.output.gsub(pattern, replacement)
    end

    # Wrap `/` chars in plain-text segments of .language-bash code
    # blocks. The whole block: `<div class="language-bash highlighter-
    # rouge"><div class="highlight"><pre class="highlight"><code>...
    # </code></pre></div></div>`. Inside the `<code>...</code>` body,
    # tokens are wrapped in `<span class="...">...</span>` and plain
    # text (whitespace, paths, etc) sits between them. Only those plain
    # segments need the `/` wrap.
    item.output = item.output.gsub(
      %r{<div class="language-bash highlighter-rouge">.*?</div>\s*</div>}m
    ) do |bash_block|
      # Within each bash block, find plain-text segments OUTSIDE any
      # span. Use `</span>` (close of previous span) or `<code>` as the
      # prefix anchor, so we don't accidentally process text INSIDE
      # `<span class="c">comment text</span>` (where live didn't wrap
      # the path slashes).
      bash_block.gsub(%r{(</span>|<code>)([^<]+?)(?=<|</code>)}) do
        prefix = Regexp.last_match(1)
        segment = Regexp.last_match(2)
        # Wrap every `/` in the segment with the styled span
        wrapped = segment.gsub(
          '/',
          '<span style="color: #000; font-weight: bold;">/</span>'
        )
        "#{prefix}#{wrapped}"
      end
    end
  end
end
