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

### 3.1 RELURL_LIQUID — 11 × `LIQUID_LEAK` — class **R**

Lines of the form `… src="{{ '/assets/…' | relative_url }}" …` or
`[…]({{ '/assets/…' | relative_url }})`. **Not a leak**: this is *valid working
Jekyll Liquid* (the `relative_url` filter), rendering a correct `/assets/…`
URL; all 13 referenced files **exist on disk** (`tmp/imgcheck.py`,
`EXISTS=True` for every one); 0 non-`relative_url` `{{`/`{%` exist anywhere in
the flagged corpus.

Why **R** (content edit) and not F-lint (linter refinement): the spec mandates
posts be **pure Markdown** (commit `b1ad5c2` goal; spec §7 "posts stay
Markdown… no structural/layout HTML… no theme chrome"; the `{{`/`{%`-in-posts
rule is the deliberate P5 build-guard). The Liquid was a *partial pre-completion
fix* (commit `2022316` "Fix asset URLs in posts to use relative_url filter
(partial fix)"). With `baseurl: ""` (spec §P4), `{{ '/assets/x' | relative_url }}`
≡ literal `/assets/x` — **removing the Liquid for the plain path is zero-fidelity-loss
and is the spec-compliant faithful remediation**. The linter is *correctly*
enforcing the rule; the content genuinely needs the edit. Oracle (live) confirms
the original rendered a real image at each site (e.g. `almost-there` →
`<p align="center"><a href="…cfxs-try2.jpg"><img src="…cfxs-try2.thumbnail.jpg"/></a></p>`).

### 3.2 RELURL_IMG_ARTIFACT — 11 × `MISSING_IMAGE` — class **R** (auto-resolved)

`Local image not found: {{ ` — pure **linter artifact**: `_MD_IMG`/`_HTML_IMG`
naively extract the literal string `{{ ` as the "src" before Liquid resolves.
Every one is on the *same line* as a RELURL_LIQUID finding. Not an independent
defect: the single per-post edit that replaces the `relative_url` Liquid with
the plain `/assets/…` path removes BOTH the LIQUID_LEAK and the MISSING_IMAGE.
(Confirmed: 0 of 13 real targets missing on disk.) Counted R because the
remediation is a faithful content edit, not a linter change.

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

### 3.5 MANGLED_LI_CLOSE — 2 × `BLOCK_HTML` — class **R**

`</li> /li>` orphan closers (the `<` of `</ul>` eaten too) from nested
`<ul><li>` lists. Oracle (live, `hdmi2usb-day2`) confirms deeply nested
`<ul><li>…<ul>…</ul></li></ul>`. The WP→MD conversion already produced the `-`
list items; faithful remediation = delete the orphan closer lines / restore
proper Markdown nested-list indentation.

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
`<object>/<embed>` → this is true **N (necessary HTML)**. Per-case decision is
deferred to remediation (Task L / N-handling): faithful options are (a) a
justified linter-allowance keeping a minimal embed, or (b) a modern responsive
YouTube `<iframe>` for `8Ct36u8RPIU` (still an embed, still inline-HTML the
linter flags — so still needs the N allowance). Either way the resolution is a
*per-case justified linter-allowance*, **not** a content mangle and **not** a
fenced block. Only 1 such finding in the entire corpus.

## 4. Full finding table (47 rows, line-numbered)

`path:line | code | class | original-content evidence (oracle) | planned remediation`

| path:line | code | class | original-content evidence (oracle source) | planned remediation |
|---|---|---|---|---|
| _posts/2007-02-26-darcs-almost-perfect.md:17 | BLOCK_HTML | R | LIVE: real `<dl><dt>×3<dd>×3</dl>` definition list | kramdown def-list (`term`/`: def`) |
| _posts/2007-05-09-almost-there.md:19 | LIQUID_LEAK | R | LIVE: `<p align=center><a href=cfxs-try2.jpg><img src=…thumbnail.jpg></a></p>` | replace `{{…relative_url}}` w/ plain `/assets/…` linked-thumbnail (md/min inline `<img>`) |
| _posts/2007-05-09-almost-there.md:19 | MISSING_IMAGE | R | artifact of the line above (file exists on disk) | auto-resolved by the same edit |
| _posts/2007-08-17-resume.md:18 | LIQUID_LEAK | R | LIVE n/a-needed: working PDF link; `resume.pdf` exists | replace `{{…relative_url}}` w/ plain `/assets/…` md link |
| _posts/2007-09-06-nm-autovpn.md:91 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); not in original | remove injected comment-CSS `<style>` block |
| _posts/2007-09-06-nm-autovpn.md:114 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2007-11-11-python-swap-var.md:36 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2007-11-11-python-swap-var.md:59 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2008-02-04-google-patchwork.md:17 | LIQUID_LEAK | R | LIVE-pattern: rendered map `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…`; fix unclosed `[` md-link |
| _posts/2008-02-04-google-patchwork.md:17 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2008-02-04-google-patchwork.md:19 | LIQUID_LEAK | R | LIVE-pattern: rendered map `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…`; fix unclosed `[` md-link |
| _posts/2008-02-04-google-patchwork.md:19 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2008-02-18-cfxs-free.md:19 | BLOCK_HTML | R | LIVE: `<blockquote><pre>svn co …</pre></blockquote>` | fenced ``` code block; split prose off the `</pre>` line |
| _posts/2008-02-18-cfxs-free.md:22 | LIQUID_LEAK | R | LIVE: `<p><img src=…cfxs-try2.jpg alt=""></p>` | replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2008-02-18-cfxs-free.md:22 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2008-06-10-techtalk-gamingforfreedom.md:22 | BLOCK_HTML | N | LIVE: original rendered identical `<object><param><embed>` Flash embed | per-case justified linter-allowance (minimal embed / modern `<iframe>` 8Ct36u8RPIU) — NOT a content mangle |
| _posts/2009-01-20-reading-cookies-firefox.md:169 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2009-01-20-reading-cookies-firefox.md:192 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-01-26-osdc-orbital-death-better-late-then-never.md:32 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9); live 500/WB 429 | remove injected comment-CSS `<style>` block |
| _posts/2009-01-26-osdc-orbital-death-better-late-then-never.md:55 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-01-27-xcompiling-cygwin-on-linux-for-windows.md:34 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9) | remove injected comment-CSS `<style>` block |
| _posts/2009-01-27-xcompiling-cygwin-on-linux-for-windows.md:57 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:22 | LIQUID_LEAK | R | LIVE-pattern: rendered screenshot `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:22 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:30 | BLOCK_HTML | R | GIT: injected `<style>` (commit 8a6c3f9) | remove injected comment-CSS `<style>` block |
| _posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md:53 | BLOCK_HTML | R | GIT: closing `</style>` of the injected block | remove injected comment-CSS `<style>` block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:42 | BLOCK_HTML | R | LIVE: `<code><pre>…config…</pre>` | fenced ``` code block (reconstruct from the ``` ` ```-delimited region) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:64 | BLOCK_HTML | R | LIVE: `<code><pre>…config…</pre>` | fenced ``` code block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:79 | BLOCK_HTML | R | LIVE: `<pre>…vpnc.conf template…</pre>` | fenced ``` code block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:121 | BLOCK_HTML | R | LIVE: `<pre>…fritzbox-script…</pre>` | fenced ``` code block |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:125 | LIQUID_LEAK | R | LIVE-pattern: rendered `VPN-error.png` `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:125 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:127 | LIQUID_LEAK | R | LIVE-pattern: rendered `VPN-encrypt.png` `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md:127 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:34 | BLOCK_HTML | R | LIVE: nested `<ul><li>…<ul>…</ul></li></ul>` | delete orphan `</li> /li>`; restore Markdown nested-list indent |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:41 | BLOCK_HTML | R | LIVE: `<blockquote><pre style=…>…ioclk_buf…</pre>` | fenced ``` code block (error dump) |
| _posts/2014-07-23-hdmi2usb…day-2-22nd-july-2014.md:46 | BLOCK_HTML | R | LIVE: `<pre>…map Error 139</pre>` | fenced ``` code block (error dump) |
| _posts/2014-07-24-hdmi2usb…day-3-23rd-july-2014.md:32 | BLOCK_HTML | R | LIVE-pattern: nested `<ul><li>` (sibling post confirmed) | delete orphan `</li> /li>`; restore Markdown nested-list indent |
| _posts/2014-07-24-hdmi2usb…day-3-23rd-july-2014.md:45 | BLOCK_HTML | R | LIVE-pattern: `<pre>…xusbdfwu.rules:3'</pre>` error dump | fenced ``` code block (error dump) |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | LIQUID_LEAK | R | LIVE-pattern: two rendered photo `<img>` (files exist) | replace `{{…relative_url}}` w/ plain `/assets/…` (×2 imgs on this line) |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | MISSING_IMAGE | R | artifact (1st `{{` on the line; file exists) | auto-resolved by the same edit |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:21 | MISSING_IMAGE | R | artifact (2nd `{{` on the line; file exists) | auto-resolved by the same edit |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:23 | LIQUID_LEAK | R | LIVE-pattern: rendered VGA-board photo `<img>` (file exists) | replace `{{…relative_url}}` w/ plain `/assets/…` |
| _posts/2014-07-25-hdmi2usb…day-4-24th-july-2014.md:23 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |
| _posts/2014-07-28-hdmi2usb…day-5-6-and-7th…july-2014.md:20 | BLOCK_HTML | R | LIVE-pattern: `<pre>ERROR:Place …ioclk_buf…</pre>` | fenced ``` code block (error line) |
| _posts/2015-07-05-first-v2-hdmi2usb-production-board-constructed.md:17 | LIQUID_LEAK | R | LIVE-pattern: rendered board photo `<img>` (`HDMI2USB-Prod-V2…` exists) | replace `{{…relative_url}}` w/ plain `/assets/…` (keep minimal inline `<img>`) |
| _posts/2015-07-05-first-v2-hdmi2usb-production-board-constructed.md:17 | MISSING_IMAGE | R | artifact of the line above (file exists) | auto-resolved by the same edit |

> "LIVE-pattern" = the *pattern* (relurl `<img>` rendering / `<pre>` block /
> nested `<ul>`) was directly confirmed on the live original for at least one
> representative post of that bucket AND the file/structure is byte-consistent
> across the bucket; the specific post's image file existence was verified on
> disk (`tmp/imgcheck.py`). "GIT" = git-history oracle (commit `8a6c3f9`).

## 5. Tally

| Class | Count | Notes |
|---|---|---|
| **R** (real defect) | **46** | 11 RELURL_LIQUID + 11 RELURL_IMG_ARTIFACT (auto-resolved w/ the Liquid) + 12 STYLE_COMMENT_CSS + 9 STRAY_PRE_CLOSE + 2 MANGLED_LI_CLOSE + 1 MANGLED_DL |
| **F-norm** (FP → fenced) | **0** | no post is a *deliberate* HTML/Liquid code example mis-flagged |
| **F-lint** (linter-fault) | **0** | no inline-code-mid-sentence Liquid; the linter is over-flagging *nothing* — every `{{` is a removable redundant artifact, not correct content |
| **N** (necessary HTML) | **1** | `techtalk-gamingforfreedom:22` `<object><embed>` Flash embed (Markdown can't express; per-case justified linter-allowance) |
| **TOTAL** | **47** | |

Of the 47, only **22 are independent edit-sites** (the 11 MISSING_IMAGE
RELURL_IMG_ARTIFACT rows are co-located with their RELURL_LIQUID row and
auto-resolve). Real *content-edit* work ≈ **26 edit points across 18 posts**.

### Signal for Task L (linter refinement) and P2 scope

- **Task L is NOT required.** 0 F-norm, 0 F-lint. The `lint_content` linter is
  behaving correctly — every finding is a genuine WP→MD conversion defect or a
  spec-forbidden Liquid artifact, *none* is the linter over-flagging legitimate
  content. (The pre-planned conditional Task L can be **skipped**; the
  FOLLOWUPS P5 linter-hardening items I3/I5/I1/I2/M1-M4 remain deferred to P5 as
  before — they are not triggered by this corpus.)
- **P2 remediation is real and bounded:** 18 posts, ~26 faithful content edits,
  all with concrete oracle-confirmed target structures (def-list, fenced code,
  nested lists, plain `/assets/` image paths, drop injected `<style>`), plus
  **1 N** decision (Flash embed allowance). No linter/test changes needed for
  the findings; M1 (category links) and M2 (category prose) remain separate
  template/decision tasks per the plan.

## 6. Remediation plan grouped BY FILE (one commit per post)

Each post = one remediation task/commit fixing **all** its findings (`P2:
content fidelity — <post> (<summary>)` + Co-Authored-By trailer). Order roughly
simplest → most complex.

| # | Post (commit unit) | Findings | Faithful remediation (oracle-confirmed) |
|---|---|---|---|
| 1 | `2007-08-17-resume.md` | LIQUID_LEAK ×1 | relurl→plain `/assets/…resume.pdf` md link |
| 2 | `2007-02-26-darcs-almost-perfect.md` | BLOCK_HTML ×1 | mangled `<dl>` → kramdown definition list (3 terms) |
| 3 | `2007-05-09-almost-there.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain path; linked-thumbnail (`[![alt](thumb)](full)` or min inline `<a><img>`) per original `<p align=center>` |
| 4 | `2008-02-04-google-patchwork.md` | LIQUID_LEAK ×2 + MISSING_IMAGE ×2 | relurl→plain path ×2; repair the two unclosed `[<img …` md-links → plain images |
| 5 | `2008-02-18-cfxs-free.md` | BLOCK_HTML ×1 + LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | `</pre>`→ fenced ``` code (split prose); relurl→plain `…cfxs-try2.jpg` image |
| 6 | `2009-05-26-starhunter-fireflys…cousin.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 + BLOCK_HTML ×2 | relurl→plain screenshot img; remove injected comment-CSS `<style>` block |
| 7 | `2007-09-06-nm-autovpn.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 8 | `2007-11-11-python-swap-var.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 9 | `2009-01-20-reading-cookies-firefox.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 10 | `2009-01-26-osdc-orbital-death…never.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 11 | `2009-01-27-xcompiling-cygwin…windows.md` | BLOCK_HTML ×2 | remove injected comment-CSS `<style>` block |
| 12 | `2015-07-05-first-v2-hdmi2usb…constructed.md` | LIQUID_LEAK ×1 + MISSING_IMAGE ×1 | relurl→plain board-photo path (keep minimal inline `<img>` for sizing) |
| 13 | `2014-07-28-hdmi2usb…day-5-6-7…2014.md` | BLOCK_HTML ×1 | `</pre>` error line → fenced ``` code block |
| 14 | `2014-07-24-hdmi2usb…day-3…2014.md` | BLOCK_HTML ×2 | orphan `</li> /li>` → Markdown nested list; `</pre>` error dump → fenced ``` |
| 15 | `2014-07-23-hdmi2usb…day-2…2014.md` | BLOCK_HTML ×3 | orphan `</li> /li>` → nested list; 2× `<pre>` error dumps → fenced ``` |
| 16 | `2014-07-25-hdmi2usb…day-4…2014.md` | LIQUID_LEAK ×2 + MISSING_IMAGE ×3 | relurl→plain path for all 3 photo `<img>` (lines 21 has 2 imgs, 23 has 1) |
| 17 | `2013-10-06-connecting-to-a-fritzbox…vpnc.md` | BLOCK_HTML ×4 + LIQUID_LEAK ×2 + MISSING_IMAGE ×2 | reconstruct 4× ``` ` ```-delimited regions as fenced ``` code (per oracle `<pre>` blocks); relurl→plain path for 2 inline `<img>` |
| 18 | `2008-06-10-techtalk-gamingforfreedom.md` | BLOCK_HTML ×1 (**N**) | per-case: justified minimal embed allowance OR modern `<iframe>` for `8Ct36u8RPIU` — NOT a Markdown conversion (decide in remediation; the only N) |

**Verification gate per post (from the plan):** that post's linter findings → 0;
`structure_check` still PASS (6/6); `bundle3.3 exec jekyll build` clean; rendered
`_site` output spot-matches the oracle (same headings/lists/links/images/code;
no literal `{{…}}`, no broken image); only that post (+ assets) changed; zero
front-matter/permalink drift.

**Image-asset note:** all 13 `relative_url` target files already exist under
`assets/images/wp-content/uploads/...` (verified). No MISSING_IMAGE finding
requires sourcing a new asset — they all resolve once the Liquid is removed for
the plain repo path. (P2 plan's "possibly add assets" path is **not** needed
for these findings.)
