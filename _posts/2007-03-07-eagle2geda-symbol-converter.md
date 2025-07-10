---
author: mithro
categories:
- pcb
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
Well, after the last post I thought I would give the [Eagle](http://www.cadsoftusa.com/) to [gEDA](http://www.geda.seul.org/) converter a try. At first I thought about reverse engineering the Eagle format and then output the result. This would have the advantage that you wouldn’t need to run Eagle to do this. I decided that this would be too much work and was about to give up, but then I remembered that Eagle has quite a good scripting language called [ULP](http://www.cadsoftusa.com/Tour/tour12.htm). About 2 hours later I have this [script which converts “symbols” in an Eagle library to a gEDA symbol]({{ ). As this seems so easy I may continue and see if I can make a converter for a complete Schematic and PCB. I’ve attached a picture of a symbol in both [gschem](http://www.geda.seul.org/tools/gschem/index.html) and Eagle at the same time.Hope other people find this useful too.
[](http://blog.mithis.net/wp-content/uploads/2007/03/eagle2geda.png)