---
layout: "post"
title: "First V2 “HDMI2USB Production Board” constructed!"
date: "2015-07-05 14:47:57 +1000"
categories:
  - Timvideos Us
author: "mithro"
excerpt: "For the last year and a half, I have been working with Numato Labs to create a “HDMI2USB Production Board” for our HDMI2USB firmware that was originally developed on the..."
wordpress_url: "https://blog.mithis.net/archives/timvideos-us/2045-first-v2-hdmi2usb-production-board-constructed"
---

<div class="entry-content">
<p>For the last year and a half, I have been working with <a href="numato.com">Numato Labs</a> to create a “HDMI2USB Production Board” for our <a href="https://github.com/timvideos/HDMI2USB">HDMI2USB firmware</a> that was originally developed on the <a href="digilentinc.com/atlys/">Digilent Atlys board</a>. On Friday, they sent me a picture of the first constructed board!</p>
<div class="wp-caption aligncenter" id="attachment_2046" style="width: 671px"><a href="https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2.jpg"><img alt='HDMI2USB "Production Board" Version 2' class="wp-image-2046" height="436" sizes="(max-width: 661px) 100vw, 661px" src="https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg" srcset="https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg 1024w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-300x197.jpg 300w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-900x593.jpg 900w" width="661"/></a><p class="wp-caption-text">HDMI2USB “Production Board” Version 2</p></div>
<p>At the end of last year, we decided to abandon our first attempt and start again from scratch, this picture is the result of that work. Some of the reasons we decided to start from scratch was;</p>
<ul>
<li>A “de facto standard” for locking HDMI ports was established and low cost connectors became available. This meant we no longer needed to support both DVI and HDMI connectors, reducing the complexity significantly and solving some persistent issues.</li>
<li>Not only did the cost of Spartan 6 parts with high speed “GTP” transceivers drop but our understanding of how to use them increased. This would allow us to create a board which natively supports DisplayPort.</li>
<li>The idea streaming via not only USB, but also Ethernet became a stronger possibility, meaning the extra cost of adding ethernet was now worth it.</li>
</ul>
<p dir="ltr">Overall, our board has the following differences with the Atlys board;</p>
<ul style="color: rgb(34, 34, 34);">
<li><span style="color: rgb(34, 34, 34);">Has DDR3 memory instead of DDR2, increasing the memory bandwidth.</span></li>
<li>Has a Spartan S6LX45<strong>T</strong> with the GTP broken out to DisplayPort headers.</li>
<li><span style="color: rgb(34, 34, 34);">Has a PCI-Express style expansion connector instead of the expensive VHDCI connector, allow much cheaper expansion boards.</span></li>
<li><span style="color: rgb(34, 34, 34);">Has all the extra pins on the FX2, increasing the potential USB interface options.</span></li>
<li>Has control over all the HDMI functionality, including hot plug and CEC functionality.</li>
<li><span style="color: rgb(34, 34, 34);">Removes parts we don’t need such as the audio, </span>buttons, switches and LEDs.</li>
<li>Mounts in any ITX style computer case.</li>
<li><span style="color: rgb(34, 34, 34);">Adds UTMI USB (as well as the Cypress FX2)</span></li>
<li><span style="color: rgb(34, 34, 34);">Adds MicroSD connector.</span></li>
</ul>
</div>