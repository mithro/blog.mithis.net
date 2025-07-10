---
author: mithro
categories:
- ideas
date: 2007-09-08T15:31:41+0000
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/ideas/54-nm-openvpn-dns
title: Network Manager – OpenVPN, DNS Domain support
wayback_recovered: true
wordpress_category: ideas
wordpress_id: 54
wordpress_url: https://blog.mithis.net/archives/ideas/54-nm-openvpn-dns
---
My [new job](http://www.astc-design.com/) uses [OpenVPN](http://www.openvpn.org/) to provide secure access to their private network. They also make heavy use of the dns domain search so that you only have to type “wiki” to get to their wiki. It turns out that the Open VPN plugin for network manager ignores the “dns-domain” setting, this means I have to manually change /etc/resolv.conf (to add the needed “search” section) after every connection.
This annoyed me enough that I have developed a small patch for the plugin which fixes support. I’ve submitted the patch to [Ubuntu,](http://www.ubuntu.com/) hopefully it will get included soon. In the meantime I have attached the [patch and the [deb for Ubuntu Gusty.
*Edit: This patch has been included in [Ubuntu Gusty](https://bugs.launchpad.net/ubuntu/+source/network-manager-openvpn/+bug/138181)!*
