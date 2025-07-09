---

author: mithro
categories:
- ideas
date: 2007-09-06T12:39:48+1100
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/ideas/51-nm-autovpn
title: Network Manager – Autostart VPN
wayback_recovered: true
wordpress_category: ideas
wordpress_id: 51
wordpress_url: https://blog.mithis.net/archives/ideas/51-nm-autovpn
comments:
  - id: 7248
    author: Dorian Scholz
    date: 2011-05-11T09:21:29+00:00
    content: |
      <p>Since this page has a high google rank for this topic, here is a more elegant solution possible from NetworkManager 0.8.1 on:</p> <p>There is now a command line tool nmcli which can interact with the nm-applet and NM directly.<br /> So connecting to a VPN is as easy as this:</p> <p>nmcli con up id NAME_OF_THE_VPN</p>
  - id: 7284
    author: Mahavir
    date: 2011-12-06T21:16:11+00:00
    content: |
      <p>For stock installation of Ubuntu 10.04 (Lucid Lynx) users, Network Manager version 0.8.0, so nmcli is not available and since there may be others like me who like to stick to the LTS, here is a solution.</p> <p>Visit <a href="http://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python?h=NM_0_8" rel="nofollow">http://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python?h=NM_0_8</a> and download list-connections.py. Mark it as executable and run it to find the UUID of your VPN connection.</p> <p>Also, download vpn.py from the same link. This script is written to connect to VPN over wifi only. So, if you want to connect to VPN over your wireless network then simply execute the script.</p> <p>However, for wired a minor modification in vpn.py is required . Below is the patch for the same.</p> <p>*** vpn.py 2011-12-07 02:38:06.205855632 +0530<br /> &#8212; vpn1.py 2011-12-07 02:39:49.861855276 +0530<br /> ***************<br /> *** 86,92 ****<br /> return None</p> <p>! def get_wifi_device_path():<br /> bus = dbus.SystemBus()<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, &#8216;/org/freedesktop/NetworkManager&#8217;)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.NetworkManager&#8217;)<br /> &#8212; 86,92 &#8212;-<br /> return None</p> <p>! def get_device_path(reqDevType):<br /> bus = dbus.SystemBus()<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, &#8216;/org/freedesktop/NetworkManager&#8217;)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.NetworkManager&#8217;)<br /> ***************<br /> *** 95,101 ****<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, d)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.DBus.Properties&#8217;)<br /> devtype = iface.Get(&#8216;org.freedesktop.NetworkManager.Device&#8217;, &#8216;DeviceType&#8217;)<br /> ! if devtype == 2:<br /> return d<br /> return None</p> <p>&#8212; 95,101 &#8212;-<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, d)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.DBus.Properties&#8217;)<br /> devtype = iface.Get(&#8216;org.freedesktop.NetworkManager.Device&#8217;, &#8216;DeviceType&#8217;)<br /> ! if devtype == reqDevType:<br /> return d<br /> return None</p> <p>***************<br /> *** 135,143 ****<br /> print &#8220;couldn&#8217;t find the connection&#8221;<br /> sys.exit(1)</p> <p>! device_path = get_wifi_device_path()<br /> if not device_path:<br /> ! print &#8220;no wifi device found&#8221;<br /> sys.exit(1)</p> <p> # Is it already activated?<br /> &#8212; 135,143 &#8212;-<br /> print &#8220;couldn&#8217;t find the connection&#8221;<br /> sys.exit(1)</p> <p>! device_path = get_device_path(1) #Pass 2 for wifi<br /> if not device_path:<br /> ! print &#8220;no wired device found&#8221;<br /> sys.exit(1)</p> <p> # Is it already activated?</p>
---

<div >
<p><em><strong>UPDATE</strong>: Dorian Scholz writes in the comments; There is now a command line tool <strong>nmcli</strong> which can interact with the nm-applet and Network Manger directly. Connecting to a VPN is as easy as:  <code>nmcli con up id NAME_OF_THE_VPN</code><br/>
</em></p>
<p>Recently I started a <a href="http://www.astc-design.com/" title="Australian Semiconductor Technology Company">new job</a>, to get my laptop on the network I first connect to their wireless LAN and then VPN into the network. <a href="http://www.gnome.org/projects/NetworkManager/" title="Network Manager">Network Manager</a> makes this fairly easily, it will automatically try and associated with the wireless network, I then have to start the VPN connection manually.</p>
<p>This wouldn’t be a problem if I only had to do it once or twice a day. However, wireless being wireless, drops out 4-5 times a day. While, Network Manager will automatically reassociated, I have to manually reconnect to the VPN which is a pain.</p>
<p>To fix this I have developed two small scripts, the first is a small shell script which will automatically call a command when connecting to certain wireless networks (<a href="{{ "/assets/images/wp-content/uploads/2007/09/02runcmd" | relative_url }}" title="Network Manager dispatcher to run a command on connection to network.">/etc/NetworkManager/dispatcher.d/02runcmd</a>). The second is a little Python script which will tell Network Manager to connect to a VPN from the command line (<a href="{{ "/assets/images/wp-content/uploads/2007/09/nm-startvpn" | relative_url }}" title="Python script to start a Network Manager managed VPN">/usr/local/bin/nm-startvpn</a>). When you combind these two, you get auto VPN connection goodness, yay!!</p>
<p>If people find this useful I might put together a config utility and properly package them.</p>
</div>

