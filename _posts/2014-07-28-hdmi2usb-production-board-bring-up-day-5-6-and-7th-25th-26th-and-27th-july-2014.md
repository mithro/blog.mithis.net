---
author: mithro
categories:
- Timvideos Us
date: 2014-07-28 23:39:31 +1000
excerpt: 25th July 2014 Setup xob‘s hacked up colormake in our build system. Nice
  colorized output now! Fought more with ERROR:Place - Constraint Resolved NO placeable
  site for hdmiMatri_Comp/dvi_rx1/ioclk_buf issue Watched...
layout: post
permalink: /archives/timvideos-us/2003-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014
title: HDMI2USB – Production Board Bring Up – Day 5, 6 and 7 (25th, 26th and 27th
  July 2014)
wordpress_category: timvideos-us
wordpress_id: 2003
wordpress_url: https://blog.mithis.net/archives/timvideos-us/2003-hdmi2usb-production-board-bring-up-day-5-6-and-7th-25th-26th-and-27th-july-2014
---

<div class="entry-content">
<h2>25th July 2014</h2>
<ul>
<li>Setup <a href="https://github.com/xobs">xob</a>‘s hacked up <a href="https://github.com/timvideos/HDMI2USB/pull/69">colormake in our build system</a>. Nice colorized output now!</li>
<li>Fought more with
<pre>ERROR:Place - Constraint Resolved NO placeable site for hdmiMatri_Comp/dvi_rx1/ioclk_buf issue</pre>
</li>
<li>Watched <a href="https://www.youtube.com/watch?v=xuK6udkbyGo">Paul Fenwick’s OSCon Keynote</a>.</li>
</ul>
<p><strong>Streaming System Hacking</strong></p>
<ul>
<li>Made the configuration system better and adding a lot of comments to the json file (which isn’t really valid json any more).</li>
<li>Made pycon2internal.py slightly better and able to parse PyOhio format (based on the PyCon US format).</li>
<li>Added hack to make event2internal.py to use pycon2internal.py at some periods.</li>
<li>Set up a bunch of encoders in the Oregon EC2 region.</li>
<li>Get access to www.timvideos.us again and deployed the updated website.</li>
</ul>
<p> </p>
<h2>26th July 2014</h2>
<ul>
<li>Went into the <a href="http://hackerspace-adelaide.org.au/">Adelaide Hackerspace</a> and created a cable to interface the <a href="http://www.microchip.com/wwwproducts/Devices.aspx?product=USB3300">USB3300 ULPI</a> chip to 2xPMOD headers.</li>
<li>Got streaming working for day 1 of <a href="http://pyohio.org">PyOhio</a>, it was late as we were disorganised.</li>
<li><a href="http://aps-sids.github.io/">aps-sids</a> foolishly pointed out a bug in the title of the streaming system, so I <a href="http://logs.timvideos.us/%23timvideos/%23timvideos.2014-07-26.log.html#t2014-07-26T16:15:22">taught him</a> about how we actually flumotion for an event.</li>
</ul>
<p> </p>
<h2> 27th July 2014</h2>
<ul>
<li>Did a lot of spreadsheet hacking on the production board pin planning spreadsheet;
<ul>
<li>Added half bank / BUFIO2 regions.</li>
<li>Added dedicated clock pin information.</li>
</ul>
</li>
<li>Started work on reshuffling the pins to fix the timing issue.</li>
<li>Helped aps-sids get <a href="https://github.com/timvideos/flumotion/tree/modern-twisted-fix">Flumotion working on the latest Twisted release</a>. Turned out that <a href="http://lists.fluendo.com/pipermail/flumotion-devel/2014-January/000698.html">someone else</a> had already done most of the work and only a couple very small fixes where needed. <a href="http://logs.timvideos.us/%23timvideos/%23timvideos.2014-07-28.log.html#t2014-07-28T05:43:23">aps-sids reported</a> that he was now able to run flumotion on Ubuntu Trusty!</li>
</ul>
<p> </p>
</div>