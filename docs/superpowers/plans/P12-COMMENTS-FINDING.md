# P12 (finding) — Comment-data drift: `_data/comments` snapshot vs current live

**Status: FINDING ONLY — needs a USER DECISION before any remediation.**
Discovered by an exhaustive per-post comment-count diff (built `_site` vs the
live `id="comment-N"` set) after P11. NOT yet acted on.

## What was found

The migrated `_data/comments/` is a **stale export snapshot**; the live site's
comments have diverged in BOTH directions since the export:

- **17/76 posts** have a comment-count mismatch.
- **Total: built renders 16 comments; live currently shows 21.**
- **~12 posts** (`built=0, live=1`): live has a REAL user comment (2007–2009,
  `class="comment"`) that `_data` lacks — e.g. eagle-for-pcb (comment-6714),
  epiphany2firefox (6952), going-to-sydney (6956), babylon-5 (7205),
  firefox3-cookies (7208). (1 of the 13, soc-end/7233, is a `pingback`.)
- **~4 posts** (`built>live`): `_data` has comments live no longer shows —
  e.g. reading-cookies-firefox: `_data`/built has 7241–7245 (2010); live shows
  only 7206 (2009). The two sets DON'T overlap: live's 7206 is in no `_data`
  file; built's 7241–7245 appear on no current live page.

So `_data/comments/` and live have **bidirectionally diverged**: live removed
some comments (spam/moderation) after the export, and the export missed/lost
others that are still on live.

## Why this needs a USER DECISION (two stated goals now conflict)

- **"User comments must be preserved"** (CLAUDE.md core requirement) → keep the
  `_data` export snapshot; it preserves comments live has since deleted.
- **"Faithful to the current live … broken stuff and all"** (2026-05-21
  directive) → match live's CURRENT comments; would DELETE the export-only
  comments (7241–7245 etc.) and ADD the ~12 live-only ones.

These conflict. Resolving requires the user's call on the canonical source:

- **Option A — sync to current live**: re-scrape all 76 posts' current live
  comments, regenerate `_data/comments/` to match. Adds the ~12 missing,
  removes the export-only ones. Substantial; chases a mutating live; deletes
  preserved content.
- **Option B — keep the export snapshot** (canonical = migration export):
  accept built≠live comment divergence; document. No data change.
- **Option C — additive only**: ADD the ~12 missing live comments to `_data`;
  KEEP the export-only ones (don't delete). Maximizes preserved comments;
  built would then be a superset, still ≠ live exactly.

## Recommendation

Option C (additive) best honors "preserve user comments" while closing the
clearest gap (the ~12 real comments live has that `_data` lacks). But this is
the user's call — it trades off against exact live-faithfulness. Do NOT
unilaterally rewrite `_data/comments/` (high risk; mutating live; deletes
preserved content) until the user chooses.

## Scope note

The comment **rendering** is faithful (P3/P6-A-8 verified the include renders
`_data` comments correctly with real name/date/message). This finding is about
the comment DATA SET (which comments exist), not how they render.

---

## CORRECTION (2026-05-23) — live comments are EMPTY STUBS; `_data` is the good source

**The premise above was WRONG.** Deeper inspection (Playwright, full JS render +
3s wait) shows live's comments are **content-less empty stubs**: every
`<li id="comment-N">` on live renders as `<span class="comment-author vcard"></span>`
with NO author, NO date, NO message. Verified on multiple posts incl.
starhunter (comment-7258): `commentsWithAnyContent: 0`.

The earlier comment-count diff counted these empty `id="comment-N"` SKELETONS
— not real comments. So:

- **`_data/comments/` PRESERVES the real comment content** (e.g. starhunter's
  "Amanda" comment; reading-cookies' 4-message thread with full text). Built
  renders these correctly (P3/P6-A-8 verified).
- **Live's comments are degraded** — content stripped/not served (broken WP
  comment rendering on the live site, or bulk-removed leaving stubs).

### Implication: "sync to current live exactly" would DESTROY preserved comments

Matching live exactly means replacing real, content-rich preserved comments
with empty stubs (or deleting them). That contradicts the core requirement
"user comments must be preserved" and almost certainly is not the intent —
the user's "sync to live" choice was made on the (incorrect) premise that
live had real comments `_data` lacked.

### Corrected recommendation: KEEP `_data/comments/` as-is

`_data` is the authoritative preservation of the real comments. Live's
comment content is gone/broken. The built site (rendering `_data`) is MORE
faithful to the blog's actual comment history than the current live site.
No data change. The "17 mismatches" were a skeleton-counting artifact, not a
real content divergence to fix.

This correction was surfaced back to the user before any `_data` change.
