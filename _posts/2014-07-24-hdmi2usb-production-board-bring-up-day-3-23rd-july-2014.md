---
author: mithro
categories:
- timvideos-us
date: 2014-07-24 01:54:52 +1000
excerpt: Looked into if Travis CI has IPv6 connectivity. It appears so! Investigated
  git server side hooks as a method to run CI on build.timvideos.tv Travis-CI does
  a git push to...
layout: post
permalink: /archives/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014
title: HDMI2USB – Production Board Bring Up – Day 3 (23rd July 2014)
wordpress_category: timvideos-us
wordpress_id: 1993
wordpress_url: https://blog.mithis.net/archives/timvideos-us/1993-hdmi2usb-production-board-bring-up-day-3-23rd-july-2014
---

<div class="entry-content">
<ul>
<li>Looked into if Travis CI has IPv6 connectivity. <a href="https://travis-ci.org/mithro/temp/builds/30607921">It appears so!</a></li>
<li>Investigated git server side hooks as a method to run CI on build.timvideos.tv
<ul>
<li>Travis-CI does a git push to build.timvideos.tv which does a make in the post-recieve.</li>
<li>Issues;
<ul>
<li>For non-pull requests we could encode the private key using Travis’s encrypted environment variables.</li>
<li>What about pull requests? Mean anyone can send arbitrary code to build.timvideos.tv – Maybe use QEmu’s COW support and reboot after each build?</li>
</ul>
</li>
<li>Looked a jig for a nice way to write the git hooks.
<ul>
<li><a href="https://github.com/robmadole/jig/pull/8">Sent a pull request</a> to fix some documentation.</li>
<li>Really designed to run as a “pre-commit” hook locally on a person’s machine rather than a server side hook. <a href="https://github.com/robmadole/jig/issues/9">Logged an issue to discuss that.</a></li>
<li>Has a lot of nice plugins for Python development already.</li>
<li>Would allow us to add hdl-pretty as a commit hook.</li>
</ul>
</li>
<li>Alternatives to jig appear to be;
<ul>
<li>https://github.com/icefox/git-hooks – Written in bash</li>
<li>https://pypi.python.org/pypi/git-pre-commit-hook – Written in python</li>
</ul>
</li>
</ul>
</li>
<li>Got my “fake” Xilinx Platform Cable USB (Model DLC9G) working under Linux – Full instructions can be found at <a href="https://github.com/timvideos/HDMI2USB/wiki/Xilinx-Platform-Cable-USB-under-Linux">https://github.com/timvideos/HDMI2USB/wiki/Xilinx-Platform-Cable-USB-under-Linux</a>
<ul>
<li>The device was <a href="http://www.ebay.com.au/itm/Xilinx-Platform-USB-Download-Cable-Jtag-Programmer-for-FPGA-CPLD-C-Mod-XC2C64A/390809652326">purchased from eBay</a> on the 11th July, costed $37 USD with shipping and arrived at Joel’s house on Monday.</li>
<li>First issue was /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/setup_pcusb didn’t understand I had udev and was trying to install for the ancient hotplug.
<ul>
<li>Fixed by changing line 26 from TP_USE_UDEV=”0″ to TP_USE_UDEV=”1″</li>
</ul>
</li>
<li>Next setup_pcusb didn’t tell udev to reload the udev rules. Had to do that with udevadm control –reload-rules</li>
<li>Next setup_pcusb didn’t ask me to install fxload, so I needed to install it with apt-get install fxload</li>
<li>Next the rules that were installed to /etc/udev/rules.d/xusbdfwu.rules were invalid; they caused the following errors in /var/log/daemon.log</li>
</ul>
</li>
</ul>
<pre style="padding-left: 90px;">Jul 23 16:40:29 laptop udevd[841]: unknown key 'SYSFS{idVendor}' in /etc/udev/rules.d/xusbdfwu.rules:2
Jul 23 16:40:29 laptop udevd[841]: invalid rule '/etc/udev/rules.d/xusbdfwu.rules:2'
Jul 23 16:46:11 laptop udevd[841]: unknown key 'SYSFS{idVendor}' in /etc/udev/rules.d/xusbdfwu.rules:3
Jul 23 16:46:11 laptop udevd[841]: invalid rule '/etc/udev/rules.d/xusbdfwu.rules:3'</pre>
<ul>
<ul>
<li>This was fixed with;
<ul>
<li>Changing SYSFS to ATTRS</li>
<li>Changing BUS to SUBSYSTEM</li>
<li>Changing $TEMPNODE to $tempnode</li>
</ul>
</li>
<li>The little status light then turned on red! Yay!</li>
<li>Was able to do a boundary scan in iMPACT on a Zybo development board after soldering a header onto it.</li>
</ul>
</ul>
<ul>
<li>Received the HDMI2USB production boards created by <a href="http://numato.com/">Numato</a>!
<ul>
<li>Started with bunch of stuff to do with LEDs;
<ul>
<li>Logged issues about LEDs not been label intelligently. Such as the “power” LED being labeled “D33”.</li>
<li>Researched the DONE net again so I could understand the D2 LED (which should be named D_FPGA_NOT_CONFIGURED or DNCFG for short). Started adding the information to the JTAG/Reset documentation.</li>
<li>Figured out why D3 (connected to the Cypress INT1 pin) was only faintly lit.</li>
</ul>
</li>
<li>Logged a bunch of issue regarding small silk screen fixes to make future boards easier to understand.</li>
<li>Logged an issue about adding some standoffs in the center of the board for mechanical stability.</li>
<li>Logged an issue about having a good GND point to connect your probe too.
<ul>
<li>This page describes the two good ways to add a GND test point – http://www.robotroom.com/PCB-Layout-Tips.html</li>
</ul>
</li>
<li>Starting researching the 5V rail and if we could remove it totally (thus saving a bunch of stuff). Looks like we can, but needs more investigation.</li>
<li>After replacing the JTAG cable was able to use iMPACT to boundary scan and it found Spartan 6 chip!</li>
</ul>
</li>
<li>Discovered CEC is 3V3 signal.</li>
</ul>
<h3>Non HDMI2USB stuff</h3>
<ul>
<li>Tried to figure out why my home router has decided that it wants to hand out address in the 2001:44b8:31dc:8d01::/64 rather than the 2001:44b8:31dc:8d00::/64 range it use too.</li>
<li>Found a bunch of issues with domains served of ns1.mithis.com as the secondary servers where disabled. Root cause was an old version of PowerDNS failing on TCP zone transfers causing domains to become stale and get dropped from the secondaries. Enabled email notification when secondary disables the zones.</li>
</ul>
<p> </p>
</div>