## Comments

<div class="comments">
<div class="comment" id="comment-7248">
  <div class="comment-meta">
    <strong>Dorian Scholz</strong> -     <time datetime="2011-05-11T09:21:29+00:00">2011-05-11</time>
  </div>
  <div class="comment-content">
    <p>Since this page has a high google rank for this topic, here is a more elegant solution possible from NetworkManager 0.8.1 on:</p> <p>There is now a command line tool nmcli which can interact with the nm-applet and NM directly.<br /> So connecting to a VPN is as easy as this:</p> <p>nmcli con up id NAME_OF_THE_VPN</p>
  </div>
</div>

<div class="comment" id="comment-7284">
  <div class="comment-meta">
    <strong>Mahavir</strong> -     <time datetime="2011-12-06T21:16:11+00:00">2011-12-06</time>
  </div>
  <div class="comment-content">
    <p>For stock installation of Ubuntu 10.04 (Lucid Lynx) users, Network Manager version 0.8.0, so nmcli is not available and since there may be others like me who like to stick to the LTS, here is a solution.</p> <p>Visit <a href="http://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python?h=NM_0_8" rel="nofollow">http://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python?h=NM_0_8</a> and download list-connections.py. Mark it as executable and run it to find the UUID of your VPN connection.</p> <p>Also, download vpn.py from the same link. This script is written to connect to VPN over wifi only. So, if you want to connect to VPN over your wireless network then simply execute the script.</p> <p>However, for wired a minor modification in vpn.py is required . Below is the patch for the same.</p> <p>*** vpn.py 2011-12-07 02:38:06.205855632 +0530<br /> &#8212; vpn1.py 2011-12-07 02:39:49.861855276 +0530<br /> ***************<br /> *** 86,92 ****<br /> return None</p> <p>! def get_wifi_device_path():<br /> bus = dbus.SystemBus()<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, &#8216;/org/freedesktop/NetworkManager&#8217;)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.NetworkManager&#8217;)<br /> &#8212; 86,92 &#8212;-<br /> return None</p> <p>! def get_device_path(reqDevType):<br /> bus = dbus.SystemBus()<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, &#8216;/org/freedesktop/NetworkManager&#8217;)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.NetworkManager&#8217;)<br /> ***************<br /> *** 95,101 ****<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, d)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.DBus.Properties&#8217;)<br /> devtype = iface.Get(&#8216;org.freedesktop.NetworkManager.Device&#8217;, &#8216;DeviceType&#8217;)<br /> ! if devtype == 2:<br /> return d<br /> return None</p> <p>&#8212; 95,101 &#8212;-<br /> proxy = bus.get_object(&#8216;org.freedesktop.NetworkManager&#8217;, d)<br /> iface = dbus.Interface(proxy, dbus_interface=&#8217;org.freedesktop.DBus.Properties&#8217;)<br /> devtype = iface.Get(&#8216;org.freedesktop.NetworkManager.Device&#8217;, &#8216;DeviceType&#8217;)<br /> ! if devtype == reqDevType:<br /> return d<br /> return None</p> <p>***************<br /> *** 135,143 ****<br /> print &#8220;couldn&#8217;t find the connection&#8221;<br /> sys.exit(1)</p> <p>! device_path = get_wifi_device_path()<br /> if not device_path:<br /> ! print &#8220;no wifi device found&#8221;<br /> sys.exit(1)</p> <p> # Is it already activated?<br /> &#8212; 135,143 &#8212;-<br /> print &#8220;couldn&#8217;t find the connection&#8221;<br /> sys.exit(1)</p> <p>! device_path = get_device_path(1) #Pass 2 for wifi<br /> if not device_path:<br /> ! print &#8220;no wired device found&#8221;<br /> sys.exit(1)</p> <p> # Is it already activated?</p>
  </div>
</div>

</div>

<style>
.comments {
  margin-top: 2rem;
  border-top: 1px solid #eee;
  padding-top: 2rem;
}

.comment {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9f9f9;
  border-left: 4px solid #ddd;
}

.comment-meta {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.comment-content {
  line-height: 1.6;
}

.comment-content p {
  margin: 0.5rem 0;
}
</style>
