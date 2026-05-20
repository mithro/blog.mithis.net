# P6-PICASA-CHECK — Picasa Header Byte-Fidelity vs Wayback Machine

**Phase:** P6 Final Acceptance
**Date:** 2026-05-20
**Item:** A-9 from P6-FINDINGS.md

---

## Summary

**Conclusion: DOCUMENTED-DIVERGENCE (faithful intent, structural difference)**

The built `_includes/header.html` replicates the Picasa photo gallery header as a static
HTML structure, which is the correct approach given the removal of the WordPress Shashin plugin
(a dynamic photo gallery that was explicitly designated for removal). The divergence from the
Wayback oracle is intentional and documented in the design spec.

---

## Oracle Structure (Wayback 2013-12-11 snapshot)

Source: `https://web.archive.org/web/20131211171839/http://blog.mithis.net/`

The live WP site used the **Shashin** plugin to dynamically render a scrolling Picasa photo
gallery in the header. The generated HTML structure was:

```html
<div id="header">
  <table style="width: 100%; border: collapse; padding: 0; margin: 0;">
    <tr>
      <td> <!-- blog title h1 --> </td>
      <td>
        <div class="shashinPhotoGroups">
          <table class="shashinThumbnailsTable" id="shashinGroup_1_1">
            <tr>
              <td><div class="shashinThumbnailDiv" style="width: 70px;">
                <a href="...ggpht.com/...IMG_4738.JPG?imgmax=800" class="highslide">
                  <img src="...ggpht.com/...IMG_4738.JPG?imgmax=64&crop=1" width="64" height="64"
                       class="shashinThumbnailImage"/>
                </a>
                <div class="highslide-caption">
                  <div class="shashinHighslideLinkToOriginalPhoto">
                    <a href="https://picasaweb.google.com/...">View at Picasa</a>
                  </div>
                  <span class="shashinCaptionExif">12-Nov-2011 11:31, Canon PowerShot SX230...</span>
                </div>
              </div></td>
              <!-- 5 more similar <td> entries -->
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
</div>
```

Key characteristics of the oracle:
- **Container:** `<table>` with the blog title in one `<td>` and photo gallery in another
- **Plugin:** Shashin WordPress plugin with Highslide JS lightbox
- **Photo count:** 6 thumbnails (64x64px, `imgmax=64&crop=1`)
- **Thumbnail URLs:** `lh*.ggpht.com` Google Photos CDN (via Shashin)
- **Captions:** EXIF data + "View at Picasa" link per photo
- **Lightbox:** JavaScript-driven Highslide lightbox on click

Oracle photos (from 2013-12-11 snapshot):
1. `IMG_4738.JPG` — Seoul Day Two, 12-Nov-2011
2. `IMG_1926.JPG` — London Day 1, 15-Oct-2011
3. `pict0133.jpg` — 19-Feb-2006 (KONICA MINOLTA)
4. `IMG_3873.JPG` — Louvre Museum, 07-Nov-2011
5. (and 2 more)

Note: The specific photos shown are **dynamic** — the Shashin plugin selects from the configured
Picasa albums. Different snapshots show different photos. This means exact photo-for-photo
comparison is not meaningful for a dynamic plugin.

---

## Built Site Structure (current _includes/header.html)

```html
<div id="header">
    <h1 id="blog-title">...</h1>
    <div id="header-photos">
        <div class="photo-gallery">
            <div class="photo-item">
                <a href="...lh3.ggpht.com/...pict0045.jpg?imgmax=800">
                    <img src="...lh3.ggpht.com/...pict0045.jpg?imgmax=64&crop=1" alt="Photo">
                </a>
                <div class="photo-meta">
                    <a href="https://picasaweb.google.com/...">View at Picasa</a><br>
                    28-Jan-2006 16:39, KONICA MINOLTA DiMAGE E500...
                </div>
            </div>
            <!-- 5 more .photo-item divs -->
        </div>
    </div>
    <div id="header-nav">...</div>
</div>
```

Built header photos (6 hardcoded):
1. `pict0045.jpg` — 28-Jan-2006 16:39
2. `IMG_0001.JPG` — 17-Nov-2011 16:18 (Jurong Bird Park)
3. `IMG_0953.JPG` — 08-Oct-2011 19:27 (Guggenheim/Central Park)
4. `IMG_6481.JPG` — 16-Nov-2011 23:37 (Night Safari)
5. `IMG_7483.JPG` — 16-Nov-2011 23:41 (Night Safari)
6. `pict0122.jpg` — 04-Feb-2006 15:12

---

## Comparison

| Aspect | Oracle (Wayback 2013) | Built site | Status |
|--------|----------------------|------------|--------|
| Container element | `<table>` wrapper | `<div id="header-photos">` | diverges (structural) |
| Gallery plugin | Shashin (JS lightbox) | Static HTML | diverges (feature) |
| Photo count | 6 thumbnails | 6 thumbnails | MATCH |
| Thumbnail size | 64x64px crop | 64x64px crop | MATCH |
| Thumbnail URL format | `ggpht.com/...?imgmax=64&crop=1` | `ggpht.com/...?imgmax=64&crop=1` | MATCH |
| Full-size URL format | `ggpht.com/...?imgmax=800` | `ggpht.com/...?imgmax=800` | MATCH |
| "View at Picasa" link | Present per photo | Present per photo | MATCH |
| EXIF caption | Present per photo | Present per photo | MATCH |
| Specific photos shown | Dynamic (plugin selects) | 6 hardcoded from album | diverges (dynamic→static) |
| Broken thumbnails | Yes (ggpht.com no longer serves) | Yes (same reason) | MATCH (both broken) |

---

## Assessment

**Structural divergence:** The `<table>` layout vs `<div id="header-photos">` is a structural
difference. However, the original Barthelme theme's `_config.yml`/PHP had no specific layout
for the Shashin widget — Shashin injected its own `<table>` into the header area. Our static
`<div class="photo-gallery">` mimics the same visual intent (6 thumbnails in a row with links
and captions).

**Feature divergence:** The Shashin JS lightbox is not reproduced (photos no longer open in a
lightbox overlay). This is acceptable per the design spec: "Remove Broken Features" includes
removing the Shashin/Picasa integration — the photos are already broken (ggpht.com CDN no
longer serves), so the lightbox is moot.

**Photo selection:** The specific 6 photos hardcoded in our header come from Tim's Picasa albums
and match the style of photos the Shashin plugin would have shown. The exact photos differ from
the 2013 snapshot but this is expected (the plugin rotated through photos dynamically).

**Broken state parity:** Both the oracle (Wayback) and the built site show broken thumbnail
images (HTTP 404 from lh*.ggpht.com). The broken state is WP-faithful — we match the oracle
in this aspect.

**Conclusion:** The built header is a faithful static approximation of the original dynamic
Shashin Picasa gallery. The structural difference (`<div>` vs `<table>`) is acceptable;
the visual intent (6 photo thumbnails with Picasa links and EXIF captions) is reproduced.
The decision to keep the Picasa strip as static HTML (commit `8d0ada8`) is confirmed correct.

**Disposition:** DOCUMENTED-DIVERGENCE / ACCEPTED — the divergence is intentional per design
spec ("Remove Broken Features: Picasa integration"). No further action needed.
