# P2-FINDINGS — triaged authoritative content-finding worklist (keystone)

> Output of P2 Task 1. Drives all P2 remediation (Tasks 2…N). Data-driven; do
> not start remediation without this. Regenerated authoritatively on
> 2026-05-19 from the worktree (`migration-p2-content-fidelity`, P0+P1 merged).

## 1. Authoritative linter output (regenerated, verbatim)

`tmp/p2_lint.py` → `lint_paths(sorted(glob('_posts/*.md')), asset_root='.')`
(`uv run python tmp/p2_lint.py`; script deleted after capture):

```
47 findings
Counter({'BLOCK_HTML': 25, 'LIQUID_LEAK': 11, 'MISSING_IMAGE': 11})
```

**No drift from the P0-era count** (47: 25 BLOCK_HTML / 11 LIQUID_LEAK / 11
MISSING_IMAGE). Spans **18 distinct posts**. Full line-numbered list is in §4.

## 2. Method & fidelity oracle

Every finding mapped to its exact source line + a pattern bucket
(`tmp/map_findings.py`). For every ambiguous pattern the **fidelity oracle** was
consulted — original rendered post via `wordpress_url` front matter, Python
`urllib` + unverified SSL context (cert expired), descriptive UA, `div.entry-content`
extraction (`tmp/oracle.py`). Fallback order: **live → Wayback → git history**.

Oracle results:
- **Live site (primary):** SUCCESS for `darcs-almost-perfect`, `almost-there`,
  `techtalk-gamingforfreedom`, `cfxs-free`, `hdmi2usb…day-2`,
  `connecting-to-a-fritzbox`. These cover **every BLOCK_HTML/relurl pattern**
  (mangled `<dl>`, `<pre>` code blocks, nested `<ul><li>`, the `<object><embed>`
  Flash embed, the rendered `<img>`, and absence-of-comment-`<style>`).
- **Live 500 → Wayback 429 (rate-limited):** `python-swap-var`,
  `reading-cookies-firefox`, `osdc-orbital-death`. Resolved via the **git-history
  oracle**: `git show b1ad5c2:…` + `git log -S` proved the `<style>`
  comment-CSS block was injected by commit **`8a6c3f9` "Add pagination support
  and homepage layout" (2025-07-08)** — a Jekyll-era migration commit, *never*
  in the original WordPress body (and predating the "Convert … to pure Markdown"
  commit `b1ad5c2`). The remaining patterns in these posts are byte-identical to
  oracle-confirmed siblings (same injected `.comments{…}` CSS).
- **No post was left unresolved.** The three live-500 posts only carry the
  STYLE_COMMENT_CSS pattern (+ a `> ` blockquote-code artifact, not flagged),
  which the git oracle resolves definitively, so no conservative
  "manual-review" fallback was needed.

Cross-checked against `P0-RESULTS.md` §"Content linter = P2 worklist": the
per-post code distribution matches exactly, and P0 already characterized the
MISSING_IMAGE findings as "`{{ ` artifacts secondary to a LIQUID_LEAK on the
same line — they disappear once the Liquid leak is fixed."

## 3. Pattern buckets, classification & evidence

All 47 findings fall into **7 patterns**. Classes: **R** real defect,
**F-norm** FP→fence, **F-lint** linter-fault, **N** necessary HTML.

### 3.1 RELURL_LIQUID — 11 × `LIQUID_LEAK` — class **R-P4 (deferred to P4)**

Lines of the form `… src="{{ '/assets/…' | relative_url }}" …` or
`[…]({{ '/assets/…' | relative_url }})`. **Not a leak**: this is *valid working
Jekyll Liquid* (the `relative_url` filter), rendering a correct baseurl-prefixed
`/assets/…` URL TODAY; all 13 occurrences / 12 unique asset paths **exist on
disk** (`tmp/imgcheck.py`, `EXISTS=True` for every one); 0 non-`relative_url`
`{{`/`{%` exist anywhere in the flagged corpus.

