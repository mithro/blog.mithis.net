# P6-USER-DECISIONS — Visual Fidelity Signoff Queue

**Phase:** P6 Final Acceptance (pixel-level visual fidelity signoff)
**Compiled:** 2026-05-20
**Branch:** `migration-p6-final-signoff`
**Source:** `docs/superpowers/plans/P6-FINDINGS.md` §C (Queue B)

---

## §1 — Status and how to use this doc

The autonomous P6 work (Queue A: A-1 through A-9) is complete. The Jekyll site is fully
built, all 76 posts are present, the content linter passes at zero, and structural/Wayback
verification is done.

What remains is **your explicit decision on 9 visual-fidelity items**. Each item is a
WordPress artifact that cannot be faithfully expressed in plain Markdown — it requires
minimal inline HTML (with the `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->`
sentinel) to restore. Neither option is automatically applied; you decide.

**Two choices per item:**
- `restore` — P6-Z will add the minimal inline HTML to the source post; the linter will
  pass (the sentinel is the approved exception mechanism per design §7).
- `accept` — ship the current Markdown rendering; document the divergence and move on.
- `either` — genuinely a coin-flip; Claude will pick the simpler path unless you have a
  preference.

**RESOLVED items** are marked — the oracle and built rendering already match; no decision needed.

Read §2 for a quick overview, then §3 for details on any item you want to look at more
carefully. Reply in any format you find convenient (see §4 for examples).

---

## §2 — Quick-decision matrix

| #   | Post slug                            | Artifact                                   | Visual impact | Recommended | Effort  |
|-----|--------------------------------------|--------------------------------------------|---------------|-------------|---------|
| B-1 | fritzbox-vpnc                        | Final section wrapped in `<blockquote>`    | medium        | restore     | low     |
| B-2 | fritzbox-vpnc                        | `<pre><strong>` bold in 3 code blocks      | low–medium    | either      | medium  |
| B-3 | hdmi2usb-day-3                       | Post-PRE orphan `<ul><ul>` nesting         | low           | accept      | low     |
| B-4 | hdmi2usb-day-4                       | `<blockquote>`-wrapped images + `&nbsp;`   | medium        | restore     | low     |
| B-5 | hdmi2usb-snippets                    | 4× `<p>&nbsp;</p>` spacers                 | low           | accept      | low     |
| B-6 | hdmi2usb-day-5-6-7                   | 3× `<p>&nbsp;</p>` spacers                 | low           | accept      | low     |
| B-7 | epiphany2firefox                     | Broken `<img>` + missing center wrapper    | **high**      | restore     | low     |
| B-8 | almost-there + google-patchwork (×2) | `<a title="…">` hover-tooltips (3 links)   | low           | either      | low     |
| B-9 | starhunter                           | `<div style="float: right">` img wrapper   | medium        | restore     | low     |

---

## §3 — Per-item detail

---

### B-1: `fritzbox-vpnc` — final section wrapped in `<blockquote>`

**Affected post:** `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`
**Permalink:** `/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc`
**Live oracle URL:** https://blog.mithis.net/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc

**The artifact (from oracle):**
```html
<blockquote>
<h2>Fritz!Box encrypted VPN configuration files</h2>
<p>Fritz!Boxes will only accept VPN configurations which are encrypted…</p>
<p><img class="alignnone size-full wp-image-1835" alt="Error: Import of the VPN settings failed."
    src="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error.png" …/></p>
<p>To create an encrypted file…</p>
<p><img class="alignnone size-full wp-image-1836" alt="Export VPN settings"
    src="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-encrypt.png" …/></p>
</blockquote>
```

**Current built rendering:**
```html
<h2 id="fritzbox-encrypted-vpn-configuration-files">Fritz!Box encrypted VPN configuration files</h2>
<p>Fritz!Boxes will only accept VPN configurations which are encrypted…</p>
<p><img alt="Error: Import of the VPN settings failed." … src="/assets/images/…/VPN-error.png" …/></p>
<p>To create an encrypted file…</p>
<p><img alt="Export VPN settings" … src="/assets/images/…/VPN-encrypt.png" …/></p>
```
The final section appears as a normal heading + paragraphs with no blockquote indentation.

**Restoration proposal** (insert before `## Fritz!Box encrypted VPN configuration files` at
line 151 of the source post, and add a closing `</blockquote>` at the end):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<blockquote>

## Fritz!Box encrypted VPN configuration files

