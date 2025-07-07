---
layout: "post"
title: "Connecting to a Fritz!Box under Linux using vpnc"
date: "2013-10-06 23:44:04 +1000"
categories:
  - Ubuntu
author: "mithro"
excerpt: "I have two Fritz!Box 7390 (one at my place and one at my parents primary residence) and one Fritz!Box 7270 devices (the house they are building). They are pretty reasonable..."
wordpress_url: "https://blog.mithis.net/archives/ubuntu/1833-connecting-to-a-fritzbox-under-linux-using-vpnc"
---

<div class="entry-content">

<p>I have two <a href="http://fritzbox.com.au/product-fritz-wlan7390.html" target="_blank">Fritz!Box 7390</a> (one at my place and one at my parents primary residence) and one <a href="http://fritzbox.com.au/product-fritz-wlan7270.html" target="_blank">Fritz!Box 7270 devices</a> (the house they are building). They are pretty reasonable “high end” ADSL routers and a cool feature is they integrated VPN support. I use this functionality to connect the three networks securely together (but that is not what this post is about). This VPN functionality can also be used to connect to your home network while not at home, but information on how to do this from Linux is very sparse (specially if you only want to use FOSS tools to do the connection), so here is how I did it.</p>
<h2>Configuring your Fritz!Box</h2>
<p>To set up your Fritz!Box you need a configuration file, there is no GUI available in the web interface to support create new VPN configurations. While a number of sites have pre-built .cfg files that look like they should work, my Fritz!Boxes only accept encrypted VPN configuration files (see end of post for more information) and no open source tool exists to encrypt them.</p>
<p>I instead needed to use the FRITZ!Box VPN Connection tool (while it is a Windows program but runs fine under Wine) to create the configuration. It can be downloaded from the <a href="http://webgw.avm.de/download/Download_en.jsp?partid=14657" target="_blank">AVM website</a> (This is different to the VPN client that AVM also provide). Annoyingly the tool doesn’t just read existing .cfg configuration files, it instead reads it’s own vpnadmin.cfg found in <code>c:/users/your username/Application Data/AVM/FRITZ!VPN</code> and then generates a .cfg file and encrypts it.</p>
<p>Using the FRITZ!Box VPN Connection tool to create a configuration that is compatible with vpnc you must:</p>
<ul>
<li>Select “Configure VPN for one User” type connection</li>
<li>On the “Select Device” screen, select “iPhone, iPod touch or iPad” option</li>
<li>On the “Enter the user’s email address” screen, despite the admin tool calling this field the user email, just enter a username. I recommend <strong>not</strong> having any special characters like @ or . in it.</li>
<li>On the “Enter IP address of the User” screen, be careful about what IP address you use (the default should be okay).
<ul>
<li>Don’t use the same IP address that the computer uses when connected via wireless/wired. While it seems like a good idea, as the computer would have the same IP address even when remote, it <strong>does not work</strong> and will mean the device is unable to access the internet when connected to wireless/wired.</li>
<li>The “Send all data over the VPN tunnel” option on this page does not seem to affect vpnc, it will always route all your data over the vpn connection. See later for how to fix this problem.</li>
</ul>
</li>
<li>On the “Key for the connection” screen enter a password. Copy down the shared secret key, you’ll want it when creating the vpnc config. I recommend also keeping the default shared secret key it generates unless your super paranoid about entropy.</li>
</ul>
<p>You can check that you have done this correctly in two ways;</p>
<ul>
<li>The vpnadmin.cfg will have the <code>iphone=1</code> and <code>xauth_key="your password"</code> options. See below for a partial example;<br/>
<code>
<pre>
...
  user {
    nameoremail = "xxxx";
    key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    ip = 192.168.179.201;
    internetaccess = 0;
    <strong>iphone = 1;
    xauth_key = "xxxxx";</strong>
  }
...
</pre>
<p></p></code></li>
<li>If you export an unencrypted config file (remember this can’t be loaded onto the Fritz!Box – so make sure you also export an encrypted version!), the remoteid section will have a key field and not a fqdn field, use_xauth will be set to yes and an xauth section will exist. See below for a partial example;<br/>
<code>
<pre>
...
  keepalive_ip = 0.0.0.0;
  remoteid {
    <strong>key_id</strong> = "qnap";
  }
  mode = phase1_mode_aggressive;
  phase1ss = "all/all/all";
  keytype = connkeytype_pre_shared;
  key = "f3e0hcca19ca2a3gaafbI.{1dGe3q8f84";
  cert_do_server_auth = no;
  use_nat_t = yes;
  <strong>use_xauth = yes;
  xauth {
    valid = yes;
    username = "qnap";
    passwd = "qnappassword";
  }</strong>
  use_cfgmode = yes;
