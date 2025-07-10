---
author: mithro
categories:
- timvideos-us
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
## 25th July 2014
- Setup [xob](https://github.com/xobs)‘s hacked up [colormake in our build system](https://github.com/timvideos/HDMI2USB/pull/69). Nice colorized output now!
- Fought more with
ERROR:Place - Constraint Resolved NO placeable site for hdmiMatri_Comp/dvi_rx1/ioclk_buf issue</pre>
- Watched [Paul Fenwick’s OSCon Keynote](https://www.youtube.com/watch?v=xuK6udkbyGo).
**Streaming System Hacking**
- Made the configuration system better and adding a lot of comments to the json file (which isn’t really valid json any more).
- Made pycon2internal.py slightly better and able to parse PyOhio format (based on the PyCon US format).
- Added hack to make event2internal.py to use pycon2internal.py at some periods.
- Set up a bunch of encoders in the Oregon EC2 region.
- Get access to www.timvideos.us again and deployed the updated website.
## 26th July 2014
- Went into the [Adelaide Hackerspace](http://hackerspace-adelaide.org.au/) and created a cable to interface the [USB3300 ULPI](http://www.microchip.com/wwwproducts/Devices.aspx?product=USB3300) chip to 2xPMOD headers.
- Got streaming working for day 1 of [PyOhio](http://pyohio.org), it was late as we were disorganised.
- [aps-sids](http://aps-sids.github.io/) foolishly pointed out a bug in the title of the streaming system, so I [taught him](http://logs.timvideos.us/%23timvideos/%23timvideos.2014-07-26.log.html#t2014-07-26T16:15:22) about how we actually flumotion for an event.
##  27th July 2014
- Did a lot of spreadsheet hacking on the production board pin planning spreadsheet;
- Added half bank / BUFIO2 regions.
- Added dedicated clock pin information.

- Started work on reshuffling the pins to fix the timing issue.
- Helped aps-sids get [Flumotion working on the latest Twisted release](https://github.com/timvideos/flumotion/tree/modern-twisted-fix). Turned out that [someone else](http://lists.fluendo.com/pipermail/flumotion-devel/2014-January/000698.html) had already done most of the work and only a couple very small fixes where needed. [aps-sids reported](http://logs.timvideos.us/%23timvideos/%23timvideos.2014-07-28.log.html#t2014-07-28T05:43:23) that he was now able to run flumotion on Ubuntu Trusty!
