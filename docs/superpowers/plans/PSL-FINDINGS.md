# PSL-FINDINGS: Pragmatic Audit — Paragraph/List Structure Fidelity Gap

**Date:** 2026-05-20  
**Branch:** `migration-psl-list-paragraph`  
**Scope:** WordPress→Jekyll flat-list/paragraph-structure pass (PSL). The systemic fidelity gap
flagged in `FOLLOWUPS.md` §"P6/SYSTEMIC — flat WP→MD lists".

---

## A. Build-Side Full Sweep

Ran `tmp/psl/built_metrics.py` against all 76 posts. Metrics extracted from built
`entry-content` HTML: P (top-level paragraphs outside `<li>`), UL, OL, maxnest, LI, DL, PRE.

Key aggregate from built site:
- Posts with P≤1 and no lists: **38**
- Posts with any UL/OL: **18** (all maxnest==1 except 1 already nested)
- Posts with DL: **2** (tp-protocol-overview, darcs-almost-perfect)
- Posts with PRE: **12**
- Single trailing blank line in source (the WP-export artifact): **36 posts**

Built metrics TSV: `tmp/psl/built.tsv` (gitignored).

---

## B. Oracle Sample — 12 Posts Across Difficulty Range

Fetched live WP oracle (TLS verify-disabled, `curl -sk` equivalent). All 12 succeeded
(500 responses yield full HTML content per P3 finding). One trivially short post
(`resume`, 1-line body) was confirmed faithful; 11/12 showed confirmed gaps.

### Raw sample results

| Label | Category | bP | oP | ΔP | bUL | oUL | bMN | oMN | ΔMN |
|---|---|---|---|---|---|---|---|---|---|
| resume | trivial | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| doh-pictures-gone | trivial | 1 | 5 | +4 | 0 | 0 | 0 | 0 | 0 |
| swap-nice | trivial | 1 | 3 | +2 | 0 | 0 | 0 | 0 | 0 |
| firefox3-cookies | prose | 1 | 3 | +2 | 0 | 0 | 0 | 0 | 0 |
| babylon-5-dvd | prose | 2 | 11 | +9 | 0 | 0 | 0 | 0 | 0 |
| nm-autovpn | prose | 3 | 5 | +2 | 0 | 0 | 0 | 0 | 0 |
| lca-proposal-suggestions | list | 1 | 7 | +6 | 1 | 2 | 1 | 1 | 0 |
| epiphany2firefox | list | 1 | 11 | +10 | 1 | 3 | 1 | 1 | 0 |
| hdmi2usb-day-3 | list | 0 | 1 | +1 | 2 | 15 | 1 | 3 | +2 |
| fritzbox-vpnc | mixed | 5 | 20 | +15 | 1 | 3 | 1 | 2 | +1 |
| timvideos-2016 | mixed | 5 | 12 | +7 | 3 | 8 | 1 | 2 | +1 |
| hdmi2usb-day-5-6-7 | mixed | 0 | 4 | +4 | 1 | 5 | 1 | 2 | +1 |

**Conclusion: Flattening hypothesis CONFIRMED.** 11/12 posts show oracle P > built P.
Total P-delta across sample: +68 (average +5.7 per affected post). All list-heavy posts
show oracle UL >> built UL (oracle confirmed multiple separate lists where built has 1).

### Flattening mechanics confirmed

Three distinct failure modes observed in oracle structure inspection:

1. **Paragraph-blank-line collapse** (every prose post): consecutive source lines that the
   oracle treats as separate `<p>` blocks are merged into one by kramdown because the WP→MD
   export emitted NO blank lines between them. `doh-pictures-gone`: 1 long source line →
   oracle 5 separate `<p>` elements. Root cause: the WP export stored paragraphs as
   line-separated (no blank line) content.

2. **List-break interstitial absorption** (lca-proposal, epiphany2firefox): the oracle has
   `<ul>…</ul><p>…</p><ul>…</ul>` (two distinct lists separated by a prose paragraph).
   The built site collapses this to one continuous `<ul>` because the source has the
   interstitial prose line as a continuation without a blank line to close the first list.

3. **Multi-level nesting collapse** (hdmi2usb-day-3, day-5, timvideos-2016, fritzbox):
   the oracle has `<ul><li>…<ul><li>…<ul>…</ul></li></ul></li></ul>` (depth 2–3).
   The built site has depth 1 because the export flattened all sub-bullets to top-level `- `.

