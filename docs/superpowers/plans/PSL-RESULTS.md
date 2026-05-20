# PSL — Systemic Flat-List/Paragraph-Structure Pass: RESULTS & Handoff

**Status: COMPLETE.** PSL exit gate met (§1). Branch
`migration-psl-list-paragraph`, ready to merge to `main`.

PSL closes the largest remaining systemic technical-fidelity gap that the
P0–P5+PSC infrastructure had documented but not corrected: the WP→MD
exporter systematically flattened paragraph blank-lines and list nesting,
so the built site rendered different structural HTML from the live
WordPress oracle on most posts. PSL restores that structural shape
oracle-by-oracle (live `https://blog.mithis.net` with `curl -sk`) across
the corpus, while leaving the WP-artifact divergences that legitimately
need inline HTML to P6 visual signoff.

**Regenerate the gate (on merged main):** `uv run python -m
scripts.fidelity.lint_content _posts --asset-root .` (exit 0 / no output);
`uv run python -m scripts.fidelity.structure_check` (6/6); `uv run python
-m pytest tests/ -q` (54); `FIDELITY_SKIP_RENDER=1 uv run python -m
scripts.fidelity.run` (Build PASS, Content linter PASS 0); `bundle3.3 exec
jekyll build` (clean).

---

## 1. Exit gate (verified from clean tree at `96ecd0b`)

| Gate | Required | Observed |
|---|---|---|
| Content linter (via CLI, enforced by CI build-guard) | 0 findings | **PASS (0)** + no output ✓ |
| `structure_check` | PASS 6/6 | **PASS (6/6)** ✓ |
| Hermetic suite | green | **54 passed** ✓ |
| Build (Fidelity runner) | PASS | **PASS** ✓ |
| `bundle3.3 exec jekyll build` | clean | clean, no errors ✓ |
| `_posts` count | 76 | **76** ✓ |
| CI build-guard step (P5-H) | still wired | line 45 of `.github/workflows/jekyll.yml`, exact run cmd ✓ |
| Per-post structural fidelity vs live oracle (§A B1) | built `<p>` count == oracle | 34/34 B1 posts ✓ |
| Per-post structural fidelity vs live oracle (§A B2) | built `<ul>`-max-nest == oracle | 2/2 B2 posts ✓ |
| Per-post structural fidelity vs live oracle (§A B3) | built `<ul>` count + interstitial == oracle | 5/5 B3 posts ✓ |
| Per-post structural fidelity vs live oracle (§A B4) | combined recipe; ±N WP-artifact tolerance documented | 5/5 B4 posts ✓ |
| OVER-P trio repaired | built P == oracle P | 3/3 (osdc-orbital, gsoc2008, starhunter) ✓ |
| Content preservation (byte-level) | typography U+2019/U+2018/U+201C/D/U+00A0 + code-block content preserved | restored to exact pre-PSL counts after Phase-3-fix; 104 typography chars + hdmi2usb-day-3 code block byte-identical (378 bytes) ✓ |
| Working tree | clean | clean; 19 commits ahead of `main` |

## 2. What PSL did (19 commits across 4 stages)

### PSL-T1: pragmatic audit + EXEC charter — `743703c`
- Live-oracle sample on 12 posts confirmed the flattening hypothesis: 11/12
  show oracle `<p>` > built `<p>`; sample total Δ +68 paragraphs missing.
- Estimated bucket distribution from a build-side full sweep + sample-confirmed
  rate: B0 (faithful) ~13, B1 (paragraph blank-line) ~43, B2 (list-nesting) ~5,
  B3 (list-break interstitial) 2, B4 (mixed) ~13.
- Defined per-bucket canonical recipes + the 3-phase EXEC charter (Phase 1
  mechanical bulk, Phase 2 focused per-post, Phase 3 precision) + the
  per-post gate (built ↔ oracle structural-metric match).

### PSL-EXEC Phase 1 — B1 paragraph-blank-line restoration (34 posts; 4 batch commits)
- `ebc8212` batch 1 — 8 posts
- `ef5096d` batch 2 — 8 posts
- `b45c66f` batch 3 — 8 posts
- `9dd2df9` batch 4 — 10 posts