Fritz!Boxes will only accept VPN configurations which are encrypted. Otherwise when try
to import the file you will get the cryptic "Error: Import of the VPN settings failed."
as seen below;

<img alt="Error: Import of the VPN settings failed." class="alignnone size-full wp-image-1835"
  height="265" sizes="(max-width: 745px) 100vw, 745px"
  src="/assets/images/wp-content/uploads/2013/10/VPN-error.png"
  srcset="/assets/images/wp-content/uploads/2013/10/VPN-error.png 745w" width="745"/>

To create an encrypted file you must use the FRITZ!Box VPN Connection tool. Then when
exporting, select "Save VPN settings in a file under" option, check the "Encrypt VPN
settings" check box (the file type should change to .eff), and enter your chosen password
twice.

<img alt="Export VPN settings" class="alignnone size-full wp-image-1836" height="306"
  sizes="(max-width: 442px) 100vw, 442px"
  src="/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png"
  srcset="/assets/images/wp-content/uploads/2013/10/VPN-encrypt.png 442w" width="442"/>

</blockquote>
```

**Accept-divergence consequence:** The "Fritz!Box encrypted VPN configuration files" section
renders without a blockquote — no left-indented border. Noticeably different to anyone
comparing side-by-side, as the section was visually set apart from the rest of the post.

**Recommendation:** `restore`. The blockquote is a meaningful visual frame that sets this
explanatory section apart from the how-to steps above it; restoring it matches the author's
original presentational intent. Effort is minimal (one blockquote wrapper).

---

### B-2: `fritzbox-vpnc` — `<pre><strong>` bold emphasis in code blocks

**Affected post:** `_posts/2013-10-06-connecting-to-a-fritzbox-under-linux-using-vpnc.md`
**Permalink:** `/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc`
**Live oracle URL:** https://blog.mithis.net/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc

**The artifact (from oracle — block 1, partial):**
```html
<pre>
...
    <strong>iphone = 1;
    xauth_key = "xxxxx";</strong>
  }
...
</pre>
```
**The artifact (from oracle — block 3, the vpnc.conf template):**
```html
<pre>
IPSec gateway <strong>ip address or DNS name of your FritzBox</strong>
…
IPSec ID <strong>[username entered into the "Enter the user's email address" screen]</strong>
IPSec secret <strong>[shared secret key from the "Key for the connection" screen]</strong>
…
Xauth username <strong>[username entered into the "Enter the user's email address" screen]</strong>
Xauth password <strong>[password entered into the "Key for the connection" screen - Not the
  password use to encrypt the vpnc configuration!]</strong>
</pre>
```

**Current built rendering (block 1):**
```html
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>...
    iphone = 1;
    xauth_key = "xxxxx";
  }
...
</code></pre></div></div>
```
All key lines are plain text — the bold is stripped. Block 3's "replace-me" placeholder
lines are also unbolded.

**Restoration proposal:** Replace the 3 affected fenced ` ``` ` blocks with raw `<pre>` HTML
(one sentinel per block):

Block 1 (inside the bullet about vpnadmin.cfg):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<pre>...
  user {
    nameoremail = "xxxx";
    key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    ip = 192.168.179.201;
    internetaccess = 0;
    <strong>iphone = 1;
    xauth_key = "xxxxx";</strong>
  }
...</pre>
```

Block 2 (unencrypted cfg export example, key_id and use_xauth sections bolded):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<pre>...
  keepalive_ip = 0.0.0.0;
  remoteid {
    <strong>key_id</strong> = "qnap";
  }
  ...
  <strong>use_xauth = yes;
  xauth {
    valid = yes;
    username = "qnap";
    passwd = "qnappassword";
  }</strong>
  ...</pre>
```

Block 3 (vpnc.conf template with "replace-me" placeholders bolded):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<pre>IPSec gateway <strong>ip address or DNS name of your FritzBox</strong>

IKE DH Group dh2
Perfect Forward Secrecy nopfs

IPSec ID <strong>[username entered into the "Enter the user's email address" screen]</strong>
# "key" from the Fritz!Box VPN configuration
IPSec secret <strong>[shared secret key from the "Key for the connection" screen]</strong>

NAT Traversal Mode force-natt