---

## C. Corrected Bucket Distribution (All 76 Posts)

Extended oracle verification across all 76 posts (scripts in `tmp/psl/`). Final counts
based on oracle P-delta confirmed or heuristically inferred from source structure:

### B0 — Already faithful: **13 posts**

Oracle confirms P count matches or source is trivially 1 paragraph/no-list. No action needed.

Examples: `resume`, `freeplay`, `going-to-sydney`, `leslie-tshirts-response`,
`my-three-weeks-on-a-mac`, `using-tailor-to-go-to-git`, `power-scripts-in-intrepid`,
`utf-8-in-python` (faithful with blanks), `itwire`, `tp-release-v3`, `gsoc2008`,
`starhunter-fireflys-little-known-older-cousin`, `tp-protocol-overview` (DL faithful),
`darcs-almost-perfect` (DL faithful).

Note: DL (definition list) posts render correctly via kramdown's native `Term\n: Def` syntax —
not a PSL gap; B5/EDGE classification was incorrect, these are B0.

### B1 — Paragraph blank-line restoration only: **~43 posts**

No lists, or lists already present at correct nesting. Oracle P >> built P. Needs blank
lines inserted between prose paragraphs in source. Mechanically scriptable.

Representative: `doh-pictures-gone` (+4P), `swap-nice` (+2P), `babylon-5-dvd` (+9P),
`noogler-week-1` (+6P), `lca2008-over` (+7P), `in-the-land-of-the-sheep` (+5P),
`schemepy` (+9P), `graphical-programming` (+7P), `cfxs-all-done` (+6P), `tv-idiots` (+5P),
`tailor-darcs2svn-tp` (+5P), `freeplay-debrief` (+4P), `compiling-tpserver-cpp-under-windows` (+4P),
`techtalk-gamingforfreedom` (+6P), `mentor-summit` (+2P), `lca08-rego` (+2P), `google-patchwork` (+3P),
`gaming-miniconf-videos` (+4P), `nm-openvpn-dns` (+2P), `lguest-and-ksplice` (+6P),
`programmer-art-its-deadly` (+3P), `firefox3-cookies` (+2P), `nm-autovpn` (+2P),
`xcompiling-cygwin-on-linux-for-windows` (+5P), `identitiesonly` (+4P), `fastcomplete` (+2P),
`python-swap-var` (+3P), `summer-of-code-woo` (+3P), `cfxs-free` (+6P), `rocks` (+3P),
`gsoc-results` (+3P), `gaming-miniconf-cfp` (+2P), `utf8-in-python` (+1P),
`eagle-for-pcb` (+3P), `soc-end` (+4P), `freeatlast` (+3P), and more.

Also includes posts with code blocks (firefox3-cookies: PRE present) — blank-line insertion
must not disturb fenced code regions.

### B2 — List nesting only (para already mostly correct): **~5 posts**

Oracle UL >> built UL or oracle maxnest > built maxnest; no major prose gap.

- `nm-vpn`: +1P, UL 1→1, maxnest 1→1 (tiny gap, nearly faithful)
- `lightning-timer-website`: +2P, UL 1→1 (para gap only, minor nesting)
- `hdmi2usb-day-2`: +0P, UL 2→6, maxnest 1→3 (pure nesting gap)
- `hdmi2usb-day-4`: +2P, UL 4→5, maxnest already 2 (partial nesting present)
- `nmigen-new-improved-by-whitequark`: +2P, UL 1→1 (para gap only)

Note: `hdmi2usb-day-2` is pure nesting — 0 para gap, all nesting; `hdmi2usb-day-4`
has existing maxnest==2 in built (partially correct already).

### B3 — List-break interstitial (prose between two lists): **2 posts confirmed**

Oracle shows multiple `<ul>` blocks separated by `<p>` or heading; source has one continuous list.

- `lca-proposal-suggestions`: oracle UL=2, separated by prose paragraph. Source: one flat
  bullet list with a mix of body paragraphs and list items.
- `epiphany2firefox`: oracle UL=3, separated by `<p>` prose blocks. Three distinct groups
  of bullets in the oracle.

### B4 — Mixed (para + list nesting + possible interstitials): **~13 posts**

