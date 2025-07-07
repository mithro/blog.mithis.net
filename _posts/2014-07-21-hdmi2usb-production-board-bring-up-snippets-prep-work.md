---
author: mithro
categories:
- Timvideos Us
date: 2014-07-21 12:47:13 +1000
excerpt: Two weeks ago I decided that I was going to take a week of work and spend
  it full time working on bringing up the HDMI2USB Production board that I’m...
layout: post
permalink: /archives/timvideos-us/1980-hdmi2usb-production-board-bring-up-snippets-prep-work
title: HDMI2USB – Production Board Bring Up – Snippets – Prep Work
wordpress_category: timvideos-us
wordpress_id: 1980
wordpress_url: https://blog.mithis.net/archives/timvideos-us/1980-hdmi2usb-production-board-bring-up-snippets-prep-work
---

<div class="entry-content">
<p>Two weeks ago I decided that I was going to take a week of work and spend it full time working on bringing up the HDMI2USB Production board that I’m working on creating with Numato. Since I’m making all our GSoC students do daily snippets, I thought it would be good for me to do snippets too! Will be good to look back on the week and see what I ended up actually doing.</p>
<p>The following snippets are for the preparation work I did before the week;</p>
<ul>
<li>Spent a whole bunch of time cleaning up and organising the <a href="https://github.com/timvideos/HDMI2USB/issues">GitHub issues</a>, including;
<ul>
<li>Creating a bunch of tasks and <a href="https://github.com/timvideos/HDMI2USB/issues?milestone=1&amp;state=open">milestone</a> to track the bring up work,</li>
<li>Writing some <a href="https://github.com/timvideos/HDMI2USB/blob/master/CONTRIBUTING.md">documentation on how we use labels</a> in the GitHub issue tracker,</li>
<li>Organising <a href="https://github.com/timvideos/HDMI2USB/issues?milestone=2">issues related to GSoC2014</a>. Found a bunch of pull requests from the start of GSoC that hadn’t been merged and looked at merging them.</li>
</ul>
</li>
<li><a href="https://docs.google.com/spreadsheets/d/10vNcsOAxnuiwc5diespjIepMySxhR0iVZfYxouq4p-E/edit#gid=0">Created a spreadsheet</a> which compares the production board to the Atlys prototyping board and will be used for tracking all HDMI2USB variants into the future.</li>
<li><a href="https://docs.google.com/document/d/1-oq0WZnooKVja8QQSS2u60MwGc0YNB3TprSNDk-SNVU/edit?usp=drive_web">Created a document proposing a future directory structure for HDMI2USB firmware to allow multiple boards, interfaces and other features.</a></li>
<li>Organised with <a href="http://dreamsxtrinsic.blogspot.com.au/">Rohit</a> to get a <a href="https://github.com/rohit91/HDMI2USB-vmodvga">VGA capture board</a> during this time.</li>
<li>Probably a bunch of other stuff I have totally forgotten.</li>
</ul>
<p> </p>
<h2>Friday – 18th July</h2>
<ul>
<li>Finished a bunch of <a href="https://codereview.chromium.org/user/mithro">paid work</a>.</li>
<li>Flew to Adelaide. <a href="http://jms.id.au/">Joel</a> picked me up from the Airport.</li>
<li>Started work on using ‘git-filter-branch’ to extract our <a href="http://code.timvideos.us/gst-switch.html#speakertrack">PTZ and speaker tracking modules</a> out of the <a href="https://github.com/timvideos/gst-plugins-bad/tree/speakertrack">gst-plugins-bad</a> repo into a normal plugins repository while preserving history.</li>
<li>Helped Joel get IPv6 working at his place.</li>
<li>Fixed up IPv6 on <a href="http://storage.mithis.com">home server</a> to allow VMs public access.</li>
<li>Started up the <a href="http://github.com/mithro/slidelint_site">slidelint website</a> VM and got it a working public IPv6 address.</li>
<li>Set up a Ubuntu Precise VM to help test <a href="http://aps-sids.github.io/porting-flumotion/">aps-sids flumotion porting work</a>.</li>
</ul>
<p> </p>
<h2>Saturday – 19th July</h2>
<ul>
<li>Day off. Spent day playing DOTA 2 and StarCraft 2 with Joel’s mates.</li>
</ul>
<p> </p>
<h2>Sunday – 20th</h2>
<ul>
<li>Concentrated on getting <a href="http://github.com/mithro/slidelint_site">slidelint website</a> up and running, targeting announcement at <a href="http://www.pycon-au.org">PyCon AU</a>.</li>
<li>Created DNS configuration and deployed it. Also updated the domain tracking spreadsheet.</li>
<li>Rewrote the setup documentation (and ported it to Markdown).</li>
<li>Set up a nginx frontend.</li>
<li>Attempted to get <a href="https://github.com/mozilla-services/circus-web">circus-web</a> interface working.
<ul>
<li>Turns out it doesn’t work under Python 3 as torandio2 is unmaintained.</li>
<li>Ported circus-web to sockjs-torando.</li>
<li>Found the tests don’t work.</li>
</ul>
</li>
</ul>
<p> </p>
</div>