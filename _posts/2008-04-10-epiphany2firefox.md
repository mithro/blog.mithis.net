---
author: mithro
categories:
- uncategorized
date: 2008-04-10T10:04:50+0000
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/uncategorized/77-epiphany2firefox
title: Quotidian!
wayback_recovered: true
wordpress_category: uncategorized
wordpress_id: 77
wordpress_url: https://blog.mithis.net/archives/uncategorized/77-epiphany2firefox
---
I’m sure most people are wondering what he hell “[quotidian](http://dictionary.reference.com/search?q=Quotidian&x=0&y=0)” is, I myself did not know this word existed.  The word actually means mundane or everyday, a work colleague suggested it when I asked is anyone knew what the opposite to epiphany was. So you probably wondering why I’m going on about some stupid word, well the reason is that I have finally converted from the gnome [Epiphany](http://live.gnome.org/Epiphany) web browser to [Firefox](http://www.mozilla.com/en-US/firefox/).
For thoses who don’t know, Epiphany is generally described as “the closest thing to Gnome’s official web browser”. It has lots of nifty features and use to have much better intergration with the Gnome desktop (things like actually using the Gnome print dialog). I use to advocate that Gnome should push Epiphany instead of Firefox.
So why have I given up? I’m tired of my browser being broken.
The developers of Epiphany decided to make some huge changes in the latest version, they started adding support for the [WebKit](http://webkit.org/) (the render behind Safari) instead of just being dependent on [Gecko](http://en.wikipedia.org/wiki/Gecko_(layout_engine)) (the same render Firefox uses). This is actually a very good goal, being able to have a choice of renders in my browser would be great. However, in the process of doing this change they broke everything! Things like the vitally important Adblock extension no longer work and the password manager is totally broken in a number of ways – for a long time they didn’t even show up in the dialog.
I’m okay with a few bugs here and there (even these quite serious ones) to get something better in the long run. I have diligently reported bugs as I found them (even firing up a different browser when the gnome bug browser was crashing Epiphany). I even started porting Google Gears to Epiphany because I had faith that Epiphany was going to remain a killer browser.
Now I find out that it has all been for nothing, the developers have decided they are going to totally ditch Gecko and move only to WebKit (with all the compatibility problems it will bring). There are so many reasons why this is a bad idea, none of which I’m going to repeat here.
So I’m now writing this in Firefox instead of Epiphany and I’m pretty happy. Having access to all the extensions that Firefox has is really nice for once. There a number of features which I miss from Epiphany and extensions have filled most of that void, so what did I install?
- [Tab History](http://www.penguinus.com/dev/tab_history/), this means that new tabs have the same history as the parent tab. This is something Epiphany does by default and I find absolutely vital.
- [Compact Menu 2](https://addons.mozilla.org/en-US/firefox/addon/4550), a little extension which gives you the ability to have all your menus in a single button saving you precious vertical screen space.
- [Ad Block Plus](http://adblockplus.org/en/), got to keep away those evil ads. It’s amazing how annoying the web is with ads, I had gotten so use to not seeing them that I didn’t know how bad it actually was.
- [NoScript](http://noscript.net/), get rid of all that annoying flash and evil javascript. In epiphany I generally ended up just apt-get removing flash, now I can still watch stupid Youtube videos without being violated by monkies.
I also installed two extensions that have no equivalent under Epiphany, they are
- [Greasemonkey](https://addons.mozilla.org/en-US/firefox/addon/748), the extension for making websites the way you like them.
- [Firebug](http://www.getfirebug.com/), a really cool tool for figuring out how a website is made up and various problems with them.
I’m still looking for an extension which makes the Firefox 3.0 URL bar sane. I really like how the Epiphany one behaves and will probably end up writing my own extension if I don’t find anything. The important features that I require are,
- Single line per URL with the title on the right.
- Support for “smart bookmarks” as the last option. These let you search for the current term at Google or Wikipedia without prefixing it with a stupid keyword or something.
Here is what my Firefox looks like currently. As you can see I have significantly customized the toolbar to remove all that excesses.
[<img alt="Screenshot of my Firefox" src="http://web.archive.org/web/20110311214257im_//assets/images/wp-content/uploads/2008/04/myfirefox.png" | relative_url }}"/>]({{ )
