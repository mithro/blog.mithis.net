---
author: mithro
categories:
- uncategorized
tags:
- acpi
- hal
- intrepid
- power
- resume
- scripts
- suspend
- Ubuntu
date: 2009-01-19T15:12:19+1000
excerpt: 'On previous versions of Ubuntu, the scripts which are called after a resume
  from suspend have been found in /etc/acpi/resume.d directory. I used this functionality
  to turn off.....'
layout: post
permalink: /archives/uncategorized/92-power-scripts-in-intrepid
title: WTF power scripts went in Intrepid….
wordpress_category: uncategorized
wordpress_id: 92
wordpress_url: https://blog.mithis.net/archives/uncategorized/92-power-scripts-in-intrepid
---
On previous versions of [Ubuntu](http://www.ubuntu.com/), the scripts which are called after a resume from suspend have been found in */etc/acpi/resume.d* directory. I used this functionality to turn off some of the hardware in my Vaio which I don’t use (such as the bluetooth and the cdrom drive).

This stopped working when I upgraded to Ubuntu Intrepid. Even more strangely while the scripts are still installed, even they are never called.

It appears that thanks to moving towards [HAL](http://www.freedesktop.org/wiki/Software/hal) (which is probably a “Good Thing”) these scripts are no longer used. The scripts which are used can be found in */etc/pm/*. Not only has the location changed, but the script format has too.

Previously, my script was found in */etc/acpi/resume.d/99-custom.sh* looked like the following,

>     #! /bin/sh
>     # Turn off the CD drive and the bluetooth device
>     echo 1 > /sys/devices/platform/sony-laptop/cdpower
>     echo 0 > /sys/devices/platform/sony-laptop/cdpower
>
>     echo 1 > /sys/devices/platform/sony-laptop/bluetoothpower
>     echo 0 > /sys/devices/platform/sony-laptop/bluetoothpower

Now my script script must be found in */etc/pm/sleep.d/10-custom* and looks like the following,

>     #!/bin/sh -e
>     case "$1" in
>     	resume)
>     		# Turn off the CD drive and the bluetooth device
>     		echo 1 > /sys/devices/platform/sony-laptop/cdpower
>     		echo 0 > /sys/devices/platform/sony-laptop/cdpower
>
>     		echo 1 > /sys/devices/platform/sony-laptop/bluetoothpower
>     		echo 0 > /sys/devices/platform/sony-laptop/bluetoothpower
>     	;;
>     esac

The main reason I’m posting this on my blog is that this change does **not seem to be documented anywhere**. Searching on Google for things like “resume script intrepid” or “/etc/acpi/resume.d intrepid” does not come up with anything useful. Hopefully some people will find this helpful.
