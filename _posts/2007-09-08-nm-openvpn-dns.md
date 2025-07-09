---
author: mithro
categories:
- Ideas
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

<div >
<p>My <a href="http://www.astc-design.com/">new job</a> uses <a href="http://www.openvpn.org/">OpenVPN</a> to provide secure access to their private network. They also make heavy use of the dns domain search so that you only have to type “wiki” to get to their wiki. It turns out that the Open VPN plugin for network manager ignores the “dns-domain” setting, this means I have to manually change /etc/resolv.conf (to add the needed “search” section) after every connection.</p>
<p>This annoyed me enough that I have developed a small patch for the plugin which fixes support. I’ve submitted the patch to <a href="http://www.ubuntu.com/">Ubuntu,</a> hopefully it will get included soon. In the meantime I have attached the <a href="/assets/images/wp-content/uploads/2007/09/nm-openvpn-dnsdomain.patch" title="Patch for OpenVPN plugin to support â€œdns-domainâ€ setting.">patch</a> and the <a href="/assets/images/wp-content/uploads/2007/09/network-manager-openvpn_032svn2342-1ubuntu2_i386.deb" title="Patched OpenVPN plugin for Ubuntu.">deb for Ubuntu Gusty.</a></p>
<p><i>Edit: This patch has been included in <a href="https://bugs.launchpad.net/ubuntu/+source/network-manager-openvpn/+bug/138181">Ubuntu Gusty</a>!</i></p>
</div>