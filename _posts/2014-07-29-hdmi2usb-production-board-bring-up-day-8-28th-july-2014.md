---
author: mithro
categories:
- timvideos-us
date: 2014-07-29 00:13:02 +1000
excerpt: Updated the HDMI2USB variant spreadsheet with new Numato board pin out. Successfully
  generated a HDMI2USB firmware for Numato board with new pin information. That fixes
  the constraint issue! Successfully generated...
layout: post
permalink: /archives/timvideos-us/2009-hdmi2usb-production-board-bring-up-day-8-28th-july-2014
title: HDMI2USB – Production Board Bring Up – Day 8 (28th July 2014)
wordpress_category: timvideos-us
wordpress_id: 2009
wordpress_url: https://blog.mithis.net/archives/timvideos-us/2009-hdmi2usb-production-board-bring-up-day-8-28th-july-2014
---
- Updated the [HDMI2USB variant spreadsheet](https://docs.google.com/a/mithis.com/spreadsheets/d/10vNcsOAxnuiwc5diespjIepMySxhR0iVZfYxouq4p-E/edit#gid=1936356070) with new Numato board pin out.
- Successfully generated a HDMI2USB firmware for Numato board with new pin information. That fixes the constraint issue!
- Successfully generated a HDMI2USB firmware for Numato board with second receive port (RX2) disabled!
<li>Was able to view the HDMI2USB test image output on TX2!
- Was able to capture the HDMI2USB test image via mplayer!
- Was unable to detect a screen on RX1.
</li>
- Created a “flash.sh” script to use libFPGALink to flash the FPGA and then load the Cypress firmware.
- Wrote a Python script to interrogate the CDC serial port for status of the firmware.