Xauth username <strong>[username entered into the "Enter the user's email address" screen]</strong>
Xauth password <strong>[password entered into the "Key for the connection" screen - Not the password use to encrypt the vpnc configuration!]</strong></pre>
```

**Accept-divergence consequence:** Three code blocks render with all text at the same weight.
The "replace-me" placeholder lines in block 3 are the most useful to bold (they guide the
reader to what must be changed); losing the bold there is a moderate UX regression.

**Recommendation:** `either`. Bold-in-code is genuinely useful for guiding readers, but raw
`<pre>` HTML is the most structurally invasive BLOCK_HTML type. If you lean toward
completeness, choose `restore`; if you prefer to keep the source clean, `accept` is fine.
P6-Z will default to `accept` if you specify `either` and move on.

---

### B-3: `hdmi2usb-day-3` — post-PRE orphan `<ul><ul>` nesting

**Affected post:** `_posts/2014-07-24-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014.md`
**Permalink:** `/archives/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014`
**Live oracle URL:** https://blog.mithis.net/archives/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014

**The artifact (from oracle — immediately after the `<pre>` block):**
```html
<ul>
<ul>
<li>This was fixed with;
<ul><li>Changing SYSFS to ATTRS</li>…</ul>
</li>
<li>The little status light then turned on red! Yay!</li>
</ul>
</ul>
```
The outer `<ul>` has no `<li>` — an orphaned double-`<ul>` wrapping the items. This is a
WordPress HTML quirk.

**Current built rendering (immediately after the `<pre>` block):**
```html
<ul>
  <li>This was fixed with;
    <ul>
      <li>Changing SYSFS to ATTRS</li>
      <li>Changing BUS to SUBSYSTEM</li>
      <li>Changing $TEMPNODE to $tempnode</li>
    </ul>
  </li>
  <li>The little status light then turned on red! Yay!</li>
  …
</ul>
```
A proper single-level `<ul>` — more semantically correct than the oracle's orphan structure.

**Restoration proposal** (replace the Markdown list after the `<pre>` block):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<ul><ul>
<li>This was fixed with;
<ul>
<li>Changing SYSFS to ATTRS</li>
<li>Changing BUS to SUBSYSTEM</li>
<li>Changing $TEMPNODE to $tempnode</li>
</ul>
</li>
<li>The little status light then turned on red! Yay!</li>
<li>Was able to do a boundary scan in iMPACT on a Zybo development board after soldering a header onto it.</li>
</ul></ul>
```

**Accept-divergence consequence:** A flat single-level `<ul>` renders where the oracle has
a double-nested orphan structure. The visual difference is one level of indentation on those
3 items. Content is fully preserved.

**Recommendation:** `accept`. The `<ul><ul>` structure is an invalid HTML quirk from
WordPress's editor — not an intentional presentational choice. The flat list is semantically
correct and more accessible. Restoring the quirk would introduce known-bad HTML.

---

### B-4: `hdmi2usb-day-4` — `<blockquote>`-wrapped images + `&nbsp;` spacer

**Affected post:** `_posts/2014-07-25-hdmi2usb-production-board-bring-up-day-4-24th-july-2014.md`
**Permalink:** `/archives/timvideos-us/1995-hdmi2usb-production-board-bring-up-day-4-24th-july-2014`
**Live oracle URL:** https://blog.mithis.net/archives/timvideos-us/1995-hdmi2usb-production-board-bring-up-day-4-24th-july-2014

**The artifact (from oracle):**
```html
<blockquote>
<p style="text-align: center;">
  <a href="…/IMG_20140725_0029322.jpg">
    <img class="alignnone wp-image-1997 size-medium"
      src="…/IMG_20140725_0029322-225x300.jpg"
      alt="Numato HDMI2USB Prototype driving 2 screens" width="225" height="300" …/>
    <img class="alignnone wp-image-1998"
      src="…/IMG_20140725_003008-300x225.jpg"
      alt="HDMI2USB weird image artifact" width="400" height="300" …/>
  </a>
</p>
</blockquote>
<p>&nbsp;</p>
```

**Current built rendering:**
```html
<p><a href="/assets/images/…/IMG_20140725_0029322.jpg">
  <img alt="Numato HDMI2USB Prototype driving 2 screens" class="alignnone …"
    src="/assets/images/…/IMG_20140725_0029322-225x300.jpg" … />
  <img alt="HDMI2USB weird image artifact" class="alignnone …"
    src="/assets/images/…/IMG_20140725_003008-300x225.jpg" … />
</a></p>
```
Images render left-aligned without the blockquote frame, without center alignment, and
without the spacer paragraph below.