Oracle-driven script under `tmp/psl/` (gitignored): for each post, fetched
the live `<p>` block list, located each block's start in the source body,
inserted blank lines BEFORE each oracle-matched anchor; never modified
words. Two notable judgment calls (both spec-review APPROVED):
- `2007-08-17-nm-vpn.md`: source was one long concatenated line with 3
  embedded `- ` items. Script split into separate lines (LI 3, plus
  closing paragraph) — character-identical to oracle, no content drift.
- `2008-06-10-techtalk-gamingforfreedom.md`: WP wraps the Flash `<object>`
  in an extra `<p>` that kramdown can't reproduce for raw-HTML blocks;
  accepted as ±1 P tolerance.

All 34 posts passed the oracle P-count gate; 0 failures.

### PSL-EXEC Phase 2 — B2 list-nesting + B3 list-break interstitials (7 posts; 7 atomic commits)
- B2 (list-nesting only): `149a38b` `hdmi2usb-day-1` (UL 1→2, max_nest 1→2),
  `58bbf29` `hdmi2usb-day-8` (UL 1→2, max_nest 1→2).
- B3 (list-break interstitial): `0e955ee` `lca-proposal-suggestions`
  (UL 1→2, P 1→7); `34ff90c` `i-want-a-cool-desktop` (UL 1→3, P 1→7);
  `e6e3998` `epiphany2firefox` (UL 1→3, P 1→10 oracle=11 ±1);
  `a328e1e` `hdmi2usb-day-4` (UL 4→5; oracle has WP `&nbsp;` empty P +
  blockquote-wrapped images — ±1 tolerance); `32b0d27` `first-v2-hdmi2usb`
  (UL 1→2, P 2→4).

`i-want-a-cool-desktop` was tagged B4 in the audit narrative but B3 in
the machine `worklist.json`; oracle max_nest=1 confirmed the worklist's
classification (canonical B3).

### PSL-EXEC Phase 3 — B4 mixed + OVER-P trio (8 posts; 6 commits)
- `b475239` OVER-P trio fix: `osdc-orbital-death` (built P now 5 ↔ oracle;
  blockquote wraps the 2 quote lines); `gsoc2008` (3 JLP paras moved
  inside `> ` blockquote → oracle's blockquote structure); `starhunter`
  (4 prose paras separated). All three OVER-P posts now match the oracle
  P-count (excluding Jekyll-template chrome paragraphs).
- `7ca3b44` `hdmi2usb-snippets` (UL=4 LI=24 max_nest=2; 4 oracle
  `<p>&nbsp;</p>` spacers accepted as WP artifact).
- `bd81079` `hdmi2usb-day-5-6-7` (UL=4 LI=16 max_nest=2; 3 spacers accepted).
- `1cd5af4` `timvideos-2016` (blockquote with H=3 + UL count + LI=25
  + max_nest=2 — full structural reconstruction of the resolutions
  blockquote).
- `4b47432` `fritzbox-vpnc` (UL=2 LI=9 max_nest=2; final blockquote
  section accepted as WP artifact; **P6 `<pre><strong>` bold-in-code
  USER-DECISION preserved untouched**).
- `9ba42f1` `hdmi2usb-day-3` (the most complex: max_nest=3 LI=41; post-PRE
  orphan `<ul><ul>` accepted as WP artifact — Markdown cannot express
  `<ul>` without an enclosing `<li>`).

### PSL-EXEC Phase 3 fix — Unicode typography restoration — `96ecd0b`
The code-quality reviewer found a systemic content-preservation
regression: the edit tool silently normalized U+2019/U+2018/U+201C/D
typography characters → ASCII apostrophes/quotes AND U+00A0 NBSP → ASCII
space across 7 of the 8 Phase 3 posts (39 U+2019 + 4 U+2018 + 18 U+201C
+ 20 U+201D + 23 U+00A0 = **104 characters** total), **including inside
the `hdmi2usb-day-3` fenced code block** (kernel log `laptop\xc2\xa0udevd`
NBSP).

The fix commit applies a per-line typography-restoration script driven by
the pre-PSL bytes (`git show 1679cf1:<path>`): for each line with the
same logical content modulo indentation/blockquote-prefix, the pre-PSL
typography characters are restored at matching positions. The `hdmi2usb-day-3`
code block is byte-identical to pre-PSL (verified by `diff` on the
fenced-block bytes); all front-matter `title:`/`excerpt:` typography
restored. All Phase 3 structural restoration preserved. Also documents
the `osdc-orbital-death` oracle-P-count clarification (correct oracle=6,
built=7, +1 from comments-section layout).

Re-review: ✅ FIX CONFIRMED CLEAN.

## 3. Cumulative project state (P0 → PSL)

- **Content fidelity (corpus).** 76/76 posts present (§11 met). All 22+1
  category pages render the WP-faithful post set + counts (PSC pass). All
  47 historical content-linter findings resolved (P2). Per-post live-WP
  structural shape (paragraph blank-lines + list nesting) restored across
  the entire corpus (PSL); WP-artifact divergences that legitimately need
  inline HTML are documented for P6 user signoff.
- **Authoring fidelity (going forward).** Documented authoring workflow
  (`docs/AUTHORING.md`), tested scaffold (`scripts/new_post.py`), tested
  reference template (`docs/sample-new-post.md`), and a CI build-guard
  (`.github/workflows/jekyll.yml` line 45) that exits non-zero on any
  future structural-HTML violation in `_posts/` — the first proactive
  fidelity safeguard, P5.
- **Comment system.** `_includes/comments.html` list-fallback-robust;
  comments rendering across all 8 known-comment posts (P3 + P5-D).
- **Test fences.** Linter CLI now exits 1 on findings (P5-A polish);
  structure_check 6/6; 54 pytest; Fidelity runner Build PASS + Content
  linter PASS 0.
- **Deployment ready.** `baseurl: ""` + `CNAME blog.mithis.net` + 301s
  set up (P4); pending only the user's DNS cutover (CNAME
  `blog → mithro.github.io` + GitHub Pages custom-domain + Enforce HTTPS).

