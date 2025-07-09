---
author: mithro
categories:
- Useful Bits
date: 2011-12-16 14:05:46 +1000
excerpt: Here at Google we have quite a few remote file systems which contain various
  tools we use in our day-to-day work. As typing sucks we generally want the tools
  in...
layout: post
permalink: /archives/useful-bits/407-fastcomplete
title: FastComplete, making bash completion fast on remote file systems
wordpress_category: useful-bits
wordpress_id: 407
wordpress_url: https://blog.mithis.net/archives/useful-bits/407-fastcomplete
---

<div class="entry-content">
<p>Here at Google we have quite a few remote file systems which contain various tools we use in our day-to-day work. As typing sucks we generally want the tools in our $PATH. When you try to tab complete Bash needs to <a href="http://linux.die.net/man/2/stat">stat</a> a couple of thousand files and even on fast remote file systems this takes a drastically long time.</p>
<p>I wrote FastComplete as a solution to this problem. The tool creates a local cache of links on your hard drive to everything in your $PATH. It uses a couple of tricks to make sure all the stats remain locally, while still allowing the remote file to change without needing to update the cache. Linux should also keep this information in memory disk cache making tab completion almost instant again. Yay!</p>
<p>You can find FastComplete at <a href="https://github.com/mithro/rcfiles/blob/master/bin/fastcomplete">https://github.com/mithro/rcfiles/blob/master/bin/fastcomplete</a> It is a stand alone python program which shouldn’t have any non-core dependencies. The usage documentation is as follows;</p>
<blockquote><p>
Fast complete creates a local disk cache of your path.<br/>
It’s specifically designed to make bash tab complete run much faster. The correct fix would be to add caching to bash, but it was to hard to do so.</p>
<p>To find out what path fastcomplete is currently using:</p>
<div class="wp_syntax"><table><tr><td class="code"><pre class="bash" style="font-family:monospace;"><span style="color: #000000; font-weight: bold;">></span> ~tansell<span style="color: #000000; font-weight: bold;">/</span>bin<span style="color: #000000; font-weight: bold;">/</span>fastcomplete
<span style="color: #666666; font-style: italic;"># Found 3977 commands</span>
<span style="color: #7a0874; font-weight: bold;">export</span> <span style="color: #007800;">PATH</span>=<span style="color: #000000; font-weight: bold;">/</span>home<span style="color: #000000; font-weight: bold;">/</span>tansell<span style="color: #000000; font-weight: bold;">/</span>bin: ... :<span style="color: #000000; font-weight: bold;">/</span>home<span style="color: #000000; font-weight: bold;">/</span>build<span style="color: #000000; font-weight: bold;">/</span>google3<span style="color: #000000; font-weight: bold;">/</span>googledata<span style="color: #000000; font-weight: bold;">/</span>validators:<span style="color: #000000; font-weight: bold;">/</span>home<span style="color: #000000; font-weight: bold;">/</span>build<span style="color: #000000; font-weight: bold;">/</span>google3<span style="color: #000000; font-weight: bold;">/</span>ads<span style="color: #000000; font-weight: bold;">/</span>db</pre></td></tr></table></div>
<p>To get fastcomplete to rebuild it’s cache:</p>
<div class="wp_syntax"><table><tr><td class="code"><pre class="bash" style="font-family:monospace;"><span style="color: #000000; font-weight: bold;">></span> ~tansell<span style="color: #000000; font-weight: bold;">/</span>bin<span style="color: #000000; font-weight: bold;">/</span>fastcomplete <span style="color: #660033;">--rebuild</span>
<span style="color: #666666; font-style: italic;"># Using path of '/home/tansell/bin: ... :/home/build/google3/googledata/validators:/home/build/google3/ads/db'</span>
<span style="color: #666666; font-style: italic;"># Cache /usr/local/google/users//tansell/tabcache/d7e5fb63454ae33b4a171b6437be904a did not exist! Rebuilding....</span>
<span style="color: #666666; font-style: italic;"># Looking in: /home/tansell/bin (execv)</span>
...
<span style="color: #666666; font-style: italic;"># Looking in: /usr/bin (symlink)</span>
...
<span style="color: #666666; font-style: italic;"># Looking in: /home/build/google3/ads/db (execv)</span>
<span style="color: #666666; font-style: italic;"># Found 3977 commands</span>
<span style="color: #7a0874; font-weight: bold;">export</span> <span style="color: #007800;">PATH</span>=<span style="color: #000000; font-weight: bold;">/</span>usr<span style="color: #000000; font-weight: bold;">/</span>local<span style="color: #000000; font-weight: bold;">/</span>google<span style="color: #000000; font-weight: bold;">/</span>users<span style="color: #000000; font-weight: bold;">//</span>tansell<span style="color: #000000; font-weight: bold;">/</span>tabcache<span style="color: #000000; font-weight: bold;">/</span>d7e5fb63454ae33b4a171b6437be904a</pre></td></tr></table></div>
<p>To use fastcomplete all the time add the following as the *LAST* line in your ~/.bashrc file. Fastcomplete will echo some output to stderr so you can see what is happening.</p>
<div class="wp_syntax"><table><tr><td class="code"><pre class="bash" style="font-family:monospace;"><span style="color: #666666; font-style: italic;"># Create a cache of the command</span>
<span style="color: #7a0874; font-weight: bold;">eval</span> <span style="color: #000000; font-weight: bold;">`</span>~tansell<span style="color: #000000; font-weight: bold;">/</span>bin<span style="color: #000000; font-weight: bold;">/</span>fastcomplete <span style="color: #007800;">$PATH</span><span style="color: #000000; font-weight: bold;">`</span></pre></td></tr></table></div>
</blockquote>
</div>