**Restoration proposal** (replace the `[![…]](…)` Markdown image link with inline HTML):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<blockquote>
<p style="text-align: center;"><a href="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322.jpg"><img class="alignnone wp-image-1997 size-medium" alt="Numato HDMI2USB Prototype driving 2 screens" height="300" sizes="(max-width: 225px) 100vw, 225px" src="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg" srcset="/assets/images/wp-content/uploads/2014/07/IMG_20140725_0029322-225x300.jpg 225w" width="225"/>  <img class="alignnone wp-image-1998" alt="HDMI2USB weird image artifact" height="300" sizes="(max-width: 400px) 100vw, 400px" src="/assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg" srcset="/assets/images/wp-content/uploads/2014/07/IMG_20140725_003008-300x225.jpg 300w" width="400"/></a></p>
</blockquote>

<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<p>&nbsp;</p>
```

**Accept-divergence consequence:** Two images display left-aligned inside a plain paragraph,
without the visual blockquote frame and center alignment. Anyone comparing to the oracle sees
a layout difference.

**Recommendation:** `restore`. Centered images inside a blockquote frame is a recognizable
WP layout choice; restoring it matches the original visual presentation. Effort is minimal.

---

### B-5: `hdmi2usb-snippets` — 4× `<p>&nbsp;</p>` spacer paragraphs

**Affected post:** `_posts/2014-07-21-hdmi2usb-production-board-bring-up-snippets-prep-work.md`
**Permalink:** `/archives/timvideos-us/1980-hdmi2usb-production-board-bring-up-snippets-prep-work`
**Live oracle URL:** https://blog.mithis.net/archives/timvideos-us/1980-hdmi2usb-production-board-bring-up-snippets-prep-work

**The artifact (from oracle):** Four occurrences of `<p>&nbsp;</p>` at line 163, 174, 179,
and 194 of the oracle HTML — empty spacer paragraphs between topic sections.

**Current built rendering:** No spacer paragraphs; sections are separated only by standard
paragraph spacing (one blank line in Markdown renders as normal paragraph margin).

**Restoration proposal** (4 instances, inserted between sections in the source post):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<p>&nbsp;</p>
```

**Accept-divergence consequence:** Sections in this post run together with standard paragraph
spacing rather than having extra visual whitespace between them. Readers get the same content;
the sections are slightly less visually separated.

**Recommendation:** `accept`. Empty `&nbsp;` paragraphs are a WordPress layout hack, not a
semantic content element. Standard paragraph spacing is cleaner HTML and fully readable.
The content meaning is unaffected.

---

### B-6: `hdmi2usb-day-5-6-7` — 3× `<p>&nbsp;</p>` spacer paragraphs

**Affected post:** `_posts/2014-07-28-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014.md`
**Permalink:** `/archives/timvideos-us/2003-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014`
**Live oracle URL:** https://blog.mithis.net/archives/timvideos-us/2003-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014

**The artifact (from oracle):** Three occurrences of `<p>&nbsp;</p>` at oracle lines 164,
171, and 183 — same pattern as B-5.

**Current built rendering:** No spacer paragraphs; sections run together with standard spacing.

**Restoration proposal** (same as B-5, 3 instances):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<p>&nbsp;</p>
```

**Accept-divergence consequence:** Same as B-5 — slightly less visual separation between
sections. No content impact.

**Recommendation:** `accept`. Same reasoning as B-5. Empty spacer paragraphs are a WP
authoring artifact; standard spacing is semantically cleaner.

---

### B-7: `epiphany2firefox` — broken `<img>` rendering + missing center wrapper

**Affected post:** `_posts/2008-04-10-epiphany2firefox.md`
**Permalink:** `/archives/uncategorized/77-epiphany2firefox`
**Live oracle URL:** https://blog.mithis.net/archives/uncategorized/77-epiphany2firefox

**NOTE: This item is higher severity than originally described in P6-FINDINGS.** The
source post (line 45) contains a broken Liquid template fragment:
```
[<img alt="Screenshot of my Firefox" src="http://web.archive.org/web/20110311214257im_//assets/images/wp-content/uploads/2008/04/myfirefox.png" | relative_url }}"/>
```
The `| relative_url }}` suffix is an orphaned Liquid filter fragment that was not cleaned
up during migration. As a result, the built page renders this as escaped literal text
(`[&lt;img alt="Screenshot of my Firefox" src="…" | relative_url }}"/&gt;`), not as an
image at all. **The screenshot is completely invisible in the current build.**

