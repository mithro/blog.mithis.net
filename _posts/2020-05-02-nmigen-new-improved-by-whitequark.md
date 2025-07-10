---
author: mithro
categories:
- hardware
date: 2020-05-02 10:12:03 +1000
excerpt: As people may know, I’m a big supporter of the Migen and associated LiteX
  ecosystem. As of today if you are starting a new project today, I would instead
  recommend...
layout: post
permalink: /archives/hardware/2186-nmigen-new-improved-by-whitequark
title: nMigen – a new improved Migen developed by whitequark!
wordpress_category: hardware
wordpress_id: 2186
wordpress_url: https://blog.mithis.net/archives/hardware/2186-nmigen-new-improved-by-whitequark
---
As people may know, I’m a big supporter of the [Migen](https://github.com/m-labs/migen) and associated [LiteX ecosystem](https://github.com/enjoy-digital/litex). As of today if you are starting a new project today, I would instead recommend that you chose to use [nMigen](https://github.com/nmigen/nmigen) instead.
[nMigen, A refreshed Python toolbox for building complex digital hardware](https://github.com/nmigen/nmigen) is a project that [whitequark](https://whitequark.org/) has been working on for the last couple of years and I’m really liking the new improve syntax and the fact that it [interfaces directly to Yosys](https://github.com/YosysHQ/yosys).
There seems a lot of interesting things happening in the [nMigen ecosystem](https://github.com/nmigen/nmigen);
- [Lambda Concept](https://lambdaconcept.com/) has built an [32-bit RISC-V soft processor called Minerva](https://github.com/lambdaconcept/minerva). The CPU core currently implements the RISC-V RV32IM instruction set, is pipelined on 6 stages and largely inspired [by the LatticeMico32 processor](https://en.wikipedia.org/wiki/LatticeMico32).
- [Robert Baruch](https://www.youtube.com/channel/UCBcljXmuXPok9kT_VGA3adg) has [a multipart series where he uses nMigen — a Python toolbox — to recreate a 6800 CPU](https://www.youtube.com/watch?v=85ZCTuekjGA) like the one used in many vintage video games and pinball machines.
- [Kate Temkin](https://twitter.com/ktemkin) is also working on creating [a new USB 2.0 protocol stack in nMigen](https://luna.readthedocs.io/en/latest/gateware/usb2_device.html) for [the LUNA: a USB multitool (& nMigen library)](https://github.com/greatscottgadgets/luna). I believe that she is also hoping to work on a USB 3.0 stack using the ECP5 high speed transceivers by [rewriting the Daisho core](https://github.com/enjoy-digital/daisho) and [the work that Enjoy Digital did to make a transceivers adapter](https://github.com/enjoy-digital/usb3_pipe).