Why **R** (real defect) and not F-lint (linter refinement): the spec mandates
posts be **pure Markdown** (commit `b1ad5c2` goal; spec §7 "posts stay
Markdown… no structural/layout HTML… no theme chrome"; the `{{`/`{%`-in-posts
rule is the deliberate P5 build-guard). The Liquid was a *partial pre-completion
fix* (commit `2022316` "Fix asset URLs in posts to use relative_url filter
(partial fix)"). Once P4 sets `baseurl: ""`, `{{ '/assets/x' | relative_url }}`
≡ literal `/assets/x` — **removing the Liquid for the plain path is then
zero-fidelity-loss and is the spec-compliant faithful remediation**.

**CRITICAL — WHY THESE ARE P4-COUPLED, NOT REMEDIATED IN P2:**
`_config.yml` currently has `baseurl: "/blog.mithis.net"` (P4 has not yet run).
kramdown does NOT prepend `baseurl` to Markdown image/link paths — it is a
Jekyll server-level routing prefix, not a string prepended to literal paths.
Therefore, replacing `{{ '/assets/x' | relative_url }}` with plain `/assets/x`
NOW would render WITHOUT the baseurl prefix: `<img src="/assets/x">` instead of
the correct `<img src="/blog.mithis.net/assets/x">`, **breaking image URLs on
the current deployment**. There is no pure-Markdown form that is BOTH no-Liquid
AND baseurl-correct under a non-empty baseurl.

These 22 findings (11 LIQUID_LEAK + 11 co-located MISSING_IMAGE) are therefore
class **R-P4**: real defects confirmed (the spec forbids Liquid in post bodies),
but **deferred to P4** because the faithful, correct remediation — replacing the
Liquid with plain `/assets/…` paths — is only correct once P4 sets `baseurl: ""`.
**P2 must NOT touch these lines.** P4 will: set `baseurl:""`+CNAME (its core
job), THEN strip the now-redundant `relative_url` Liquid → plain `/assets/…` in
those ~12 post image lines, THEN run the final post-corpus linter-0 gate.

The linter is *correctly* enforcing the rule; the content genuinely needs the
edit — just not yet. Oracle (live) confirms the original rendered a real image
at each site (e.g. `almost-there` →
`<p align="center"><a href="…cfxs-try2.jpg"><img src="…cfxs-try2.thumbnail.jpg"/></a></p>`).

### 3.2 RELURL_IMG_ARTIFACT — 11 × `MISSING_IMAGE` — class **R-P4 (deferred to P4)**

`Local image not found: {{ ` — pure **linter artifact**: `_MD_IMG`/`_HTML_IMG`
naively extract the literal string `{{ ` as the "src" before Liquid resolves.
Every one is on the *same line* as a RELURL_LIQUID finding. Not an independent
defect: the single per-post edit that replaces the `relative_url` Liquid with
the plain `/assets/…` path removes BOTH the LIQUID_LEAK and the MISSING_IMAGE.
(Confirmed: 0 of the 13 occurrences / 12 unique asset paths are actually missing
on disk.) These co-locate 1-for-1 with their RELURL_LIQUID row and are
**deferred to P4** for the same reason (see §3.1): they auto-resolve when the
LIQUID_LEAK is fixed, but fixing the LIQUID_LEAK now would break image URLs
under the current `baseurl:"/blog.mithis.net"`. Class **R-P4** (real defect
pair, P4-coupled).

### 3.3 STYLE_COMMENT_CSS — 12 × `BLOCK_HTML` — class **R**

Open/close of an identical injected `<style>.comments{…}.comment{…}
.comment-meta{…}.comment-content{…}</style>` block in 6 posts (the 6 with
recovered `comments:` front matter). **Migration artifact**: git oracle proves
it was added by commit `8a6c3f9` (2025-07-08), never in the original WP body
(live oracle: `cfxs-free`/`hdmi2usb-day2`/`darcs`/`almost-there` show NO such
block). Spec §7 forbids structural/layout HTML & theme chrome in post bodies —
comment-rendering CSS belongs in the theme/layout, not inline in every post.
Faithful remediation = remove the block from the post body (the original never
had it; comment styling is a theme concern). NOTE for the remediator: this is a
6-post sweep; the comment *content/rendering* (the `## Comments` section + the
`comments:` front matter) is out of scope here — only the appended `<style>`
chrome is the finding. (Distinct from the *legitimate author-authored* `<style>`
in the original `fritzbox` post — that one was dropped in conversion and is NOT
in our finding list; do not confuse them.)

### 3.4 STRAY_PRE_CLOSE — 9 × `BLOCK_HTML` — class **R**

Orphan `</pre>` (sometimes mid-line, e.g. `… cfxs</pre>So why not…`) left when
WP `<pre>` code/output blocks were converted. Oracle (live) confirms the
original rendered real `<blockquote><pre>…</pre></blockquote>` code/error
blocks (`cfxs-free` → `<blockquote><pre>svn co …</pre></blockquote>`;
`hdmi2usb-day2` → two `<pre style="padding-left:30px">…</pre>` error dumps;
`fritzbox` → multiple `<code><pre>…</pre>` config templates). Faithful
remediation = reconstruct as **fenced ```` ``` ```` code blocks** (kramdown/GFM;
the linter correctly skips fences). These are genuine *defects* (not deliberate
code-example FPs) so class **R** even though the fix produces a fenced block.

**IMPORTANT — fritzbox structural note (lines 42, 64, 79, 121):** In
`_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md` the
single-backtick (`` ` ``) lines surrounding each code region are **multi-line
block code delimiters — NOT inline-code spans**. The conversion left bare `` ` ``
lines as open/close markers around each `<pre>` block. When reconstructing
fenced ```` ``` ```` blocks, the remediator MUST replace these `` ` `` delimiter
lines themselves (not treat them as inline code). Additionally, **line 121 has
the `</pre>` and the closing `` ` `` concatenated on a single line** (literal:
`` </pre>` ``) — the `</pre>` is not on its own line. Line 122 carries a stray
`> ` blockquote-marker artifact that must also be removed as part of
reconstructing that block. Target: each oracle `<pre>` block → one fenced
```` ``` ```` block with no surrounding `` ` `` lines and no `> ` artifacts.

**IMPORTANT — cfxs-free:19 structural note:** The stray `</pre>` on line 19 is
embedded on the **same line as a blockquote marker** — the source line reads:
`` > svn co http://verbal.mithis.com/svn/cfxs/trunk cfxs</pre>So why not check it out and build your own? ``
The oracle-confirmed original is `<blockquote><pre>svn co …</pre></blockquote>`
followed by plain prose. Faithful fix: **strip the leading `> ` blockquote
marker**, convert the `svn co …` command to a fenced ```` ``` ```` code block
(the command stands alone; no blockquote wrapper in Markdown), then continue
"So why not check it out and build your own?" as a **separate prose paragraph**
— NOT a blockquote wrapping a code block. Do not preserve the `> ` wrapper; the
oracle shows `<blockquote>` only as the container for the `<pre>`, not as author
commentary.

### 3.5 MANGLED_LI_CLOSE — 2 × `BLOCK_HTML` — class **R**

`</li> /li>` orphan closers (the `<` of `</ul>` eaten too) from nested
`<ul><li>` lists. Oracle (live, `hdmi2usb-day2`) confirms deeply nested
`<ul><li>…<ul>…</ul></li></ul>`. The WP→MD conversion already produced the `-`
list items; faithful remediation = delete the orphan closer lines / restore
proper Markdown nested-list indentation.

> **P2-NOW scope clarification (controller decision, 2026-05-19 — added during
> R-D execution).** Live-oracle inspection of `hdmi2usb` day-2/day-3 shows the
> originals are 3–4-level-deep nested `<ul>`s, while the WP→MD export flattened
> ALL list items to top-level `-` with no indentation across the WHOLE corpus
> (and dropped blank-line paragraph separators). That flat-vs-nested divergence
> is **valid Markdown with no raw HTML → not linter-detectable → a SYSTEMIC,
> corpus-wide structural-fidelity problem**, NOT one of the 47 findings.
> Restoring full nesting only around the finding lines would be incoherent
> (the same post has many un-nested sublists with no closer-finding) and would
> conflate two scopes. **Therefore P2-R-D's bounded scope for MANGLED_LI_CLOSE
> is: DELETE the orphan `</li> /li>` line (this removes the BLOCK_HTML raw-HTML
> finding) and DO NOT re-nest/re-indent the surrounding flat list.** The
> "restore proper Markdown nested-list indentation" half of the remediation
> above is the systemic structural-fidelity work, deferred to the dedicated
> P6/SYSTEMIC pass — see `FOLLOWUPS.md` → "P6/SYSTEMIC — flat WP→MD lists don't
> reproduce original list structure" (committed `e4e706c`). This mirrors how
> R-C deliberately left cfxs-free's systemic paragraph-joining untouched. The
> co-located `<pre>` dumps in the same posts ARE in P2 scope (raw `</pre>` is a
> finding) and are reconstructed as fenced code blocks, oracle-verbatim.

### 3.6 MANGLED_DL — 1 × `BLOCK_HTML` — class **R**

`<dl> dt>…</dt> dd>…</dd> … /dl>` (opening `<` stripped from `dt`/`dd`/`/dl`).
Oracle (live, `darcs-almost-perfect`) confirms a real
`<dl><dt>…</dt><dd>…</dd>…</dl>` 3-term definition list. Faithful remediation =
kramdown definition-list syntax (`term`\n`: definition`) — kramdown supports
this natively and renders `<dl>`, preserving the original structure.

### 3.7 FLASH_OBJECT_EMBED — 1 × `BLOCK_HTML` — class **N**

`techtalk-gamingforfreedom:22` `<object …><embed … shockwave-flash …/></object>`
— a YouTube *Flash* embed. Oracle (live) confirms the original rendered exactly
`<object><param><embed></embed></object>` (the same obsolete Flash player); the
post text says "see it below". Markdown genuinely **cannot** express an
`<object>/<embed>` → this is true **N (necessary HTML)**. Only 1 such finding
in the entire corpus.

**Concrete resolution (decided; encoded in Task L):** KEEP the `<object><embed>`
element faithful (it renders the original YouTube video; do NOT mangle to
Markdown or a fenced block). ADD an in-content `fidelity-allow` sentinel
comment immediately adjacent to the element — a standard HTML comment of the
form:

```html
<!-- fidelity-allow: BLOCK_HTML necessary-embed — YouTube; Markdown cannot express -->
```

When `lint_content` detects this sentinel on/adjacent to a BLOCK_HTML
occurrence, it does NOT emit the finding for that line. Task L implements this
minimal sentinel-allowance feature in `lint_content.py` (TDD: failing test first
— sentinel suppresses exactly that one occurrence; un-annotated block HTML still
flagged; F-lint/F-norm classes unaffected — both remain 0; all existing
`test_lint_content.py` assertions green). After P2, `lint_content` over
`_posts/*.md` reports **exactly 22** findings: only the R-P4 residuals; the 1 N
is sentinel-suppressed (not counted). The exit-gate arithmetic is coherent: the
N never inflates the residual beyond 22.

This is NOT a blanket weakening of the linter — only explicitly annotated
occurrences are suppressed. The broader F-lint/F-norm refinement remains
deferred to P5 (0 F-norm and 0 F-lint in this corpus, so P5 linter-hardening
items I3/I5/I1/I2/M1-M4 are still deferred; Task L partially advances P5 by
establishing the necessary-HTML sentinel mechanism — noted in FOLLOWUPS).

## 4. Full finding table (47 rows, line-numbered)

`path:line | code | class | original-content evidence (oracle) | planned remediation`

**Class key:** `R` = P2-NOW (real defect, fix in P2); `R-P4` = real defect, P4-COUPLED (deferred — only correct to fix after P4 sets `baseurl:""`); `N` = necessary HTML (per-case allowance in P2).

### P2-NOW findings (25 rows — P2 remediates these)

| path:line | code | class | original-content evidence (oracle source) | planned remediation |
|---|---|---|---|---|
| _posts/2007-02-26-darcs-almost-perfect.md:17 | BLOCK_HTML | R | LIVE: real `<dl><dt>×3<dd>×3</dl>` definition list | kramdown def-list (`term`/`: def`) |
| _posts/2007-09-06-nm-autovpn.md:91 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); not in original | remove injected comment-CSS `<style>` block |
| _posts/2007-09-06-nm-autovpn.md:114 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2007-11-11-python-swap-var.md:36 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2007-11-11-python-swap-var.md:59 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2008-02-18-cfxs-free.md:19 | BLOCK_HTML | R | LIVE: `<blockquote><pre>svn co …</pre></blockquote>` | fenced ``` code block; split prose off the `</pre>` line |
| _posts/2008-06-10-techtalk-gamingforfreedom.md:22 | BLOCK_HTML | N | LIVE: original rendered identical `<object><param><embed>` Flash embed | per-case justified linter-allowance (minimal embed / modern `<iframe>` 8Ct36u8RPIU) — NOT a content mangle |
| _posts/2009-01-20-reading-cookies-firefox.md:169 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2009-01-20-reading-cookies-firefox.md:192 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-01-26-osdc-orbital-death-better-late-then-never.md:32 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2009-01-26-osdc-orbital-death-better-late-then-never.md:55 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-01-27-xcompiling-cygwin-on-linux-for-windows.md:34 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9) | remove injected comment-CSS `<style>` block |
| _posts/2009-01-27-xcompiling-cygwin-on-linux-for-windows.md:57 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:30 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9) | remove injected comment-CSS `<style>` block |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:53 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:42 | BLOCK_HTML | R | LIVE: `<code><pre>…config…</pre>` | fenced ``` code block (reconstruct from the ``` ` ```-delimited region) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:64 | BLOCK_HTML | R | LIVE: `<code><pre>…config…</pre>` | fenced ``` code block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:79 | BLOCK_HTML | R | LIVE: `<pre>…vpnc.conf template…</pre>` | fenced ``` code block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:121 | BLOCK_HTML | R | LIVE: `<pre>…fritzbox-script…</pre>` | fenced ``` code block |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:34 | BLOCK_HTML | R | LIVE: nested `<ul><li>…<ul>…</ul></li></ul>` | delete orphan `</li> /li>`; restore Markdown nested-list indent |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:41 | BLOCK_HTML | R | LIVE: `<blockquote><pre style=…>…ioclk_buf…</pre>` | fenced ``` code block (error dump) |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:46 | BLOCK_HTML | R | LIVE: `<pre>…map Error 139</pre>` | fenced ``` code block (error dump) |
| _posts/2014-07-24-hdmi2usb…day-3-23rd-july-2014.md:32 | BLOCK_HTML | R | LIVE-pattern: nested `<ul><li>` (sibling post confirmed) | delete orphan `</li> /li>`; restore Markdown nested-list indent |
| _posts/2014-07-24-hdmi2usb…day-3-23rd-july-2014.md:45 | BLOCK_HTML | R | LIVE-pattern: `<pre>…xusbdfwu.rules:3'</pre>` error dump | fenced ``` code block (error dump) |
| _posts/2014-07-28-hdmi2usb…day-5-6-and-7th…july-2014.md:20 | BLOCK_HTML | R | LIVE-pattern: `<pre>ERROR:Place …ioclk_buf…</pre>` | fenced ``` code block (error line) |

### P4-COUPLED findings (22 rows — DO NOT TOUCH IN P2; deferred to P4)

> These are VALID WORKING Liquid today. Replacing with plain `/assets/…` now would break image URLs under `baseurl:"/blog.mithis.net"`. P4 will fix these after setting `baseurl:""`.

| path:line | code | class | original-content evidence (oracle source) | planned remediation (IN P4, NOT P2) |
|---|---|---|---|---|
| _posts/2007-05-09-almost-there.md:19 | LIQUID_LEAK | R-P4 | LIVE: `<p align=center><a href=cfxs-try2.jpg><img src=…thumbnail.jpg></a></p>` | P4: replace `{{…relative_url}}` w/ plain `/assets/…` linked-thumbnail after `baseurl:""` |
| _posts/2007-05-09-almost-there.md:19 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists on disk) | P4: auto-resolved by the same edit |
| _posts/2007-08-17-resume.md:18 | LIQUID_LEAK | R-P4 | LIVE n/a-needed: working PDF link; `resume.pdf` exists | P4: replace `{{…relative_url}}` w/ plain `/assets/…` md link after `baseurl:""` |
| _posts/2008-02-04-google-patchwork.md:17 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered map `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…`; fix unclosed `[` md-link |
| _posts/2008-02-04-google-patchwork.md:17 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2008-02-04-google-patchwork.md:19 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered map `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…`; fix unclosed `[` md-link |
| _posts/2008-02-04-google-patchwork.md:19 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2008-02-18-cfxs-free.md:22 | LIQUID_LEAK | R-P4 | LIVE: `<p><img src=…cfxs-try2.jpg alt=""></p>` | P4: replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2008-02-18-cfxs-free.md:22 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:22 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered screenshot `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:22 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:125 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered `VPN-error.png` `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:125 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:127 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered `VPN-encrypt.png` `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:127 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | LIQUID_LEAK | R-P4 | LIVE-pattern: two rendered photo `<img>` (files exist) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` (×2 imgs on this line) |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | MISSING_IMAGE | R-P4 | artifact (1st `{{` on the line; file exists) | P4: auto-resolved by the same edit |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | MISSING_IMAGE | R-P4 | artifact (2nd `{{` on the line; file exists) | P4: auto-resolved by the same edit |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:23 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered VGA-board photo `<img>` (file exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:23 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |
| _posts/2015-07-05-first-v2-hdmi2usb-production-board-constructed.md:17 | LIQUID_LEAK | R-P4 | LIVE-pattern: rendered board photo `<img>` (`HDMI2USB-Prod-V2…` exists) | P4: replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2015-07-05-first-v2-hdmi2usb-production-board-constructed.md:17 | MISSING_IMAGE | R-P4 | artifact of the line above (file exists) | P4: auto-resolved by the same edit |

> "LIVE-pattern" = the *pattern* (relurl `<img>` rendering / `<pre>` block /
> nested `<ul>`) was directly confirmed on the live original for at least one
> representative post of that bucket AND the file/structure is byte-consistent
> across the bucket; the specific post's image file existence was verified on
> disk (`tmp/imgcheck.py`). "GIT" = git-history oracle (commit `8a6c3f9`).

## 5. Tally

| Class | Count | Scope | Notes |
|---|---|---|---|
| **R** (real defect, P2-NOW) | **24** | P2-NOW | 12 STYLE_COMMENT_CSS + 9 STRAY_PRE_CLOSE + 2 MANGLED_LI_CLOSE + 1 MANGLED_DL — all BLOCK_HTML; no baseurl dependency |
| **R-P4** (real defect, P4-COUPLED) | **22** | DEFERRED to P4 | 11 RELURL_LIQUID + 11 RELURL_IMG_ARTIFACT — deferred because plain `/assets/…` is only correct+faithful once P4 sets `baseurl:""` |
| **F-norm** (FP → fenced) | **0** | — | no post is a *deliberate* HTML/Liquid code example mis-flagged |
| **F-lint** (linter-fault) | **0** | — | no inline-code-mid-sentence Liquid; the linter is over-flagging *nothing* |
| **N** (necessary HTML) | **1** | P2-NOW | `techtalk-gamingforfreedom:22` `<object><embed>` Flash embed (Markdown can't express; per-case justified linter-allowance) |
| **TOTAL** | **47** | | 25 P2-NOW (24 R + 1 N) + 22 R-P4 |

**P2-NOW set (25 findings — P2 remediates these):** the 24 R BLOCK_HTML
findings (injected `<style>` comment-CSS, mangled `<dl>`/`<dt>`/`<dd>`, mangled
`<li>`, stray `<pre>` closers) PLUS the 1 N (`techtalk-gamingforfreedom:22`
Flash embed — per-case justified linter-allowance). These have NO baseurl
dependency; P2 fixes them now.

**P4-COUPLED set (22 findings — DEFERRED to P4):** the 11 RELURL_LIQUID + 11
co-located RELURL_IMG_ARTIFACT findings. These are VALID WORKING Liquid
producing correct baseurl-prefixed URLs TODAY. They only become removable to
plain `/assets/…` (pure Markdown, faithful, correct) once P4 sets `baseurl:""`.
**P2 does NOT touch these lines** — touching them now would break image URLs
under the current `baseurl:"/blog.mithis.net"`.

Of the 25 P2-NOW findings, all 25 are distinct BLOCK_HTML/N rows (no
co-located auto-resolve pairs in the P2-NOW set). Real *content-edit* work in
P2 ≈ **13 commits across ~13 posts** (the BLOCK_HTML + 1 N items, grouped per
the §6 remediation plan). The 22 R-P4 findings each resolve as a co-located
LIQUID_LEAK + MISSING_IMAGE pair in P4 (~11 independent P4 edit-sites).

### Signal for Task L (linter refinement) and P2 scope

- **Task L IS required** — not for F-lint/F-norm (0 of each; linter correctly
  flags every finding), but to implement the **necessary-HTML sentinel allowance**
  for the 1 N (`techtalk-gamingforfreedom:22`). Without Task L the residual linter
  count after all P2-NOW remediation would be 23 (22 R-P4 + the unflagged-but-
  still-emitted N), breaking the exit-gate "exactly 22" assertion. Task L adds
  minimal TDD'd support for an in-content `fidelity-allow` sentinel comment
  (see §3.7) so the N is suppressed in the linter output. This is NOT a blanket
  FP refinement — un-annotated block HTML is still flagged. The FOLLOWUPS P5
  linter-hardening items I3/I5/I1/I2/M1-M4 remain deferred as before (not
  triggered by this corpus; Task L partially advances P5 by establishing the
  sentinel mechanism).
- **P2 remediation is real and bounded (P2-NOW only):** ~11 posts, ~12 faithful
  content edits, all with concrete oracle-confirmed target structures (def-list,
  fenced code, nested lists, drop injected `<style>`), plus **1 N** decision
  (Flash embed faithful-keep + Task L sentinel allowance). M1 (category links)
  and M2 (category prose) remain separate template/decision tasks per the plan.
  The 22 R-P4 findings are P4's responsibility.

## 6. Remediation plan grouped BY FILE (one commit per post)

### P2-NOW (P2 remediates these — 11 posts, BLOCK_HTML + N only)

Each post = one remediation task/commit fixing **all its P2-NOW findings**
(`P2: content fidelity — <post> (<summary>)` + Co-Authored-By trailer).
Order roughly simplest → most complex.

| # | Post (commit unit) | P2-NOW Findings | Faithful remediation (oracle-confirmed) |
|---|---|---|---|
| 1 | `2007-02-26-darcs-almost-perfect.md` | BLOCK_HTML ×1 | mangled `<dl>` → kramdown definition list (3 terms) |
| 2 | `2007-09-06-nm-autovpn.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 3 | `2007-11-11-python-swap-var.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 4 | `2008-02-18-cfxs-free.md` | BLOCK_HTML ×1 | strip `> ` blockquote marker; `svn co …` → fenced ``` code block; "So why not…" → separate prose paragraph (see §3.4 cfxs-free note) |
| 5 | `2009-01-20-reading-cookies-firefox.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 6 | `2009-01-26-osdc-orbital-death…never.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 7 | `2009-01-27-xcompiling-cygwin…windows.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 8 | `2009-05-26-starhunter-fireflys…cousin.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 9 | `2014-07-28-hdmi2usb…day-5-6-7…2014.md` | BLOCK_HTML ×1 | `</pre>` error line → fenced ``` code block |
| 10 | `2014-07-24-hdmi2usb…day-3…2014.md` | BLOCK_HTML ×2 | orphan `</li> /li>` → Markdown nested list; `</pre>` error dump → fenced ``` |
| 11 | `2014-07-23-hdmi2usb…day-2…2014.md` | BLOCK_HTML ×3 | orphan `</li> /li>` → nested list; 2× `<pre>` error dumps → fenced ``` |
| 12 | `2013-10-06-connecting-to-a-fritzbox…vpnc.md` | BLOCK_HTML ×4 | reconstruct 4× fenced ``` code blocks: replace each `` ` `` delimiter line (NOT inline code — these are block markers), the `</pre>` on the same line as the closing `` ` `` (line 121: `` </pre>` ``), and the `> ` artifact on line 122 (see §3.4 fritzbox note) |
| 13 | `2008-06-10-techtalk-gamingforfreedom.md` | BLOCK_HTML ×1 (**N**) | keep `<object><embed>` faithful (original video; NOT a Markdown conversion); add `<!-- fidelity-allow: BLOCK_HTML necessary-embed — YouTube; Markdown cannot express -->` sentinel adjacent to it; Task L implements linter suppression for the sentinel so linter shows exactly 22 R-P4 residuals |

**Verification gate per P2-NOW post:** that post's BLOCK_HTML/N linter findings
→ 0; `structure_check` still PASS (6/6); `bundle3.3 exec jekyll build` clean;
rendered `_site` output spot-matches the oracle (same headings/lists/links/code;
no broken structure); only that post changed; zero front-matter/permalink drift.
NOTE: after all P2-NOW posts are done (including the Task L sentinel
implementation for the 1 N), the linter will show **exactly 22 R-P4
findings** (LIQUID_LEAK + MISSING_IMAGE; the 1 N sentinel-suppressed) — this is
expected and correct.

### P4-COUPLED (DO NOT TOUCH IN P2 — deferred to P4)

The following posts still carry LIQUID_LEAK + MISSING_IMAGE findings after P2 is
complete. **P2 must not touch these lines.** Touching them now would break image
URLs under `baseurl:"/blog.mithis.net"`. P4 owns these.

| Post | P4-COUPLED Findings | P4 remediation (after `baseurl:""`) |
|---|---|---|
| `2007-05-09-almost-there.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain path; linked-thumbnail per original `<p align=center>` |
| `2007-08-17-resume.md` | LIQUID_LEAK ×1 | relurl→plain `/assets/…resume.pdf` md link |
| `2008-02-04-google-patchwork.md` | LIQUID_LEAK ×2 + MISSING_IMAGE ×2 | relurl→plain path ×2; repair the two unclosed `[<img …` md-links |
| `2008-02-18-cfxs-free.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain `…cfxs-try2.jpg` image |
| `2009-05-26-starhunter-fireflys…cousin.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain screenshot img |
| `2013-10-06-connecting-to-a-fritzbox…vpnc.md` | LIQUID_LEAK ×2 + MISSING_IMAGE ×2 | relurl→plain path for 2 inline `<img>` |
| `2014-07-25-hdmi2usb…day-4…2014.md` | LIQUID_LEAK ×2 + MISSING_IMAGE ×3 | relurl→plain path for all 3 photo `<img>` |
| `2015-07-05-first-v2-hdmi2usb…constructed.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain board-photo path |

**Image-asset note:** all 13 occurrences / 12 unique `relative_url` target
paths already exist under `assets/images/wp-content/uploads/...` (verified).
No MISSING_IMAGE finding requires sourcing a new asset — they all resolve once
the Liquid is removed for the plain repo path in P4. (P2 plan's "possibly add
assets" path is **not** needed for any of these findings.)