...</pre>
<p></p></code></li>
</ul>
<h2>Configuring vpnc on your Linux box</h2>
<p></p>
<p>The Fritz!Box needs both draft-ietf-ipsec-nat-t-ike-03 support and the client to adopt the server suggested lifetime (which for the Fritz!Box is 3600 seconds). These features where only added to vpnc recently, so make sure your vpnc is newer than subversion revision 511. Both the version in Debian Unstable and any Ubuntu newer than Precise (12.04) have vpnc 0.5.3r512, which is new enough version and you can just <code>apt-get install vpnc</code>. For Fedora 17 x86 systems you can find RPMs at http://www.pabloendres.com/2013/02/27/vpnc-and-fritzbox/</p>
<p>Create the vpnc config in <code>/etc/vpnc/fritzbox.conf</code> using the following as a template (replace the parts in bold/brackets):<br/>
<code>
<pre>
IPSec gateway <strong>ip address or DNS name of your FritzBox</strong>

IKE DH Group dh2
Perfect Forward Secrecy nopfs

IPSec ID <strong>[username entered into the "Enter the user's email address" screen]</strong>
# "key" from the Fritz!Box VPN configuration
IPSec secret <strong>[shared secret key from the "Key for the connection" screen]</strong>

NAT Traversal Mode force-natt

Xauth username <strong>[username entered into the "Enter the user's email address" screen]</strong>
Xauth password <strong>[password entered into the "Key for the connection" screen - Not the password use to encrypt the vpnc configuration!]</strong>
</pre>
<p></p></code></p>
<p>As this file contains usernames and password, the config file should be owned by root and only readable by the owner.<br/>
<code><br/>
sudo chown root /etc/vpnc/fritzbox.conf<br/>
sudo chmod 0600 /etc/vpnc/fritzbox.conf<br/>
</code></p>
<p>You should now be able to connect to your home internet using:<br/>
<code><br/>
sudo vpnc-connect fritzbox<br/>
</code></p>
<p>When you are finished, use:<br/>
<code><br/>
sudo vpnc-disconnect fritzbox<br/>
</code></p>
<h2>Internet Access while using vpnc</h2>
<p></p>
<p>When vpnc connects it will change your default route to go via the tunnel. This will send all your local internet traffic over the VPN connection. If you are setting up the VPN to secure your internet browsing while on a hostile network such as a public WiFi hotspot (such as at a coffee shop) this is what you want.</p>
<p>However, if you just want to be able to access the hosts on your home network, you don’t want this as it will make your internet browsing extraordinarily slow.  These routes are set up by <code>/etc/vpn/vpnc-script</code> script, so you will need custom one. Normally this script is provided a lot of information when connecting to other VPN concentrators (such as a Cisco EasyVPN device) but when connecting to the Fritz!Box you only seem to get limited information.</p>
<p>I created the following script in <code>/etc/vpnc/fritzbox-script</code>, marked it as executable (<code>chmod a+x /etc/vpnc/fritzbox-script</code>) and then added “<code>Script /etc/vpnc/fritzbox-script</code>” to my <code>/etc/vpnc/fritzbox.conf</code> file.</p>
<p><code>
<pre>
#!/bin/sh

IPROUTE=/sbin/ip

case "$reason" in
  pre-init)
    /etc/vpnc/vpnc-script pre-init
    ;;
  connect)
    INTERNAL_IP4_PREFIX=$(echo $INTERNAL_IP4_ADDRESS | sed -e's/\.[0-9]\+$//')
    $IPROUTE link set dev "$TUNDEV" up mtu 1024
    $IPROUTE addr add "$INTERNAL_IP4_ADDRESS/255.255.255.0" peer "$INTERNAL_IP4_ADDRESS" dev "$TUNDEV"
    $IPROUTE route replace "$INTERNAL_IP4_PREFIX.0/255.255.255.0" dev "$TUNDEV"
    $IPROUTE route flush cache
    ;;
  disconnect)
    $IPROUTE link set dev "$TUNDEV" down
    ;;
  *)
    echo "unknown reason '$reason'. Maybe vpnc-script is out of date" 1&gt;&amp;2
    exit 1
    ;;
esac
exit 0
</pre></code>
<blockquote>
<h2>Fritz!Box encrypted VPN configuration files</h2>
<p>Fritz!Boxes will <span style="color: #ff0000;">only accept VPN configurations which are encrypted</span>. Otherwise when try to import the file you will get the cryptic "Error: Import of the VPN settings failed." as seen below;<br/>
<img alt="Error: Import of the VPN settings failed." class="alignnone size-full wp-image-1835" height="265" sizes="(max-width: 745px) 100vw, 745px" src="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error.png" srcset="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error.png 745w, https://blog.mithis.net/wp-content/uploads/2013/10/VPN-error-300x106.png 300w" width="745"/></p>
<p>To create an encrypted file you must use the FRITZ!Box VPN Connection tool. Then when exporting, select "Save VPN settings in a file under" option, check the "Encrypt VPN settings" check box (the file type should change to .eff), and enter your chosen password twice.</p>
<p><img alt="Export VPN settings" class="alignnone size-full wp-image-1836" height="306" sizes="(max-width: 442px) 100vw, 442px" src="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-encrypt.png" srcset="https://blog.mithis.net/wp-content/uploads/2013/10/VPN-encrypt.png 442w, https://blog.mithis.net/wp-content/uploads/2013/10/VPN-encrypt-300x207.png 300w" width="442"/></p></blockquote>
</p></div>