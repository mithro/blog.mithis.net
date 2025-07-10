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
- Looked into if Travis CI has IPv6 connectivity. [It appears so!](https://travis-ci.org/mithro/temp/builds/30607921)
- Investigated git server side hooks as a method to run CI on build.timvideos.tv
<li>Travis-CI does a git push to build.timvideos.tv which does a make in the post-recieve.
- Issues;
<li>For non-pull requests we could encode the private key using Travis’s encrypted environment variables.
- What about pull requests? Mean anyone can send arbitrary code to build.timvideos.tv – Maybe use QEmu’s COW support and reboot after each build?
</li>
- Looked a jig for a nice way to write the git hooks.
<li>[Sent a pull request](https://github.com/robmadole/jig/pull/8) to fix some documentation.
- Really designed to run as a “pre-commit” hook locally on a person’s machine rather than a server side hook. [Logged an issue to discuss that.](https://github.com/robmadole/jig/issues/9)
- Has a lot of nice plugins for Python development already.
- Would allow us to add hdl-pretty as a commit hook.
</li>
- Alternatives to jig appear to be;
<li>https://github.com/icefox/git-hooks – Written in bash
- https://pypi.python.org/pypi/git-pre-commit-hook – Written in python
</li> /li>
- Got my “fake” Xilinx Platform Cable USB (Model DLC9G) working under Linux – Full instructions can be found at [https://github.com/timvideos/HDMI2USB/wiki/Xilinx-Platform-Cable-USB-under-Linux](https://github.com/timvideos/HDMI2USB/wiki/Xilinx-Platform-Cable-USB-under-Linux)
<li>The device was [purchased from eBay](http://www.ebay.com.au/itm/Xilinx-Platform-USB-Download-Cable-Jtag-Programmer-for-FPGA-CPLD-C-Mod-XC2C64A/390809652326) on the 11th July, costed $37 USD with shipping and arrived at Joel’s house on Monday.
- First issue was /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/setup_pcusb didn’t understand I had udev and was trying to install for the ancient hotplug.
<li>Fixed by changing line 26 from TP_USE_UDEV=”0″ to TP_USE_UDEV=”1″
</li>
- Next setup_pcusb didn’t tell udev to reload the udev rules. Had to do that with udevadm control –reload-rules
- Next setup_pcusb didn’t ask me to install fxload, so I needed to install it with apt-get install fxload
- Next the rules that were installed to /etc/udev/rules.d/xusbdfwu.rules were invalid; they caused the following errors in /var/log/daemon.log
</li>
Jul 23 16:40:29 laptop udevd[841]: unknown key 'SYSFS{idVendor}' in /etc/udev/rules.d/xusbdfwu.rules:2
Jul 23 16:40:29 laptop udevd[841]: invalid rule '/etc/udev/rules.d/xusbdfwu.rules:2'
Jul 23 16:46:11 laptop udevd[841]: unknown key 'SYSFS{idVendor}' in /etc/udev/rules.d/xusbdfwu.rules:3
Jul 23 16:46:11 laptop udevd[841]: invalid rule '/etc/udev/rules.d/xusbdfwu.rules:3'</pre>
- This was fixed with;
<li>Changing SYSFS to ATTRS
- Changing BUS to SUBSYSTEM
- Changing $TEMPNODE to $tempnode
</li>
- The little status light then turned on red! Yay!
- Was able to do a boundary scan in iMPACT on a Zybo development board after soldering a header onto it.
- Received the HDMI2USB production boards created by [Numato](http://numato.com/)!
<li>Started with bunch of stuff to do with LEDs;
<li>Logged issues about LEDs not been label intelligently. Such as the “power” LED being labeled “D33”.
- Researched the DONE net again so I could understand the D2 LED (which should be named D_FPGA_NOT_CONFIGURED or DNCFG for short). Started adding the information to the JTAG/Reset documentation.
- Figured out why D3 (connected to the Cypress INT1 pin) was only faintly lit.
</li>
- Logged a bunch of issue regarding small silk screen fixes to make future boards easier to understand.
- Logged an issue about adding some standoffs in the center of the board for mechanical stability.
- Logged an issue about having a good GND point to connect your probe too.
<li>This page describes the two good ways to add a GND test point – http://www.robotroom.com/PCB-Layout-Tips.html
</li>
- Starting researching the 5V rail and if we could remove it totally (thus saving a bunch of stuff). Looks like we can, but needs more investigation.
- After replacing the JTAG cable was able to use iMPACT to boundary scan and it found Spartan 6 chip!
</li>
- Discovered CEC is 3V3 signal.
### Non HDMI2USB stuff
- Tried to figure out why my home router has decided that it wants to hand out address in the 2001:44b8:31dc:8d01::/64 rather than the 2001:44b8:31dc:8d00::/64 range it use too.
- Found a bunch of issues with domains served of ns1.mithis.com as the secondary servers where disabled. Root cause was an old version of PowerDNS failing on TCP zone transfers causing domains to become stale and get dropped from the secondaries. Enabled email notification when secondary disables the zones.