**The artifact (from oracle):**
```html
<p style="text-align: center">
  <a href="https://blog.mithis.net/wp-content/uploads/2008/04/myfirefox.png"
     title="Screenshot of my Firefox">
    <img src="https://blog.mithis.net/wp-content/uploads/2008/04/myfirefox.png"
         alt="Screenshot of my Firefox" />
  </a>
</p>
```

**Current built rendering:**
```html
<p>Here is what my Firefox looks like currently. As you can see I have significantly
customized the toolbar to remove all that excesses.
[&lt;img alt="Screenshot of my Firefox" src="http://web.archive.org/web/20110311214257im_//assets/images/wp-content/uploads/2008/04/myfirefox.png" | relative_url }}"/&gt;</p>
```
The image is rendered as escaped literal text — it is invisible as an image.

**Restoration proposal** (replace the broken line 45 with correct inline HTML):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<p style="text-align: center"><a href="http://web.archive.org/web/20110311214257/https://blog.mithis.net/wp-content/uploads/2008/04/myfirefox.png" title="Screenshot of my Firefox"><img alt="Screenshot of my Firefox" src="http://web.archive.org/web/20110311214257im_/https://blog.mithis.net/wp-content/uploads/2008/04/myfirefox.png"/></a></p>
```
This uses the Wayback image URL (the original WP upload is gone; Wayback is the only
surviving source) and adds the center wrapper + link title from the oracle.

**Accept-divergence consequence:** The screenshot of Firefox remains completely invisible —
rendered as escaped literal text in the page body. Any reader reaching the end of the post
sees broken garbled markup instead of the image. This is a significant regression; the post
text explicitly says "Here is what my Firefox looks like currently."

**Recommendation:** `restore`. The image is completely broken in the current build (not merely
uncentered). This is the highest-priority item in the queue. The fix is minimal: one line
replacing the broken Liquid fragment with correct inline HTML.

---

### B-8: `almost-there` + `google-patchwork` — `<a title="…">` hover-tooltips (3 links)

**Affected posts:**
- `_posts/2007-05-09-almost-there.md` — permalink `/archives/pcb/40-almost-there`
- `_posts/2008-02-04-google-patchwork.md` — permalink `/archives/google/67-google-patchwork`

**Investigation note (P6-FINDINGS mentioned a possible third instance in hardware-mod-of-htc-hd2):** That post does not exist in the migrated set. The hardware category contains only one post (`nmigen-new-improved-by-whitequark`). The `almost-there` + `google-patchwork` instances are the complete set.

**Live oracle URLs:**
- https://blog.mithis.net/archives/pcb/40-almost-there
- https://blog.mithis.net/archives/google/67-google-patchwork

**The artifact (from oracle — almost-there):**
```html
<p align="center">
  <a href="https://blog.mithis.net/wp-content/uploads/2007/05/cfxs-try2.jpg"
     title="CFXS Try2 PCB Board">
    <img src="https://blog.mithis.net/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg"
         alt="CFXS Try2 PCB Board" />
  </a>
</p>
```

**The artifact (from oracle — google-patchwork, 2 images):**
```html
<p><a href="…/map-patchwork.png" title="Google patchwork.">
  <img src="…/map-patchwork.png" alt="Google patchwork." /></a></p>
<p><a href="…/map-change.png" title="Google Transsision">
  <img src="…/map-change.png" alt="Google Transsision" /></a></p>
```

**Current built rendering (almost-there):**
```html
<p><a href="/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg">
  <img src="/assets/images/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg"
       alt="CFXS Try2 PCB Board" /></a></p>
```
The `title="CFXS Try2 PCB Board"` on the `<a>` tag is absent. Also note: the oracle has
`<p align="center">` — the centering is also lost (though `align=` is a deprecated attribute).

**Current built rendering (google-patchwork, both images):**
```html
<p><a href="/assets/images/wp-content/uploads/2008/02/map-patchwork.png">
  <img src="/assets/images/wp-content/uploads/2008/02/map-patchwork.png"
       alt="Google patchwork." /></a></p>
<p><a href="/assets/images/wp-content/uploads/2008/02/map-change.png">
  <img src="/assets/images/wp-content/uploads/2008/02/map-change.png"
       alt="Google Transsision" /></a></p>
