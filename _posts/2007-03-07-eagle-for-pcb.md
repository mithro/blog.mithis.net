---
author: mithro
categories:
- Ideas
date: 2007-03-07T11:53:32-0500
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/ideas/21-eagle-for-pcb
title: Eagle for PCB
wayback_recovered: true
wordpress_category: ideas
wordpress_id: 21
wordpress_url: https://blog.mithis.net/archives/ideas/21-eagle-for-pcb
---

<div >
<table>
<tr>
<td><a href="http://blog.mithis.net/wp-content/uploads/2007/03/board.png" title="PCB Board for my Honors Project"><img alt="PCB Board for my Honors Project" height="355" src="http://web.archive.org/web/20090817225635im_/http://blog.mithis.net/wp-content/uploads/2007/03/board.png" width="153"/></a></td>
<td >
<p>For the last 3 days I have been working on routing the Honours project. For the design I use <a href="http://www.cadsoftusa.com/">CadSoft Eagle</a>. However, it’s been annoying me quite a bit.Here is just a shortlist of things,</p>
<ul>
<li>You can’t change pads unless you modify a library. At my Uni they use a rivet system for doing plated through holes, these means that the holes and pads have to be a certain size as you have to solder the rivets to the pads. This means that you often want to change a hole and pad for a particular instance of an IC so that it can have a rivet put in it.</li>
<li>Polygon Pours can not be put in “outline” mode. This makes it quite annoying, as you want to put in the GND plane first so it removes all the GND airwires, but then you are constantly using the “rip-up” command so you can see where you are putting signals.</li>
</ul>
<p>
I’m thinking of moving to <a href="http://www.geda.seul.org/">gEDA</a> because it’s free software, I would no longer be restricted with what I do. However, it’s quite hard to use and doesn’t come with the extensive libraries that Eagle has.
</p>
<p>
I’m thinking that I’m going to write a ULP script which converts EAGLE stuff to the format used by gEDA. We’ll see what happens.</p>
</td>
</tr>
</table>
</div>