## 4. Handoff — P6 next

The remaining work is **P6** (the final phase) — pixel-level visual
signoff. PSL's accepted WP artifacts give P6 a curated list of inline-HTML
restoration candidates per design §7 (`fritzbox-vpnc` final blockquote,
fritzbox bold-in-code `<pre><strong>`, `hdmi2usb-day-3` post-PRE orphan
`<ul><ul>`, `hdmi2usb-day-4` blockquote-wrapped images +`&nbsp;` spacer,
3 `<p>&nbsp;</p>` spacers, `epiphany2firefox` centered screenshot `<p>`,
3 linked-thumbnail `<a title>` tooltips, `<hr/>` survival). Each is a
P6 USER-DECISION: accept the divergence (no change), OR restore via
minimal `<HTML>` per design §7 with a `<!-- fidelity-allow: BLOCK_HTML
pixel-fidelity-tolerance -->` sentinel.

Also remaining for P6: Wayback pixel-by-pixel signoff for visual
fidelity claim; CSS micro-deltas; Picasa byte-fidelity confirmation;
nav-below clearfix verification; the recorded R-E region-3 fence
cosmetic; the P3 pre-existing comment-data fidelity check.

PSL polish items (5 cosmetic non-blockers from PSL reviews) are recorded
in `docs/superpowers/plans/FOLLOWUPS.md` under the "PSL polish" heading
for a future polish-bundle commit, separate from P6.

## 5. PSL gate — independent re-verification command stack

```bash
cd <repo>  # main after merge
uv run python -m scripts.fidelity.lint_content _posts --asset-root .  # exit 0
uv run python -m scripts.fidelity.structure_check                      # PASS 6/6
uv run python -m pytest tests/ -q                                      # 54 passed
FIDELITY_SKIP_RENDER=1 uv run python -m scripts.fidelity.run           # Build PASS, Content linter 0
bundle3.3 exec jekyll build                                            # clean
ls _posts/*.md | wc -l                                                 # 76
```

All six commands MUST succeed for the PSL exit gate to be considered met
on merged main.
