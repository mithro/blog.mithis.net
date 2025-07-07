---
author: mithro
categories:
- Useful Bits
date: 2016-05-03 12:26:52 +1000
excerpt: If you want to restrict the keys that ssh tries when connecting to a server,
  you need to use the IdentityFile and IdentitiesOnly configuration options in your
  ssh_config. However, a...
layout: post
permalink: /archives/useful-bits/2172-using-identitiesonly-without-key-files
title: Using “IdentitiesOnly” without key files
wordpress_category: useful-bits
wordpress_id: 2172
wordpress_url: https://blog.mithis.net/archives/useful-bits/2172-using-identitiesonly-without-key-files
---

<div class="entry-content">
<p>If you want to restrict the keys that ssh tries when connecting to a server, you need to use the <em>IdentityFile</em> and <em>IdentitiesOnly</em> <a href="http://linux.die.net/man/5/ssh_config">configuration options in your ssh_config</a>. </p>
<p>However, a couple of the keys I have are auto generated, with the key being loaded directly into ssh-agent and never written to a file on disk. For hopefully obvious reasons, you can’t dump a private key back out of the agent, but it turns out that <em>IdentityFile</em> only needs the public key which you <strong>can</strong> get.</p>
<p>I ended up using the following script to dump the public keys to files;</p>

```bash
# Dump the public keys
for KEY in $(ssh-add -l | sed -e's/[^ ]\+ [^ ]\+ \([^ ]\+\) .*/\1/'); do
  if echo $KEY | grep -q '^/'; then
    continue
  fi
  export KEY_FILE="$HOME/.ssh/agent.$(echo $KEY | sed -e's/[^A-Za-z0-9]/_/g').pub"
  echo "Saving $KEY into $KEY_FILE"
  ssh-add -L | grep $KEY > $KEY_FILE
done
```

<p>Then I added the following to the ssh_config</p>

```bash
IdentitiesOnly true

  IdentityFile ~/.ssh/agent.keyname.pub
```

<p>When running with “ssh -vv” I see the following in the output;</p>

```text
debug2: set_newkeys: mode 1

debug1: SSH2_MSG_NEWKEYS sent

debug1: expecting SSH2_MSG_NEWKEYS

debug2: set_newkeys: mode 0

debug1: SSH2_MSG_NEWKEYS received

debug1: SSH2_MSG_SERVICE_REQUEST sent

debug2: service_accept: ssh-userauth

debug1: SSH2_MSG_SERVICE_ACCEPT received

debug2: key: /home/tansell/.ssh/agent.keyb.pub (0x2257da0), explicit

debug1: Authentications that can continue: publickey,password

debug1: Next authentication method: publickey

debug1: Offering ECDSA public key: //home/tansell/.ssh/agent.keyb.pub

debug2: we sent a publickey packet, wait for reply
```

</div>