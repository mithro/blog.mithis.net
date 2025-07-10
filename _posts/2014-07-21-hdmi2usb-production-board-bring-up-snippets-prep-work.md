---
author: mithro
categories:
- timvideos-us
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
Two weeks ago I decided that I was going to take a week of work and spend it full time working on bringing up the HDMI2USB Production board that I’m working on creating with Numato. Since I’m making all our GSoC students do daily snippets, I thought it would be good for me to do snippets too! Will be good to look back on the week and see what I ended up actually doing.
The following snippets are for the preparation work I did before the week;
- Spent a whole bunch of time cleaning up and organising the [GitHub issues](https://github.com/timvideos/HDMI2USB/issues), including;
<li>Creating a bunch of tasks and [milestone](https://github.com/timvideos/HDMI2USB/issues?milestone=1&state=open) to track the bring up work,
- Writing some [documentation on how we use labels](https://github.com/timvideos/HDMI2USB/blob/master/CONTRIBUTING.md) in the GitHub issue tracker,
- Organising [issues related to GSoC2014](https://github.com/timvideos/HDMI2USB/issues?milestone=2). Found a bunch of pull requests from the start of GSoC that hadn’t been merged and looked at merging them.
</li>
- [Created a spreadsheet](https://docs.google.com/spreadsheets/d/10vNcsOAxnuiwc5diespjIepMySxhR0iVZfYxouq4p-E/edit#gid=0) which compares the production board to the Atlys prototyping board and will be used for tracking all HDMI2USB variants into the future.
- [Created a document proposing a future directory structure for HDMI2USB firmware to allow multiple boards, interfaces and other features.](https://docs.google.com/document/d/1-oq0WZnooKVja8QQSS2u60MwGc0YNB3TprSNDk-SNVU/edit?usp=drive_web)
- Organised with [Rohit](http://dreamsxtrinsic.blogspot.com.au/) to get a [VGA capture board](https://github.com/rohit91/HDMI2USB-vmodvga) during this time.
- Probably a bunch of other stuff I have totally forgotten.
## Friday – 18th July
- Finished a bunch of [paid work](https://codereview.chromium.org/user/mithro).
- Flew to Adelaide. [Joel](http://jms.id.au/) picked me up from the Airport.
- Started work on using ‘git-filter-branch’ to extract our [PTZ and speaker tracking modules](http://code.timvideos.us/gst-switch.html#speakertrack) out of the [gst-plugins-bad](https://github.com/timvideos/gst-plugins-bad/tree/speakertrack) repo into a normal plugins repository while preserving history.
- Helped Joel get IPv6 working at his place.
- Fixed up IPv6 on [home server](http://storage.mithis.com) to allow VMs public access.
- Started up the [slidelint website](http://github.com/mithro/slidelint_site) VM and got it a working public IPv6 address.
- Set up a Ubuntu Precise VM to help test [aps-sids flumotion porting work](http://aps-sids.github.io/porting-flumotion/).
## Saturday – 19th July
- Day off. Spent day playing DOTA 2 and StarCraft 2 with Joel’s mates.
## Sunday – 20th
- Concentrated on getting [slidelint website](http://github.com/mithro/slidelint_site) up and running, targeting announcement at [PyCon AU](http://www.pycon-au.org).
- Created DNS configuration and deployed it. Also updated the domain tracking spreadsheet.
- Rewrote the setup documentation (and ported it to Markdown).
- Set up a nginx frontend.
- Attempted to get [circus-web](https://github.com/mozilla-services/circus-web) interface working.
<li>Turns out it doesn’t work under Python 3 as torandio2 is unmaintained.
- Ported circus-web to sockjs-torando.
- Found the tests don’t work.
</li>