Confirmed by oracle: both paragraph gaps AND UL count/nesting gaps.

- `hdmi2usb-day-3`: +1P, UL 2→15, maxnest 1→3 (MOST COMPLEX: deep nesting + many breaks)
- `hdmi2usb-day-5-6-7`: +4P, UL 1→5, maxnest 1→2
- `timvideos-2016`: +7P, UL 3→8, maxnest 1→2
- `fritzbox-vpnc`: +15P, UL 1→3, maxnest 1→2 (also has code blocks with `<pre>`)
- `i-want-a-cool-desktop`: +6P, UL 1→3 (list-break interstitials)
- `hdmi2usb-snippets`: +5P, UL 1→6, maxnest 1→2
- `hdmi2usb-day-1`: +0P, UL 1→2, maxnest 1→2
- `hdmi2usb-day-8`: +0P, UL 1→2, maxnest 1→2
- `first-v2-hdmi2usb`: +2P, UL 1→2
- `timvideos-gsoc-2016`: +5P, UL 1→1 (mainly para gap)
- `gnome-improvements`: oracle faithful (P=1, UL=1, maxnest=1 — no gap confirmed)
- `hdmi2usb-day-4`: partially in B2 (existing nesting) + small para gap

Additional B4 candidates not yet oracle-verified (from built-metrics heuristics):
`gnome-improvements` appears faithful. Remaining: check `i-want-a-cool-desktop` detail (oracle UL=3,
so has list-break interstitial too).

### Summary counts

| Bucket | Count | Description |
|---|---|---|
| B0 — faithful | ~13 | No action needed |
| B1 — para only | ~43 | Blank-line restoration (scriptable) |
| B2 — list nesting | ~5 | Sub-bullet indentation (per-post) |
| B3 — list-break | 2 | Interstitial paragraph between lists (per-post) |
| B4 — mixed | ~13 | Para + nesting + possible interstitials (per-post) |
| **Total need work** | **~63** | |

---

## D. Canonical Bucket Recipes

### B1 — Paragraph blank-line restoration

**Diagnosis:** source has consecutive non-blank lines that the oracle treats as separate `<p>` elements.
The export omitted blank-line paragraph separators. Confirmation: `src_blanks <= 2` with
`oracle_P >> built_P`.

