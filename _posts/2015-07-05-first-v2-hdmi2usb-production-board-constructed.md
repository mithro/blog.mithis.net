---
author: mithro
categories:
- timvideos-us
date: 2015-07-05 14:47:57 +1000
excerpt: For the last year and a half, I have been working with Numato Labs to create
  a “HDMI2USB Production Board” for our HDMI2USB firmware that was originally developed
  on the...
layout: post
permalink: /archives/timvideos-us/2045-first-v2-hdmi2usb-production-board-constructed
title: First V2 “HDMI2USB Production Board” constructed!
wordpress_category: timvideos-us
wordpress_id: 2045
wordpress_url: https://blog.mithis.net/archives/timvideos-us/2045-first-v2-hdmi2usb-production-board-constructed
---
For the last year and a half, I have been working with [Numato Labs](http://numato.com) to create a “HDMI2USB Production Board” for our [HDMI2USB firmware](https://github.com/timvideos/HDMI2USB) that was originally developed on the [Digilent Atlys board](http://digilentinc.com/atlys/). On Friday, they sent me a picture of the first constructed board!
[<img alt='HDMI2USB "Production Board" Version 2' class="wp-image-2046" height="436" sizes="(max-width: 661px) 100vw, 661px" src="{{ "/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg" | relative_url }}" srcset="/assets/images/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-1024x675.jpg 1024w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-300x197.jpg 300w, https://blog.mithis.net/wp-content/uploads/2015/07/HDMI2USB-Prod-V2-900x593.jpg 900w" width="661"/>HDMI2USB “Production Board” Version 2
At the end of last year, we decided to abandon our first attempt and start again from scratch, this picture is the result of that work. Some of the reasons we decided to start from scratch was;
- A “de facto standard” for locking HDMI ports was established and low cost connectors became available. This meant we no longer needed to support both DVI and HDMI connectors, reducing the complexity significantly and solving some persistent issues.
- Not only did the cost of Spartan 6 parts with high speed “GTP” transceivers drop but our understanding of how to use them increased. This would allow us to create a board which natively supports DisplayPort.
- The idea streaming via not only USB, but also Ethernet became a stronger possibility, meaning the extra cost of adding ethernet was now worth it.
Overall, our board has the following differences with the Atlys board;
- Has DDR3 memory instead of DDR2, increasing the memory bandwidth.
- Has a Spartan S6LX45**T** with the GTP broken out to DisplayPort headers.
- Has a PCI-Express style expansion connector instead of the expensive VHDCI connector, allow much cheaper expansion boards.
- Has all the extra pins on the FX2, increasing the potential USB interface options.
- Has control over all the HDMI functionality, including hot plug and CEC functionality.
- Removes parts we don’t need such as the audio, buttons, switches and LEDs.
- Mounts in any ITX style computer case.
- Adds UTMI USB (as well as the Cypress FX2)
- Adds MicroSD connector.