```
The `title=` attributes on the `<a>` tags are absent.

**Restoration proposal (almost-there):**
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<p align="center"><a href="/assets/images/wp-content/uploads/2007/05/cfxs-try2.jpg" title="CFXS Try2 PCB Board"><img alt="CFXS Try2 PCB Board" src="/assets/images/wp-content/uploads/2007/05/cfxs-try2.thumbnail.jpg"/></a></p>
```

**Restoration proposal (google-patchwork, both images):**
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<a href="/assets/images/wp-content/uploads/2008/02/map-patchwork.png" title="Google patchwork."><img alt="Google patchwork." src="/assets/images/wp-content/uploads/2008/02/map-patchwork.png"/></a>

<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<a href="/assets/images/wp-content/uploads/2008/02/map-change.png" title="Google Transsision"><img alt="Google Transsision" src="/assets/images/wp-content/uploads/2008/02/map-change.png"/></a>
```

**Accept-divergence consequence:** Hovering over the linked images produces no tooltip. The
images, alt text, and link functionality are fully intact. Tooltips are a minor UX nicety.

**Recommendation:** `either`. The tooltip is a small detail; the image+link is faithfully
rendered. If you want the link to show a tooltip on hover, choose `restore`; otherwise `accept`
is fine. P6-Z will default to `accept` if you leave this as `either`.

---

### B-9: `starhunter` — `<div style="float: right; padding: 10px;">` image wrapper

**Affected post:** `_posts/2009-05-26-starhunter-fireflys-little-known-older-cousin.md`
**Permalink:** `/archives/sci-fi/102-starhunter-fireflys-little-known-older-cousin`
**Live oracle URL:** https://blog.mithis.net/archives/sci-fi/102-starhunter-fireflys-little-known-older-cousin

**The artifact (from oracle):**
```html
<div style="float: right; padding: 10px;">
  <img class="aligncenter size-full wp-image-103"
       title="Tulip - The ship from Starhunter"
       src="https://blog.mithis.net/wp-content/uploads/2009/05/screenshot.png"
       alt="Tulip - The ship from Starhunter" width="300" height="219" />
</div>
```
The image floats to the right with 10px padding, so the post text wraps around it on the left.

**Current built rendering:**
```html
<p><img alt="Tulip - The ship from Starhunter" height="219"
        src="/assets/images/wp-content/uploads/2009/05/screenshot.png"
        title="Tulip - The ship from Starhunter" width="300" /></p>
