---
author: mithro
categories:
- useful-bits
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
Here at Google we have quite a few remote file systems which contain various tools we use in our day-to-day work. As typing sucks we generally want the tools in our $PATH. When you try to tab complete Bash needs to [stat](http://linux.die.net/man/2/stat) a couple of thousand files and even on fast remote file systems this takes a drastically long time.
I wrote FastComplete as a solution to this problem. The tool creates a local cache of links on your hard drive to everything in your $PATH. It uses a couple of tricks to make sure all the stats remain locally, while still allowing the remote file to change without needing to update the cache. Linux should also keep this information in memory disk cache making tab completion almost instant again. Yay!
You can find FastComplete at [https://github.com/mithro/rcfiles/blob/master/bin/fastcomplete](https://github.com/mithro/rcfiles/blob/master/bin/fastcomplete) It is a stand alone python program which shouldn’t have any non-core dependencies. The usage documentation is as follows;
> 
Fast complete creates a local disk cache of your path.
It’s specifically designed to make bash tab complete run much faster. The correct fix would be to add caching to bash, but it was to hard to do so.
To find out what path fastcomplete is currently using:
> ~tansell/bin/fastcomplete
# Found 3977 commands
export PATH=/home/tansell/bin: ... :/home/build/google3/googledata/validators:/home/build/google3/ads/db
To get fastcomplete to rebuild it’s cache:
```
> ~tansell/bin/fastcomplete --rebuild
# Using path of '/home/tansell/bin: ... :/home/build/google3/googledata/validators:/home/build/google3/ads/db'
# Cache /usr/local/google/users//tansell/tabcache/d7e5fb63454ae33b4a171b6437be904a did not exist! Rebuilding....
# Looking in: /home/tansell/bin (execv)
...
# Looking in: /usr/bin (symlink)
...
# Looking in: /home/build/google3/ads/db (execv)
# Found 3977 commands
export PATH=/usr/local/google/users//tansell/tabcache/d7e5fb63454ae33b4a171b6437be904a
```
To use fastcomplete all the time add the following as the *LAST* line in your ~/.bashrc file. Fastcomplete will echo some output to stderr so you can see what is happening.
# Create a cache of the command
eval `~tansell/bin/fastcomplete $PATH`
