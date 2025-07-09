---
author: mithro
categories:
- rcs-darcs
date: 2007-02-26T05:07:56+1000
excerpt: Darcs is a really cool SCM system. We use it for Thousand Parsec and I really
  like all the way it works. However there are some very annoying bugs which keep
  pissing me off. So now I’m going to rant.....
layout: post
permalink: /archives/rcs/darcs/19-darcs-almost-perfect
title: darcs almost perfect.
wordpress_category: rcs-darcs
wordpress_id: 19
wordpress_url: https://blog.mithis.net/archives/rcs/darcs/19-darcs-almost-perfect
---

<div >
<p><a href="http://darcs.net/">Darcs</a> is a really cool SCM system. We use it for Thousand Parsec and I really like all the way it works. However there are some very annoying bugs which keep pissing me off. So now I’m going to rant about what these problems are,</p>
<dl>
<dt>Using Massive amounts of memory with Binary files</dt>
<dd>Darcs is an absolute memory hog when you try and use it to manage even small binary files. I have seen it balloon to over 700mb on a little 7mb binary file. This keeps biting me in the arse because we are using darcs to manage our <a href="http://darcs.thousandparsec.net/darcsweb/darcsweb.cgi?r=web;a=summary">web repository</a>. It’s starting to get so bad I’m thinking of switching that repository to <a href="http://subversion.tigris.org/">subversion</a>. We have already had to convert our <a href="http://www.thousandparsec.net/svn/media/">media</a> repository to subversion because of this problem :-/.</dd>
<dt>Not using good terminal interaction.</dt>
<dd>Darcs is design to be used interactively. However it crashes if you send it weird control characters or other strange stuff. It also doesn’t let you use the cursor keys to change long message title and such. Currently I have to use the “add long comment” if I want to fix anything in a patch title (which is very annoying for small patches).</dd>
<dt>Darcs being written in Haskel</dt>
<dd>By writing Darcs in <a href="http://www.haskell.org/haskellwiki/Haskell">Haskel</a> I am unable to try and fix the above bugs. It is also the main reason using Darcs under “alternative” operating systems (such as Windows or Mac OS X) sucks so much (getting a working Haskell compiler is a real chore). Even when you do get it working it doesn’t quite fit properly (and the console IO is even more fragile). Mathematical correctness doesn’t mean you code doesn’t have any bugs. Being unusable is very much a huge bug.</dd>
</dl>
<p>It’s starting to get to the Stage that I’m considering other SCM tools such as <a href="http://www.selenic.com/mercurial/wiki/">Mercurial</a> or maybe even <a href="http://monotone.ca/">monotone</a>.</p>
</div>