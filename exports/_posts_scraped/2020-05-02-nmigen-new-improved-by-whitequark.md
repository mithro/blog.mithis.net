---
layout: "post"
title: "nMigen – a new improved Migen developed by whitequark!"
date: "2020-05-02 10:12:03 +1000"
categories:
  - Hardware
author: "mithro"
excerpt: "As people may know, I’m a big supporter of the Migen and associated LiteX ecosystem. As of today if you are starting a new project today, I would instead recommend..."
wordpress_url: "https://blog.mithis.net/archives/hardware/2186-nmigen-new-improved-by-whitequark"
---

<div class="entry-content">
<p>As people may know, I’m a big supporter of the <a href="https://github.com/m-labs/migen" target="_blank">Migen</a> and associated <a href="https://github.com/enjoy-digital/litex" target="_blank">LiteX ecosystem</a>. As of today if you are starting a new project today, I would instead recommend that you chose to use <a href="https://github.com/nmigen/nmigen">nMigen</a> instead.</p>
<p><a href="https://github.com/nmigen/nmigen">nMigen, A refreshed Python toolbox for building complex digital hardware</a> is a project that <a href="https://whitequark.org/">whitequark</a> has been working on for the last couple of years and I’m really liking the new improve syntax and the fact that it <a href="https://github.com/YosysHQ/yosys">interfaces directly to Yosys</a>.</p>
<p>There seems a lot of interesting things happening in the <a href="https://github.com/nmigen/nmigen">nMigen ecosystem</a>;</p>
<ul>
<li><a href="https://lambdaconcept.com/">Lambda Concept</a> has built an <a href="https://github.com/lambdaconcept/minerva">32-bit RISC-V soft processor called Minerva</a>. The CPU core currently implements the RISC-V RV32IM instruction set, is pipelined on 6 stages and largely inspired <a href="https://en.wikipedia.org/wiki/LatticeMico32">by the LatticeMico32 processor</a>.</li>
<li><a href="https://www.youtube.com/channel/UCBcljXmuXPok9kT_VGA3adg" target="_blank">Robert Baruch</a> has <a href="https://www.youtube.com/watch?v=85ZCTuekjGA">a multipart series where he uses nMigen — a Python toolbox — to recreate a 6800 CPU</a> like the one used in many vintage video games and pinball machines.</li>
<li><a href="https://twitter.com/ktemkin">Kate Temkin</a> is also working on creating <a href="https://luna.readthedocs.io/en/latest/gateware/usb2_device.html">a new USB 2.0 protocol stack in nMigen</a> for <a href="https://github.com/greatscottgadgets/luna">the LUNA: a USB multitool (&amp; nMigen library)</a>. I believe that she is also hoping to work on a USB 3.0 stack using the ECP5 high speed transceivers by <a href="https://github.com/enjoy-digital/daisho">rewriting the Daisho core</a> and <a href="https://github.com/enjoy-digital/usb3_pipe">the work that Enjoy Digital did to make a transceivers adapter</a>.</li>
</ul>
</div>