```
The `<img>` itself (with `title=` attribute) is already in the source post as inline HTML.
However the `<div>` float wrapper is absent, so the image renders as a block element at the
top of the content, and the post text begins below it rather than wrapping alongside.

**Restoration proposal** (replace line 22 of the source post):
```markdown
<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->
<div style="float: right; padding: 10px;"><img alt="Tulip - The ship from Starhunter" class="aligncenter size-full wp-image-103" height="219" src="/assets/images/wp-content/uploads/2009/05/screenshot.png" title="Tulip - The ship from Starhunter" width="300"/></div>
```

**Accept-divergence consequence:** The Starhunter ship image renders as a full-width block
above the post text, rather than floating to the right with text wrapping alongside it.
Visible layout difference — the original had a classic "text-beside-image" layout that the
current rendering does not.

**Recommendation:** `restore`. The `float: right` is a meaningful layout choice that affects
the entire reading experience of the post. The text-beside-image layout is visually distinct
from text-below-image. Effort is minimal (one `<div>` wrapper around the existing `<img>`).

---

## §4 — How to reply

Any clear format works. Examples:

**Option A — numbered list:**
```
B-1 restore
B-2 accept
B-3 accept
B-4 restore
B-5 accept
B-6 accept
B-7 restore
B-8 either (you pick)
B-9 restore
```

**Option B — free-form:**
"Restore B-1, B-4, B-7, B-9. Accept B-3, B-5, B-6. For B-2 and B-8, you decide."

**Option C — accept all / restore all:**
"Restore everything recommended" or "Accept everything" are also valid answers.

**Notes:**
- `either` means P6-Z will default to `accept` unless you add a preference.
- You can mix any format. The implementer reads for clear intent, not format compliance.
- If you want to change a recommendation (e.g., accept B-1 instead of restoring it), just
  say so — all options are valid.

---

## §5 — What happens after you reply

1. P6-Z dispatches an implementer agent to apply your chosen restorations to the source
   `_posts/` files, with the `<!-- fidelity-allow: BLOCK_HTML pixel-fidelity-tolerance -->`
   sentinel on each block.
2. The linter is re-run to confirm it stays at 0 (`bundle3.3 exec jekyll build` + linter).
3. The final P6 gate check runs: linter 0, structure_check 6/6, 54+ pytest green, build clean.
4. If you chose `accept` for all items, no `_posts/` files are changed — P6-Z proceeds
   directly to final documentation and merge-to-main.
5. P6-Z commits the restorations (if any), writes the final `P6-RESULTS.md`, and prepares
   the branch for merge.

If any restoration reveals an unexpected linter issue, P6-Z will surface it before finalizing.

---

## §6 — Applied decisions (controller-autonomous execution, 2026-05-20)

The following decisions were applied by the implementer subagent per the controller's
autonomous-default directive and the bundle's per-item recommendations. Restorations
(B-1, B-4, B-7, B-9) were committed atomically to `_posts/`; accept-decisions (B-2, B-3,
B-5, B-6, B-8) are documented here with no source change.

### Applied restorations

- **B-1** (`fritzbox-vpnc`): `<blockquote>` wrapper added around the final section.
  Commit: `d612830` — "P6-EXEC: restore blockquote wrapper in fritzbox-vpnc (B-1)"
- **B-4** (`hdmi2usb-day-4`): `<blockquote>` + `<p style="text-align: center">` wrapper
  and `<p>&nbsp;</p>` spacer added. Commit: `d93376f` — "P6-EXEC: restore blockquote +
  center wrapper in hdmi2usb-day-4 (B-4)"
- **B-7** (`epiphany2firefox`): Broken `| relative_url }}` Liquid fragment removed AND
  centered `<p style="text-align: center">` wrapper restored. Commit: `8bfb9ec` —
  "P6-EXEC: fix broken Liquid + restore center wrapper in epiphany2firefox (B-7)"
- **B-9** (`starhunter`): `<div style="float: right; padding: 10px;">` wrapper added
  around the ship image. Commit: `7fb5da5` — "P6-EXEC: restore float:right div wrapper
  in starhunter (B-9)"

### Accepted divergences

- **B-2** (`fritzbox-vpnc` — `<pre><strong>` bold in code blocks): Accepted. Three fenced
  code blocks lose bold emphasis on key lines (the `iphone`/`xauth_key` settings and the
  "replace-me" vpnc.conf placeholders). Bold-in-code is structurally impossible in Markdown
  fenced blocks. Replacing with raw `<pre>` HTML would be the most invasive BLOCK_HTML type
  and conflicts with design §7-tolerance (structural divergence). The content is fully
  preserved; the bold is a presentational emphasis. Accepted per design §7 tolerance.

- **B-3** (`hdmi2usb-day-3` — post-PRE orphan `<ul><ul>` nesting): Accepted. The oracle's
  double-nested `<ul><ul>` (no `<li>` on the outer) is invalid HTML from WordPress's legacy
  editor, not an intentional presentational choice. The Jekyll migration renders a semantically
  correct single-level `<ul>`. Restoring the orphan structure would introduce known-bad HTML.
  The content (list items and sub-items) is fully preserved. Accepted as a semantic improvement.

- **B-5** (`hdmi2usb-snippets` — 4× `<p>&nbsp;</p>` spacers): Accepted. Empty non-breaking-
  space paragraphs are a WordPress layout hack with no semantic meaning. Standard paragraph
  spacing from Markdown renders all content fully readable; the sections are slightly less
  visually separated than in the oracle but no content is missing. Accepted per design
  §7-tolerance (cosmetic-only divergence).

- **B-6** (`hdmi2usb-day-5-6-7` — 3× `<p>&nbsp;</p>` spacers): Accepted. Same reasoning
  as B-5. Three `<p>&nbsp;</p>` paragraphs between topic sections are WordPress layout
  artifacts. Markdown paragraph spacing is semantically equivalent. Accepted per design
  §7-tolerance.

- **B-8** (`almost-there` + `google-patchwork` — `<a title="…">` hover-tooltips, 3 links):
  Accepted. The `title=` attribute on `<a>` tags provides tooltip text on hover; this
  attribute is absent from Markdown-generated `<a>` tags. The images, alt text, and link
  functionality are fully intact. `alt` text serves the primary accessibility role; tooltips
  are a low-impact UX nicety. The bundle recommendation was `either` (P6-Z defaults to
  accept). Accepted per bundle default and low visual/accessibility impact.
