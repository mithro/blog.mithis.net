---
author: mithro
categories:
- Pcb
date: 2007-03-07T14:09:50-0500
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/pcb/23-eagle2geda-symbol-converter
title: eagle2geda Symbol Converter
wayback_recovered: true
wordpress_category: pcb
wordpress_id: 23
wordpress_url: https://blog.mithis.net/archives/pcb/23-eagle2geda-symbol-converter
---

<div >
<table>
<tr>
<td >Well, after the last post I thought I would give the <a href="http://www.cadsoftusa.com/">Eagle</a> to <a href="http://www.geda.seul.org/">gEDA</a> converter a try. At first I thought about reverse engineering the Eagle format and then output the result. This would have the advantage that you wouldn’t need to run Eagle to do this. I decided that this would be too much work and was about to give up, but then I remembered that Eagle has quite a good scripting language called <a href="http://www.cadsoftusa.com/Tour/tour12.htm">ULP</a>. About 2 hours later I have this <a href="/assets/images/wp-content/uploads/2007/04/eagle2geda.ulp">script which converts “symbols” in an Eagle library to a gEDA symbol</a>. As this seems so easy I may continue and see if I can make a converter for a complete Schematic and PCB. I’ve attached a picture of a symbol in both <a href="http://www.geda.seul.org/tools/gschem/index.html">gschem</a> and Eagle at the same time.Hope other people find this useful too.</td>
<td><a href="http://blog.mithis.net/wp-content/uploads/2007/03/eagle2geda.png" title="Component in Eagle and gschem"><img alt="Component in Eagle and gschem" height="208" src="http://web.archive.org/web/20091017100646im_/http://blog.mithis.net/wp-content/uploads/2007/03/eagle2geda.png" width="275"/></a></td>
</tr>
</table>
</div>