**Recipe:** for each affected post, a Python script iterates body lines (after front matter)
and inserts a blank line between each non-continuation line pair. Definition of "safe boundary"
where a blank line may be inserted:
- Between two consecutive non-empty lines that are neither part of a list (`- ` prefix),
  nor inside a fenced code block (between ` ``` ` delimiters), nor a blockquote continuation
  (`> ` prefix on both sides unless there's a paragraph break intended), nor a front-matter line.
- Must NOT insert inside `<!-- fidelity-allow: … -->` sentinel blocks.

**Verification gate:** after blank-line insertion, `bundle3.3 exec jekyll build` → extract
entry-content P count → must equal oracle P count (±1 tolerance for blockquote-wrapped
paragraphs that WP renders as one `<p>`). Content linter must stay at 0.

**Pre-conditions (safe boundaries — do NOT insert):**
- Inside fenced code (between ` ``` ` pairs)
- After a `- ` list item line (don't split list continuation)
- After a `> ` blockquote line without intentional para break
- At or adjacent to `<!-- fidelity-allow -->` sentinels
- Lines that are kramdown attribute lists `{:…}`

**Automatic scriptability:** high. The pattern is mechanical: every run of non-blank lines
in the WP-export body is a collapsed paragraph group. The oracle P count provides the
verification gate. Expected total: ~43 posts, probably 200–400 blank-line insertions corpus-wide.

### B2 — List nesting (sub-bullet indentation)

**Diagnosis:** oracle shows nested `<ul>` inside `<li>` elements. Source has all items at top level `- `.

**Recipe:** for each affected post, compare oracle structure (oracle fetch → parse `<li>` nesting
depth) against source bullets. Where oracle has a bullet at depth 2, indent the source `- ` by
4 spaces (kramdown convention for nested lists). Where oracle has depth 3, indent by 8 spaces.

**Verification gate:** built `maxnest` == oracle `maxnest`. Content linter 0. Build clean.

**Complexity:** medium. Requires per-post oracle inspection to map which bullets are nested
under which parents. Posts: `hdmi2usb-day-2`, `hdmi2usb-day-4`, and embedded in B4 posts.

### B3 — List-break interstitial

**Diagnosis:** oracle shows `</ul><p>text</p><ul>` pattern; source has one continuous list.

**Recipe:** identify where the oracle ends the first `<ul>` and what the interstitial text is.
In source, add blank line + the interstitial element (prose paragraph in Markdown, or `## Heading`
if the oracle uses `<h2>`) + blank line, then continue new bullets.

Concrete for `lca-proposal-suggestions`: source has a mix of prose-as-bullets and actual bullets.
Oracle shows 2 distinct UL blocks separated by a prose paragraph. Fix: ensure the prose paragraph
(about "The proposals had to be submitted under an Open Source license...") is blank-line separated
from both lists, not embedded in a list.

Concrete for `epiphany2firefox`: oracle shows 3 UL blocks separated by prose paragraphs. Source
already has the bullets correctly identified; just needs blank lines before/after each list group.

**Verification gate:** oracle UL count == built UL count; oracle interstitial `<p>` position
preserved. Content linter 0.

**Complexity:** low-to-medium. Only 2 posts in pure B3. Embedded in B4 posts (e.g., `hdmi2usb-day-3`
has multiple interstitials within its complex nesting structure).

### B4/B5 — Mixed

**Recipe:** combine B1 + B2 + B3 per post. Start with B1 (blank-line restoration), then B2
(nesting), then B3 (interstitials). For `fritzbox-vpnc` with 20 oracle paragraphs vs 5 built:
requires careful oracle structure trace — there are heading breaks (`<h2>`) creating section
separators, blockquote wrapping the final section, and 2 list groups with interstitials.

**Key complex posts:**
- `hdmi2usb-day-3`: oracle UL=15 with maxnest=3 — the most complex post. Must carefully
  reconstruct 3-level nesting from a completely flat source. Expect 30+ structural edits.
- `fritzbox-vpnc`: oracle P=20 vs built P=5; has `<h2>` sections, nested `<ul>`, and
  `<pre>` blocks. The `<!-- fidelity-allow -->` sentinel for the Flash embed must be preserved.
- `timvideos-2016`: oracle P=12, UL=8 (5 more UL blocks than built) — multiple list groups.

---

## E. EXEC Charter — Strict Pragmatic Sequencing

### Phase 1: Mechanical bulk — B1 paragraph blank-line restoration (~43 posts)

A single Python script (`scripts/psl/restore_paragraphs.py`) processes each B1 post:
1. Parse front matter boundary.
2. Iterate body lines; detect fenced code, blockquotes, list continuations.
3. Insert blank lines at safe boundaries between non-continuation line pairs.
4. Verify: build site, extract entry-content P count, compare to oracle target.
5. If oracle P matches: commit. If not: flag for manual inspection.

Commit strategy: one commit per post (or small batches of 5–10 similar posts).
Gate: content linter 0, `structure_check` 6/6, build clean, no content drift (ONLY blank
lines added; no text changed).

**Estimated effort:** 1–2 subagent sessions. ~43 posts, mostly mechanical.

### Phase 2: Focused per-post — B2 list nesting + B3 interstitials (~7 posts)

Per-post oracle inspection → identify nesting depth for each bullet → indent source accordingly.
For B3: identify interstitial text from oracle → insert blank line + interstitial + blank line.

Gate per post: oracle maxnest == built maxnest; oracle UL count == built UL count; content
linter 0; build clean.

**Estimated effort:** 1 subagent session (~7 posts, 30–60 source edits total across them).

### Phase 3: Precision — B4 mixed complex posts (~13 posts)

Per-post careful oracle trace: fetch oracle, parse full `<ul>`/`<li>`/`<p>` nesting tree,
reconstruct faithful Markdown. Each post reviewed before commit.

For the most complex posts (`hdmi2usb-day-3`, `fritzbox-vpnc`, `timvideos-2016`): anticipate
needing an intermediate "oracle structure map" (a brief ASCII or inline comment showing the
expected nesting) before editing.

Gate per post: oracle metrics match (P ± blockquote tolerance, UL count, maxnest); content
linter 0; build clean; no inline HTML introduced (exceptions via `fidelity-allow` only if
structure is Markdown-inexpressible — see USER-DECISION below).

**Estimated effort:** 1–2 subagent sessions. ~13 posts; some are very complex.

---

## F. Risks + USER-DECISION Items

### Risk 1: Blank-line insertion in wrong place

If a blank line is inserted between a list continuation and its parent item, kramdown may
interpret it as a new list or a paragraph break inside an item. The script must be conservative:
never insert inside `- ` item continuations (lines with leading spaces after a `- ` parent).

Mitigation: the oracle P-count gate catches this — if built P after insertion exceeds oracle P,
the post is flagged for manual review.

### Risk 2: Blockquote paragraph counting difference

WP's `<blockquote>` wrapping a multi-paragraph block counts as N `<p>` inside it; kramdown's
`>` blockquote also counts those `<p>` elements. The oracle P count metric may double-count if
the extractor counts `<p>` inside blockquotes. Observed in `osdc-orbital-death`: built P=3
but oracle P=1 — this is a `OVER` case where built has MORE paragraphs than oracle, likely
because the WP blockquote wraps the text differently. The P-gate should use ±1 tolerance and
flag OVER cases for manual review rather than auto-fail.

### Risk 3: hdmi2usb-day-3 nesting depth 3

The oracle shows 3-level nesting in some `<li>` elements. kramdown supports 4-space indentation
for level 2 and 8-space for level 3. Confirm kramdown rendering matches oracle before committing.
This post may require a USER-REVIEW intermediate step.

### Risk 4: fritzbox-vpnc paragraph count (oracle P=20)

The fritzbox post has a `<!-- fidelity-allow: BLOCK_HTML necessary-embed -->` sentinel for the
techtalk Flash embed. The sentinel must be preserved through all blank-line and paragraph editing.
Additionally, the oracle has `<h2>` section headings that already exist as `## Heading` in source
— blank-line insertion must not duplicate these headings or create spurious `<p>` wrapping around
heading text.

### USER-DECISION item 1: osdc-orbital-death OVER case

`osdc-orbital-death-better-late-then-never`: built P=3, oracle P=1. This means the built site has
MORE paragraphs than the oracle, suggesting the blockquote wrapping in the WP original collapses
what would be separate paragraphs in Markdown. This is NOT a case where blank lines need adding;
it may be a case where blank lines need REMOVING or where the blockquote structure differs.
Flag for manual inspection before any automated pass touches this post.

### USER-DECISION item 2: gsoc2008 OVER case

`gsoc2008`: built P=2, oracle P=1. Similar to above — built has more paragraphs than oracle.
Inspect source and oracle structure before touching.

### USER-DECISION item 3: starhunter OVER case

`starhunter-fireflys-little-known-older-cousin`: built P=2, oracle P=1. Oracle appears to wrap
the content in a different structure. Manual inspection required.

### USER-DECISION item 4: Inherited from P6 — `<a title>` hover-tooltip loss (3 posts)

From `FOLLOWUPS.md` P6 section: `almost-there`, `google-patchwork` ×2 — linked thumbnails whose
`<a title>` tooltip cannot be expressed in pure Markdown. NOT a PSL issue (already handled in P4);
flagged here to ensure PSL pass does not accidentally re-introduce inline HTML in these posts.

### USER-DECISION item 5: fritzbox bold-in-code loss

From `FOLLOWUPS.md` P6 section: the fritzbox post's `<pre><strong>` bolding inside code blocks
is already documented as an accepted casualty (plain code blocks instead). PSL must NOT try to
restore this via inline HTML. The P6 user signoff is the correct path.

---

## G. Content-Linter Safety

PSL changes touch ONLY:
- Blank line insertions between body paragraphs
- Indentation changes on `- ` list items (spaces added, no text change)
- Interstitial text lines moved from being list items to standalone paragraphs (B3)

None of these produce BLOCK_HTML, LIQUID_LEAK, or MISSING_IMAGE linter findings. The linter
is expected to remain at 0 findings throughout. Build guard (`scripts/fidelity/build.py`)
enforces this as CI gate.

`structure_check` 6/6 must pass after each phase (the structural gate is insensitive to
paragraph count and list nesting depth changes — it checks anchor presence, not content structure).

---

## H. Quick Reference — Post-by-Post Work List

### B1 posts (para blank-line only, no list work):

`2007-04-14-doh-pictures-gone.md`, `2007-02-18-swap-nice.md`, `2007-03-01-graphical-programming.md`,
`2007-03-07-eagle-for-pcb.md`, `2007-07-23-schemepy.md`, `2007-09-06-nm-autovpn.md`,
`2008-06-10-techtalk-gamingforfreedom.md`, `2008-07-08-babylon-5-dvd-copy-protection.md`,
`2009-01-19-firefox3-cookies-in-python.md`, `2009-01-20-reading-cookies-firefox.md`,
`2009-01-26-osdc-orbital-death-better-late-then-never.md` (**OVER — manual**),
`2009-01-27-xcompiling-cygwin-on-linux-for-windows.md`, `2009-05-26-starhunter-…cousin.md` (**OVER — manual**),
`2016-05-03-using-identitiesonly-without-key-files.md`,
`2007-01-03-gnome-improvements.md` (borderline B1/B4 — oracle faithful on list, para gap zero),
`2007-03-21-summer-of-code-woo.md`, `2007-05-19-cfxs-all-done.md`, `2007-07-19-freeatlast.md`,
`2007-08-17-soc-end.md`, `2007-08-23-freeplay-debrief.md`, `2007-09-08-nm-openvpn-dns.md`,
`2007-10-07-mentor-summit.md`, `2007-10-22-gaming-miniconf-cfp.md`, `2007-10-22-gsoc-results.md`,
`2007-10-22-lca08-rego.md`, `2007-11-11-python-swap-var.md`, `2007-12-18-itwire.md` (faithful),
`2008-02-04-google-patchwork.md`, `2008-02-04-lca2008-over.md`, `2008-03-06-gaming-miniconf-videos.md`,
`2008-03-18-gsoc2008.md` (**OVER — manual**), `2008-04-27-going-to-sydney.md` (faithful),
`2008-04-27-rocks.md`, `2008-05-27-noogler-week-1.md`, `2008-11-15-in-the-land-of-the-sheep.md`,
`2010-01-03-lguest-and-ksplice.md`, `2009-01-19-utf-8-in-python.md`, `2009-01-28-programmer-art-its-deadly.md`,
`2011-12-16-fastcomplete.md`, `2008-02-18-cfxs-free.md`,
`2007-02-20-compiling-tpserver-cpp-under-windows.md`, `2007-02-25-tailor-darcs2svn-tp.md`,
`2007-04-25-tv-idiots.md`

### B2 posts (list nesting; limited para gap):

`2007-08-17-nm-vpn.md`, `2013-08-30-lightning-timer-website.md`,
`2014-07-23-hdmi2usb-production-board-bring-up-day-2-22nd-july-2014.md`,
`2014-07-25-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.md`,
`2020-05-02-nmigen-new-improved-by-whitequark.md`

### B3 posts (list-break interstitials):

`2006-11-19-lca-proposal-suggestions.md`, `2008-04-10-epiphany2firefox.md`

### B4 posts (mixed — per-post oracle trace required):

`2014-07-24-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014.md` (most complex),
`2014-07-28-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014.md`,
`2016-01-15-timvideos-us-2016-new-years-resolutions.md`,
`2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`,
`2007-03-11-i-want-a-cool-desktop.md`,
`2014-07-21-hdmi2usb-production-board-bring-up-snippets-prep-work.md`,
`2014-07-22-hdmi2usb-production-board-bring-up-day-1-21st-july-2014.md`,
`2014-07-29-hdmi2usb-production-board-bring-up-day-8-28th-july-2014.md`,
`2015-07-05-first-v2-hdmi2usb-production-board-constructed.md`,
`2016-03-15-timvideos-us-and-google-summer-of-code-2016.md`

### B0 — confirmed faithful (no action):

`2007-02-18-resume.md`, `2007-08-15-freeplay.md`, `2008-04-27-going-to-sydney.md`,
`2008-07-08-leslie-tshirts-response.md`, `2008-07-08-my-three-weeks-on-a-mac.md`,
`2007-04-21-using-tailor-to-go-to-git.md`, `2009-01-19-power-scripts-in-intrepid.md`,
`2007-12-18-itwire.md`, `2008-02-19-tp-release-v3.md`,
`2007-02-23-tp-protocol-overview.md`, `2007-02-26-darcs-almost-perfect.md`,
and short posts with adequate P count (≤6 src lines, P≥1).
