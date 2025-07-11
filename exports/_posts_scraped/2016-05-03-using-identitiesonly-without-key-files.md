---
layout: "post"
title: "Using “IdentitiesOnly” without key files"
date: "2016-05-03 12:26:52 +1000"
categories:
  - Useful Bits
author: "mithro"
excerpt: "If you want to restrict the keys that ssh tries when connecting to a server, you need to use the IdentityFile and IdentitiesOnly configuration options in your ssh_config. However, a..."
wordpress_url: "https://blog.mithis.net/archives/useful-bits/2172-using-identitiesonly-without-key-files"
---

<div class="entry-content">
<p>If you want to restrict the keys that ssh tries when connecting to a server, you need to use the <em>IdentityFile</em> and <em>IdentitiesOnly</em> <a href="http://linux.die.net/man/5/ssh_config">configuration options in your ssh_config</a>. </p>
<p>However, a couple of the keys I have are auto generated, with the key being loaded directly into ssh-agent and never written to a file on disk. For hopefully obvious reasons, you can’t dump a private key back out of the agent, but it turns out that <em>IdentityFile</em> only needs the public key which you <strong>can</strong> get.</p>
<p>I ended up using the following script to dump the public keys to files;</p>
<blockquote>
<pre><code># Dump the public keys
for KEY in $(ssh-add -l | sed -e's/[^ ]\+ [^ ]\+ \([^ ]\+\) .*/\1/'); do
  if echo $KEY | grep -q '^/'; then
    continue
  fi
  export KEY_FILE="$HOME/.ssh/agent.$(echo $KEY | sed -e's/[^A-Za-z0-9]/_/g').pub"
  echo "Saving $KEY into $KEY_FILE"
  ssh-add -L | grep $KEY &gt; $KEY_FILE
done
</code></pre>
</blockquote>
<p>Then I added the following to the ssh_config</p>
<blockquote><p><code>  IdentitiesOnly true<br/>
  IdentityFile ~/.ssh/agent.keyname.pub<br/>
</code>
</p></blockquote>
<p>When running with “ssh -vv” I see the following in the output;</p>
<blockquote><p><code>debug2: set_newkeys: mode 1<br/>
debug1: SSH2_MSG_NEWKEYS sent<br/>
debug1: expecting SSH2_MSG_NEWKEYS<br/>
debug2: set_newkeys: mode 0<br/>
debug1: SSH2_MSG_NEWKEYS received<br/>
debug1: SSH2_MSG_SERVICE_REQUEST sent<br/>
debug2: service_accept: ssh-userauth<br/>
debug1: SSH2_MSG_SERVICE_ACCEPT received<br/>
debug2: key: /home/tansell/.ssh/agent.keyb.pub (0x2257da0), explicit<br/>
debug1: Authentications that can continue: publickey,password<br/>
debug1: Next authentication method: publickey<br/>
debug1: Offering ECDSA public key: //home/tansell/.ssh/agent.keyb.pub<br/>
debug2: we sent a publickey packet, wait for reply<br/>
</code>
</p></blockquote>
</div>